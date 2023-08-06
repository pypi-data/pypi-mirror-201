import socket
import time
from netkit.contrib.tcp_client import TcpClient

from ..share import constants
from ..share.log import logger
from ..share.task import Task


class Connection(object):

    def __init__(self, worker, address, conn_timeout):
        self.worker = worker
        # 直接创建即可
        self.client = TcpClient(Task, address=address, timeout=conn_timeout)

    def run(self):
        while self.worker.enabled:
            try:
                self._handle()
            except:
                logger.error('exc occur. worker: %s',
                             self.worker, exc_info=True)

    def _handle(self):
        while self.worker.enabled and self.closed():
            if not self._connect():
                logger.error('connect fail. worker: %s, address: %s, sleep %ss',
                             self.worker, self.client.address, self.worker.app.reconnect_interval)
                time.sleep(self.worker.app.reconnect_interval)
            else:
                # 只在连接建立成功时，跟gateway要task
                self._ask_for_task()

        if not self.worker.enabled:
            # 安全退出
            return

        self._read_message()

    def _ask_for_task(self):
        task = Task()
        task.cmd = constants.CMD_WORKER_ASK_FOR_TASK
        task.room_id = self.worker.room_id

        return self.write(task.pack())

    def _connect(self):
        try:
            self.client.connect()
        except:
            logger.error('exc occur. worker: %s', self.worker, exc_info=True)
            return False
        else:
            self.worker.app.events.open_conn(self)
            for bp in self.worker.app.blueprints:
                bp.events.open_app_conn(self)

            return True

    def write(self, data):
        """
        发送数据    True: 成功   else: 失败
        """
        if self.client.closed():
            logger.error('connection closed. worker: %s, data: %r', self.worker, data)
            return False

        # 只支持字符串
        self.worker.app.events.before_response(self, data)
        for bp in self.worker.app.blueprints:
            bp.events.before_app_response(self, data)

        ret = self.client.write(data)
        if not ret:
            logger.error('connection write fail. worker: %s, data: %r', self.worker, data)

        for bp in self.worker.app.blueprints:
            bp.events.after_app_response(self, data, ret)
        self.worker.app.events.after_response(self, data, ret)

        return ret

    def _read_message(self):
        task = None

        while 1:
            try:
                # 读取数据 gw_box
                task = self.client.read()
            except socket.timeout:
                # 超时了
                if not self.worker.enabled:
                    return
                else:
                    # 继续读
                    continue
            else:
                # 正常收到数据了
                break

        if task:
            self._on_read_complete(task)

        if self.closed():
            self._on_connection_close()

    def _on_connection_close(self):
        # 链接被关闭的回调

        logger.error('connection closed. worker: %s, address: %s', self.worker, self.client.address)

        for bp in self.worker.app.blueprints:
            bp.events.close_app_conn(self)
        self.worker.app.events.close_conn(self)

    def _on_read_complete(self, task):
        """
        数据获取结束
        """
        self.worker.push_task(task)

    def close(self):
        """
        直接关闭连接
        """
        self.client.close()

    def closed(self):
        """
        连接是否已经关闭
        :return:
        """
        return self.client.closed()

