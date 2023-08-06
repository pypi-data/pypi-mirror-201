
import signal
import setproctitle
import os

from .connection import Connection
from ..share.log import logger
from ..share import constants
from ..share.utils import safe_call


class Worker(object):

    type = constants.PROC_TYPE_WORKER

    connection_class = Connection

    group_id = None

    # 是否有效(父进程中代表程序有效，子进程中代表worker是否有效)
    enabled = True

    conn = None

    got_first_request = False

    def __init__(self, app, group_id):
        """
        构造函数
        :return:
        """
        self.app = app
        self.group_id = group_id

    def run(self):
        setproctitle.setproctitle(self.app.make_proc_name(
            '%s:%s' % (self.type, self.group_id)
        ))

        self._handle_proc_signals()
        self._on_start()

        try:
            address = os.path.join(
                self.app.config['IPC_ADDRESS_DIRECTORY'],
                self.app.config['WORKER_ADDRESS_TPL'] % self.group_id
            )
            self.conn = self.connection_class(self, address, self.app.config['WORKER_CONN_TIMEOUT'])
            self.conn.run()
        except:
            logger.error('exc occur. worker: %s', self, exc_info=True)
        finally:
            self._on_stop()

    def _on_start(self):
        self.app.events.start_worker(self)
        for bp in self.app.blueprints:
            bp.events.start_app_worker(self)

    def _on_stop(self):
        for bp in self.app.blueprints:
            bp.events.stop_app_worker(self)
        self.app.events.stop_worker(self)

    def _handle_proc_signals(self):
        def safe_stop_handler(signum, frame):
            self.enabled = False

            # 关闭读，从而快速退出
            safe_call(lambda: self.conn.shutdown(0))

        # 安全停止
        signal.signal(signal.SIGTERM, safe_stop_handler)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

    def __repr__(self):
        return '<%s name: %s, group_id: %r>' % (
            type(self).__name__, self.app.name, self.group_id
        )
