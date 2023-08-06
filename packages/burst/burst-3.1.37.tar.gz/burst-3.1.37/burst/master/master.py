
import os
import copy
import json
import sys
import subprocess
import time
import signal
import _thread
import setproctitle
from netkit.box import Box
from netkit.contrib.tcp_client import TcpClient

from ..share.log import logger
from ..share.utils import safe_call
from ..share import constants


class Master(object):
    """
    master相关
    """

    type = constants.PROC_TYPE_MASTER

    app = None

    # 是否有效
    enabled = True

    # 子进程们
    child_processes = None

    def __init__(self, app):
        """
        构造函数
        :return:
        """
        self.app = app
        self.child_processes = dict()

    def run(self):
        setproctitle.setproctitle(self.app.make_proc_name(self.type))

        self._handle_proc_signals()

        proxy = self._spawn_proxy()
        if not proxy:
            # 启动proxy失败，就应该直接返回
            self._stop_all()
            return

        self.child_processes[constants.PROC_TYPE_PROXY] = proxy

        # 等待proxy启动，为了防止worker在连接的时候一直报connect失败的错误
        if not self._wait_proxy():
            # 有可能ctrl-c终止，这个时候就要直接返回了
            self._stop_all()
            return

        loader = self._spawn_loader()
        if not loader:
            # 启动loader失败，就应该直接返回
            self._stop_all()
            return

        self.child_processes[constants.PROC_TYPE_LOADER] = loader

        _thread.start_new_thread(self._connect_to_proxy, ())

        self._monitor_child_processes()

    def _wait_proxy(self):
        """
        尝试连接proxy，如果连接成功，说明proxy启动起来了
        :return:
        """
        address = os.path.join(
            self.app.config['IPC_ADDRESS_DIRECTORY'],
            self.app.config['MASTER_ADDRESS']
        )
        client = TcpClient(Box, address=address)

        while self.enabled:
            try:
                client.connect()
                # 连接成功后，就关闭连接
                client.close()
                return True
            except:
                time.sleep(0.1)
                continue

        return False

    def _connect_to_proxy(self):
        """
        连接到proxy，因为有些命令要发过来
        :return:
        """
        address = os.path.join(
            self.app.config['IPC_ADDRESS_DIRECTORY'],
            self.app.config['MASTER_ADDRESS']
        )
        client = TcpClient(Box, address=address)

        while self.enabled:
            try:
                if client.closed():
                    client.connect()
            except:
                # 只要连接失败
                logger.error('connect fail. master: %s, address: %s', self, address)
                time.sleep(1)
                continue

            # 读取的数据
            box = client.read()
            if not box:
                logger.info('connection closed. master: %s', self)
                continue

            logger.info('box received. master: %s, box: %s', self, box)

            safe_call(self._handle_proxy_data, box)

    def _handle_proxy_data(self, box):
        """
        处理从proxy过来的box
        :param box:
        :return:
        """

        if box.cmd == constants.CMD_ADMIN_RELOAD:
            self._reload_workers()
        elif box.cmd == constants.CMD_ADMIN_STOP:
            self._stop_all()

    def _start_child_process(self, proc_env):
        worker_env = copy.deepcopy(os.environ)
        worker_env.update({
            self.app.config['CHILD_PROCESS_ENV_KEY']: json.dumps(proc_env)
        })

        args = [sys.executable] + sys.argv
        try:
            inner_p = subprocess.Popen(args, env=worker_env)
            inner_p.proc_env = proc_env
            return inner_p
        except:
            logger.error('exc occur. app: %s, args: %s, env: %s',
                         self, args, worker_env, exc_info=True)
            return None

    def _spawn_proxy(self):
        proc_env = dict(
            type=constants.PROC_TYPE_PROXY
        )
        return self._start_child_process(proc_env)

    def _spawn_loader(self):
        proc_env = dict(
            type=constants.PROC_TYPE_LOADER
        )
        return self._start_child_process(proc_env)

    def _monitor_child_processes(self):
        while 1:
            for proc_type, p in self.child_processes.items():

                if p and p.poll() is not None:
                    # 说明退出了
                    proc_env = p.proc_env
                    self.child_processes[proc_type] = None

                    if self.enabled:
                        # 如果还要继续服务
                        p = self._start_child_process(proc_env)
                        self.child_processes[proc_type] = p

            if not any(self.child_processes.values()):
                # 没活着的proxy和worker了
                break

            # 时间短点，退出的快一些
            time.sleep(0.1)

    def _kill_processes_later(self, processes, timeout):
        """
        等待一段时间后杀死所有进程
        :param processes:
        :param timeout:
        :return:
        """
        def _kill_processes():
            # 等待一段时间
            time.sleep(timeout)

            for p in processes:
                if p and p.poll() is None:
                    # 说明进程还活着
                    safe_call(p.send_signal, signal.SIGKILL)

        _thread.start_new_thread(_kill_processes, ())

    def _stop_all(self):
        """
        停止所有进程
        :return:
        """
        self.enabled = False

        processes = list(self.child_processes.values())

        for p in processes:
            if p:
                safe_call(p.send_signal, signal.SIGTERM)

        # 不能使用强制kill的方式，因为loader即使被强制kill，如果worker还在正常运行的话，问题更大

        # if self.app.config['STOP_TIMEOUT'] is not None:
        #    self._kill_processes_later(processes, self.app.config['STOP_TIMEOUT'])

    def _reload_workers(self):
        """
        reload workers
        :return:
        """

        loader = self.child_processes.get(constants.PROC_TYPE_LOADER)
        if loader:
            safe_call(loader.send_signal, signal.SIGTERM)

    def _handle_proc_signals(self):
        def stop_handler(signum, frame):
            """
            等所有子进程结束，父进程也退出
            """
            self._stop_all()

        def reload_handler(signum, frame):
            """
            让所有子进程重新加载
            """
            self._reload_workers()

        # INT为强制结束
        signal.signal(signal.SIGINT, stop_handler)
        # TERM为安全结束
        signal.signal(signal.SIGTERM, stop_handler)
        # HUP为热更新
        signal.signal(signal.SIGHUP, reload_handler)

    def __repr__(self):
        return '<%s name: %s>' % (
            type(self).__name__, self.app.name
        )
