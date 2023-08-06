import os
import time
import queue
from pyglet.clock import Clock
import _thread

from ..share import constants
from ..share.log import logger
from .connection import Connection
from .request import Request
from ..share.task import Task
from ..proto.pansy_pb2 import RspToUsers, CloseUsers


class Worker:
    connection_class = Connection
    request_class = Request

    station = None
    room_id = None

    conn = None
    # 业务可以通过clock来设置schedule
    clock = None

    # 工作进展
    _work_progress = None
    _got_first_request = False
    _task_queue = None

    def __init__(self, station, room_id):
        self.station = station
        self.room_id = room_id

        self._task_queue = queue.Queue(self.app.tasks_max_size)

        self.conn = self.connection_class(
            self,
            (self.app.host, self.app.port),
            self.app.conn_timeout
        )

        self.clock = Clock()

    def run(self):

        self.on_start()

        # daemon==True，主线程不需要等待网络线程结束
        _thread.start_new_thread(self.conn.run, ())
        _thread.start_new_thread(self._monitor_work_timeout, ())

        while self.enabled:
            try:
                self._handle()
            except:
                logger.error('exc occur. worker: %s', self, exc_info=True)

        self.on_stop()

    def _handle(self):
        """
        主循环，等待网络消息，并进行处理
        """
        # 允许idle
        sleep_time = self.clock.get_sleep_time(True)
        # sleep_time is None 说明没有需要处理的，直接永久阻塞等待即可
        # 否则就要使用指定时间阻塞等待
        task_list = []
        # 第一个get要block
        block = True
        while True:
            try:
                task_list.append(
                    self._task_queue.get(block=block, timeout=sleep_time)
                )
            except queue.Empty:
                # 说明已经没有了
                break
            except:
                # 说明出问题了
                logger.error('exc occur. worker: %s', self, exc_info=True)
                break
            finally:
                block = False

        for task in task_list:
            if task is None:
                # 通过传入None来中断block
                continue

            request = self.request_class(self, task)
            # 设置task开始处理的时间和信息
            self._work_progress = dict(
                begin_time=time.perf_counter(),
                request=request,
            )

            self._handle_request(request)

            self._work_progress = None

        self.clock.tick(True)

    def _handle_request(self, request):
        """
        出现任何异常的时候，服务器不再主动关闭连接
        """
        if not request.is_valid:
            return False

        if request.task.cmd != constants.CMD_CLIENT_CLOSED and not request.view_func:
            logger.info('cmd invalid. request: %s' % request)
            return False

        if not self._got_first_request:
            self._got_first_request = True
            self.app.events.before_first_request(request)
            for bp in self.app.blueprints:
                bp.events.before_app_first_request(request)

        self.app.events.before_request(request)
        for bp in self.app.blueprints:
            bp.events.before_app_request(request)
        if request.blueprint:
            request.blueprint.events.before_request(request)

        if request.interrupted:
            # 业务要求中断
            return True

        view_func_exc = None

        if request.task.cmd == constants.CMD_CLIENT_CLOSED:
            self.app.events.close_client(request)
            for bp in self.app.blueprints:
                bp.events.close_app_client(request)
        else:
            try:
                request.view_func(request)
            except Exception as e:
                logger.error('view_func raise exception. e: %s, request: %s', e, request, exc_info=True)
                view_func_exc = e

        if request.blueprint:
            request.blueprint.events.after_request(request, view_func_exc)
        for bp in self.app.blueprints:
            bp.events.after_app_request(request, view_func_exc)
        self.app.events.after_request(request, view_func_exc)

        return True

    def _monitor_work_timeout(self):
        """
        监控task的耗时
        :return:
        """

        while True:
            time.sleep(1)

            work_progress = self._work_progress
            if work_progress:
                past_time = time.perf_counter() - work_progress['begin_time']
                if self.app.work_timeout is not None and past_time > self.app.work_timeout:
                    # 说明worker的处理时间已经太长了
                    logger.fatal('work timeout: %s / %s, request: %s',
                                 past_time, self.app.work_timeout, work_progress['request'])
                    # 不能这么做啊，直接把其他room也杀掉了，就打印一下告警算了
                    # 强制从子线程退出整个进程
                    # os._exit(-1)

    def push_task(self, task):
        """
        加入task，不阻塞
        return:
            True: 成功
            False: 失败
        """
        try:
            self._task_queue.put_nowait(task)
            return True
        except:
            logger.error('exc occur. worker: %s, task: %s', self, task, exc_info=True)
            return False

    @property
    def app(self):
        return self.station.app

    @property
    def enabled(self):
        return self.station.enabled

    def on_start(self):
        """
        当worker启动后
        可继承实现
        :return:
        """
        self.app.events.start_worker(self)
        for bp in self.app.blueprints:
            bp.events.start_app_worker(self)

    def on_stop(self):
        """
        当worker停止前
        可继承实现
        :return:
        """
        for bp in self.app.blueprints:
            bp.events.stop_app_worker(self)
        self.app.events.stop_worker(self)

    def write_to_members(self, data):
        if isinstance(data, self.app.box_class):
            data = data.pack()
        elif isinstance(data, dict):
            data = self.app.box_class(data).pack()

        task = Task()
        task.cmd = constants.CMD_WRITE_TO_MEMBERS
        task.body = data

        return self.conn.write(task.pack())

    def write_to_users(self, data_list):
        """
        格式为
        [(uids, box), (uids, box), (uids, box) ...]
        :param data_list:
        :return:
        """

        msg = RspToUsers()

        for uids, data in data_list:
            if isinstance(data, self.app.box_class):
                data = data.pack()
            elif isinstance(data, dict):
                data = self.app.box_class(data).pack()

            row = msg.rows.add()
            row.buf = data
            row.uids.extend(uids)

        task = Task()
        task.cmd = constants.CMD_WRITE_TO_USERS
        task.body = msg.SerializeToString()

        return self.conn.write(task.pack())

    def close_members(self):
        task = Task()
        task.cmd = constants.CMD_CLOSE_MEMBERS

        return self.conn.write(task.pack())

    def close_users(self, uids):
        msg = CloseUsers()
        msg.uids.extend(uids)

        task = Task()
        task.cmd = constants.CMD_CLOSE_USERS
        task.body = msg.SerializeToString()

        return self.conn.write(task.pack())

    def __repr__(self):
        return '<%s name: %s, room_id: %r>' % (
            type(self).__name__, self.app.name, self.room_id
        )

