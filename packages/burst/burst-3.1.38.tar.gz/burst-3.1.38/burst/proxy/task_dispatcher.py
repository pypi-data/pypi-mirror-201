
from collections import defaultdict

from ..share import constants
from ..share.log import logger
from .group_queue import GroupQueue


class TaskDispatcher(object):
    """
    任务管理
    主要包括: 消息来了之后的分发
    """

    proxy = None

    # 之所以不用WeakSet的原因是，经过测试worker断掉之后，对象不会立即被删除，极有有可能会被用到。
    # 繁忙worker列表
    busy_workers_dict = None
    # 空闲
    idle_workers_dict = None
    # 消息队列
    group_queue = None

    def __init__(self, proxy):
        self.busy_workers_dict = defaultdict(set)
        self.idle_workers_dict = defaultdict(set)

        self.proxy = proxy
        self.group_queue = GroupQueue(self.proxy.app.config['PROXY_MSG_QUEUE_MAX_SIZE'])

    def remove_worker(self, worker):
        """
        删除worker，一般是worker断掉了
        :param worker:
        :return:
        """
        if worker in self.busy_workers_dict[worker.group_id]:
            self.busy_workers_dict[worker.group_id].remove(worker)

        elif worker in self.idle_workers_dict[worker.group_id]:
            self.idle_workers_dict[worker.group_id].remove(worker)

    def add_task(self, group_id, item):
        """
        添加任务
        当新消息来得时候，应该先检查有没有空闲的worker，如果没有的话，才放入消息队列
        :return:
        """
        idle_workers = self.idle_workers_dict[group_id]
        if not idle_workers:
            if not self.group_queue.put(group_id, item):
                logger.error('put item fail. group_id: %s, queue_size: %s / %s',
                             group_id, self.group_queue.qsize(group_id), self.group_queue.max_size)
                self.proxy.stat_counter.add_discard_task(group_id)
            return

        # 弹出一个可用的worker
        worker = idle_workers.pop()
        # 变成处理中
        worker.status = constants.WORKER_STATUS_BUSY
        # 放到队列中去
        self.busy_workers_dict[group_id].add(worker)

        # 让worker去处理任务吧
        worker.assign_task(item)

    def alloc_task(self, worker):
        """
        尝试获取新任务
        :return: 获取的新任务
        """
        task = self.group_queue.get(worker.group_id)
        dst_status = constants.WORKER_STATUS_BUSY if task else constants.WORKER_STATUS_IDLE

        if worker.status != dst_status:
            # 说明状态有变化，需要调整队列
            worker.status = dst_status
            # 同步状态
            self._sync_worker_status(worker)

        return task

    def clear_tasks(self, group_id):
        """
        清空任务
        :param group_id:
        :return:
        """
        self.group_queue.clear(group_id)

    def clear_all_tasks(self):
        """
        清空所有任务
        :return:
        """
        self.group_queue.clear_all()

    def _sync_worker_status(self, worker):
        """
        内部 同步worker的状态：空闲/繁忙
        此时worker的status，已经自己改过了
        :param worker:
        :return:
        """

        if worker.status == constants.WORKER_STATUS_BUSY:
            src_workers_dict = self.idle_workers_dict
            dst_workers_dict = self.busy_workers_dict
        else:
            src_workers_dict = self.busy_workers_dict
            dst_workers_dict = self.idle_workers_dict

        if worker in src_workers_dict[worker.group_id]:
            # 因为有可能worker的状态是None的话，是不在任何队列里面的，所以先判断一下
            src_workers_dict[worker.group_id].remove(worker)

        dst_workers_dict[worker.group_id].add(worker)
