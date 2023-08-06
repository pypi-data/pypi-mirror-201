# burst

### 一. 概述

逻辑服务器框架。灵感来自于腾讯内部的SPP。

python3 supported


### 二. 模块介绍

进程主要分为 master、proxy、loader、worker 4个部分。
网络部分使用twisted驱动。使用twisted的原因，一是为了简化代码，另一方面也是为了使mac/linux都可以直接运行。否则手写epoll的话，mac下就没法调试了。

1. master

    作为管理进程，负责管理proxy和loader进程的状态。例如proxy/loader异常死掉，master会负责重新拉起。

2. proxy

    网络进程，负责接收网络消息，并且将任务派发给worker进行处理，之后再返回给client端。
    支持tcp/udp监听。
    worker、master 均会与proxy建立连接。并均使用本地socket的方式。
    proxy还支持burstctl的连接，可以进行worker数量配置，统计等操作。当然，需要在服务器启动的时候，打开ADMIN相关的配置。

3. loader

    加载进程，负责启动并管理worker。
    具体查看下文中关于 优雅重启 的部分

4. worker

    工作进程，负责真正的任务处理。
    为了简化模型，worker要求与http协议一样，仅支持一个或者无回应。
    当worker对proxy返回有内容的或者空回应时，会顺便告知proxy，worker状态已经回到idle状态，可以分配任务了。
    而因为有这种应答的特性，所以proxy中对应的worker连接，并没有使用如 [maple](https://github.com/dantezhu/maple) 一样的client_id机制，而是直接将conn的连接弱引用存储在了proxy中对应的worker连接上。

5. burstctl

    管理工具，可以在线完成统计、配置变更、重启等操作。

    - clear            清空消息队列
    - reload           更新workers
    - stat             查看统计
    - stop             安全停止整个服务
    - version          版本号

    统计示例:

    ```
    {
        "clients": 16,
        "workers": {
            "all": 8,
            "1": 8
        },
        "busy_workers": {
            "all": 0,
            "1": 0
        },
        "idle_workers": {
            "all": 8,
            "1": 8
        },
        "pending_tasks": {
            "all": 0,
            "1": 0
        },
        "client_req": 37983,
        "client_rsp": 0,
        "worker_req": {
            "all": 37983,
            "1": 37983
        },
        "worker_rsp": {
            "all": 37983,
            "1": 37983
        },
        "tasks_time": {
            "10": 4484,
            "50": 1267,
            "100": 775,
            "500": 30234,
            "1000": 638,
            "5000": 584,
            "more": 1
        }
    }
    ```

### 三. 部署

以supervisor为例:

```
[program:burst_server]
environment=PYTHON_EGG_CACHE=/tmp/.python-eggs/
directory=/data/release/prj
command=python main.py
user=dantezhu
autorestart=true
redirect_stderr=true
stopwaitsecs=10
```

优雅重启:

```
kill -HUP $master_pid

burstctl reload
```

优雅停止:

```
kill -TERM $master_pid

burstctl stop
```

强制停止:

```
kill -INT $master_pid
```


### 四. 设计思路

1. 优雅重启

    之前在没有loader进程时，我们发现一个问题，即worker的启动速度越来越慢。
    主要原因是当应用越来越复杂时，import的库和模块会越来越多。尤其多个worker同时启动时，时间更长。

    注:
    >后来经过测试，发现worker启动慢的主要原因在于python文件的载入。
    >当主进程载入完毕，如果直接使用multiprocessing.Process来启动的话速度是极快的，所有worker总共才几百毫秒。

    这在maple中还是能够接受的，因为maple的worker其实是无状态的，所以无非是启动两套workers，每套workers单独优雅重启就足以不影响业务。

    但是在burst中，这个是接受不了的，因为burst的workers是分组的，如果用上面的方法启动，就可以导致某个组内的消息一直被堵塞。

    所以，我实现了另一套方案:

    1. master收到HUP信号后，先标识自己的状态为reload中，并通知proxy也变成reload中状态。
    2. master启动一批worker，但是作为替补worker存在，不替换原有的worker。
    3. proxy在reload状态下，将收到的新worker连接也都放到替补workers中去。
    4. proxy在收到client消息、worker工作完成消息、worker建立新连接消息后，都去判断替补worker是否已经达到替换老workers的条件，如果已经达到则替换老workers，并通过master_connection向master发送消息，告知master可以替换掉老workers了。表示自己为非reload状态。
    5. master替换掉老的workers，并向老的workers发送TERM信号。标识自己状态为非reload状态。

    但是这种方案及其复杂，而且因为非原子的特性导致及其容易出现问题。

    所以我们引入了loader进程。

    这也是burst比spp多的一个进程的原因，因为如果直接使用popen启动大量worker的话，python导入包加载很慢。
    所以我们将loader作为起始的进程，后续的worker的启动都是直接通过multiprocessing.Process来启动，就不需要每次popen了，速度快很多。
    新方案完美解决了如下几个问题:

    1. python导入包太慢的问题
    2. 直接支持了reload要求所有worker都停止，才启动新worker的问题(因为只有一个loader)。
    3. 直接支持了group修改count，reload后生效的问题，因为loader本身重新加载了代码。
        当然因为proxy没有重新加载，所以动态增加group/修改group_router还是不行的。

### 五. 注意

1. 配置要求

    group_id务必为数字类型，否则burstctl无法正确处理。另外数字的查找性能也会高一点。

2. 使用udp监听的时候，由于udp的特性，clients数量无法统计。


### 六. 最佳实践

1. 与maple配合

    在之前的德州扑克，偶聊，矩阵危机中，均使用了如下架构：

    ```
    maple.gateway -> maple.broker -> burst
       ^                               |
       |                               |
       +----------forwarder<-----------+
    ```

    即burst作为逻辑服务器进行消息处理，并将响应通过trigger发送给forwarder/gateway。

    如果有同学担心burst的worker是多进程单线程，对于高IO操作的请求不是很友好的话，其实在这里也可以直接在worker中进行多线程处理。
    即worker每次收到一个请求在python的线程池(如ThreadPoolExecutor)中处理。

2. 支持定时器

    比如我们希望实现类似修仙模拟器中每5秒获取经验的功能，那么就需要在worker中实现一个定时器。
    但是因为worker等待task是阻塞的，所以我们可以借鉴pansy中`station->worker`之间的交互。
    worker在start_worker的回调中启动一个loop线程，通过queue与主线程交互。queue的get超时与clock的定时器设置相关。
    之后在view函数中将task放到queue中，整个功能就实现了。

    另外如果是与maple配合的话，request就可以不用自定义了，因为传过来的是maple.Task，正好可以减少需要route的cmd数量。

    缺点:

    1. burstctl统计出来pending_tasks不再真实，因为worker会不停的接收，实际阻塞的queue是worker与loop线程之间的queue。
    2. task处理函数不是在主线程，不过这个还好

### 七. TODO

1. ~~支持修改worker数量后，优雅重启worker. 目前可行方案是通过burst ctl，但是ctl是连接到了proxy，貌似还不行~~
2. ~~考虑group_conf和group_router怎么更好的热加载~~
3. ~~考虑是不是要支持udp，似乎没法直接支持。其实调用方可以直接在前面建一个udp代理server即可~~
4. ~~怎样在刚开始启动的时候，不报connect fail的错误~~
5. ~~client.timeout配置~~
6. ~~burstctl支持clear某个group的消息~~
