from ..share.log import logger


class Request(object):
    """
    请求
    """

    # 业务层需要访问的对象，消息内容
    box = None

    worker = None
    # 封装的task，外面不需要理解
    task = None
    is_valid = False
    route_rule = None
    # 是否中断处理，即不调用view_func，主要用在before_request中
    interrupted = False

    def __init__(self, worker, task):
        self.worker = worker
        self.task = task
        # 赋值
        self.is_valid = self._parse_raw_data()
        # request 也可以直接调用
        self.write_to_members = self.worker.write_to_members
        self.close_members = self.worker.close_members
        self.write_to_users = self.worker.write_to_users
        self.close_users = self.worker.close_users

    def _parse_raw_data(self):
        if not self.task.body:
            return True

        self.box = self.app.box_class()

        if self.box.unpack(self.task.body) > 0:
            self._parse_route_rule()
            return True
        else:
            logger.error('unpack fail. request: %s', self)
            return False

    def _parse_route_rule(self):
        if self.cmd is None:
            return

        self.route_rule = self.app.get_route_rule(self.cmd)

    @property
    def cmd(self):
        return self.box.cmd if self.box else None

    @property
    def view_func(self):
        return self.route_rule['view_func'] if self.route_rule else None

    @property
    def endpoint(self):
        return self.route_rule['endpoint'] if self.route_rule else None

    @property
    def blueprint(self):
        return self.route_rule.get('blueprint') if self.route_rule else None

    @property
    def app(self):
        return self.worker.app

    @property
    def client_ip(self):
        """
        客户端连接IP，外面不需要了解task
        :return:
        """
        return self.task.client_ip

    def interrupt(self):
        """
        中断处理
        """
        self.interrupted = True

    def write_to_client(self, data):
        """
        写回响应
        :param data:
        :return:
        """
        data = data or dict()

        if isinstance(data, dict):
            data.update(
                cmd=self.box.cmd,
                sn=self.box.sn,
            )

        self.write_to_users([
            ([self.task.uid], data)
        ])

    def __repr__(self):
        return '<%s cmd: %r, endpoint: %s, task: %r, worker: %s>' % (
            type(self).__name__, self.cmd, self.endpoint, self.task, self.worker
        )
