from ...share.log import logger
from ...share import constants
from ...share.proto.maple_pb2 import RspToUsers, CloseUsers


class Request(object):
    """
    请求
    """

    # 与gateway的连接对象
    conn = None
    # gateway封装的box
    task = None
    # 业务box
    box = None
    # 数据是否有效
    is_valid = False
    # 是否已经作出回应
    responded = False
    # 路由表
    route_rule = None
    # 是否中断处理，即不调用view_func，主要用在before_request中
    interrupted = False

    def __init__(self, conn, task):
        self.conn = conn
        self.task = task
        # 赋值
        self.is_valid = self._parse_raw_data()

    @property
    def worker(self):
        return self.conn.worker

    @property
    def app(self):
        return self.worker.app

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

    def write_to_client(self, data):
        """
        写回
        :param data: 可以是dict也可以是box
        :return:
        """

        assert not (self.app.rsp_once and self.responded), 'request has been responded'

        if isinstance(data, self.app.box_class):
            data = data.pack()
        elif isinstance(data, dict):
            data = self.box.map(data).pack()

        task = self.task.map(dict(
            cmd=constants.CMD_WRITE_TO_CLIENT,
            body=data,
        ))

        succ = self.conn.write(task.pack())

        if succ:
            # 如果发送成功，就标记为已经回应
            self.responded = True

        return succ

    def write_to_users(self, data_list):
        """
        格式为
        [(uids, box), (uids, box, userdata), (uids, box, userdata, exclude) ...]
        :param data_list: userdata可不传，默认为0，conn.userdata & userdata == userdata; exclude 代表排除的uid列表
        :return:
        """

        msg = RspToUsers()

        for data_tuple in data_list:
            tmp_len = len(data_tuple)
            if tmp_len == 2:
                uids, data = data_tuple
                userdata = None
                exclude = None
            elif tmp_len == 3:
                uids, data, userdata = data_tuple
                exclude = None
            else:
                uids, data, userdata, exclude = data_tuple

            if isinstance(data, self.app.box_class):
                data = data.pack()
            elif isinstance(data, dict):
                data = self.app.box_class(data).pack()

            row = msg.rows.add()
            row.buf = data
            row.userdata = userdata or 0
            row.uids.extend(uids)
            if exclude:
                row.exclude.extend(exclude)

        task = self.app.task_class()
        task.cmd = constants.CMD_WRITE_TO_USERS
        task.body = msg.SerializeToString()

        return self.conn.write(task.pack())

    def close_client(self):
        task = self.task.map(dict(
            cmd=constants.CMD_CLOSE_CLIENT,
        ))

        return self.conn.write(task.pack())

    def close_users(self, uids, userdata=None, exclude=None):
        msg = CloseUsers()
        msg.uids.extend(uids)
        msg.userdata = userdata or 0
        if exclude:
            msg.exclude.extend(exclude)

        task = self.app.task_class()
        task.cmd = constants.CMD_CLOSE_USERS
        task.body = msg.SerializeToString()

        return self.conn.write(task.pack())

    def login_client(self, uid, userdata=None):
        task = self.task.map(dict(
            cmd=constants.CMD_LOGIN_CLIENT,
            uid=uid,
            userdata=userdata or 0,
        ))

        return self.conn.write(task.pack())

    def logout_client(self):
        task = self.task.map(dict(
            cmd=constants.CMD_LOGOUT_CLIENT,
        ))

        return self.conn.write(task.pack())

    def write_to_worker(self, data, params=None):
        """
        透传到worker进行处理
        :param params 指定task的参数, dict类型
        """

        task = self.app.task_class()
        task.cmd = constants.CMD_WRITE_TO_WORKER

        if params:
            for k, v in params.items():
                setattr(task, k, v)

        if isinstance(data, self.app.box_class):
            # 打包
            data = data.pack()
        elif isinstance(data, dict):
            data = self.app.box_class(data).pack()

        task.body = data

        return self.conn.write(task.pack())

    def clear_client_tasks(self):
        """
        清空客户端对应的所有任务
        :return:
        """
        task = self.task.map(dict(
            cmd=constants.CMD_CLEAR_CLIENT_TASKS,
        ))

        return self.conn.write(task.pack())

    def interrupt(self, data=None):
        """
        中断处理
        :param data: 要响应的数据，不传即不响应
        :return:
        """
        self.interrupted = True
        # box有可能为None，在create_client/close_client事件中
        if data is not None and self.box is not None:
            return self.write_to_client(data)
        else:
            return True

    def __repr__(self):
        return '<%s cmd: %r, endpoint: %s, task: %r, worker: %s>' % (
            type(self).__name__, self.cmd, self.endpoint, self.task, self.worker
        )
