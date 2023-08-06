import _thread
import multiprocessing
import signal
import time
import setproctitle

from ..share import constants


class Loader:
    type = constants.PROC_TYPE_LOADER

    app = None

    worker_processes = None

    enabled = True

    def __init__(self, app):
        self.app = app
        self.worker_processes = list()

    def run(self):
        setproctitle.setproctitle(self.app.make_proc_name(self.type))
        self._handle_signals()

        self._spawn_workers()

        self._monitor_workers()

    def _create_worker(self, group_id):
        process = multiprocessing.Process(
            target=self.app.worker_class(self.app, group_id).run,
        )
        # master不可以独自退出
        process.daemon = False
        process.init_params = dict(
            group_id=group_id,
        )

        process.start()

        return process

    def _spawn_workers(self):
        """
        监控进程
        :return:
        """
        for group in self.app.group_list:
            group_id = group['id']
            for it in range(group['count']):
                self.worker_processes.append(self._create_worker(
                    group_id,
                ))

    def _monitor_workers(self):
        while True:
            for idx, process in enumerate(self.worker_processes):
                if process and not process.is_alive():
                    self.worker_processes[idx] = None

                    if self.enabled:
                        # 需要重启启动process
                        self.worker_processes[idx] = self._create_worker(**process.init_params)

            if not self.enabled and not any(self.worker_processes):
                # 可以彻底停掉了
                break

            time.sleep(0.1)

    def _stop_all(self):
        """
        等所有子进程结束，父进程也退出
        """

        def kill_processes_later(processes, timeout):
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
                    if p and p.is_alive():
                        # 说明进程还活着
                        p.kill()

            _thread.start_new_thread(_kill_processes, ())

        self.enabled = False

        # 一定要这样，否则后面kill的时候可能会kill错
        processes = self.worker_processes[:]

        # 如果是终端直接CTRL-C，子进程自然会在父进程之后收到INT信号，不需要再写代码发送
        # 如果直接kill -INT $parent_pid，子进程不会自动收到INT
        # 所以这里可能会导致重复发送的问题，重复发送会导致一些子进程异常，所以在子进程内部有做重复处理判断。
        for p in processes:
            if p:
                p.terminate()

        if self.app.config['STOP_TIMEOUT'] is not None:
            kill_processes_later(processes, self.app.config['STOP_TIMEOUT'])

    def _handle_signals(self):

        def stop_handler(signum, frame):
            """
            等所有子进程结束，父进程也退出
            """
            self._stop_all()

        # TERM为安全结束
        signal.signal(signal.SIGTERM, stop_handler)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        # 热重启
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

    def __repr__(self):
        return '<%s name: %s>' % (
            type(self).__name__, self.app.name
        )
