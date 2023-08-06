import os
import socket
import time
import _thread
from netkit.contrib.tcp_client import TcpClient
from ...share import constants
from ...share.log import logger


class Connection(object):

    worker = None
    client = None

    _work_progress = None

    def __init__(self, worker, address, conn_timeout):
        self.worker = worker
        # 直接创建即可
        self.client = TcpClient(self.app.task_class, address=address, timeout=conn_timeout)

    def run(self):
        _thread.start_new_thread(self._monitor_work_timeout, ())
        while self.worker.enabled:
            try:
                self._handle()
            except:
                logger.error('exc occur. worker: %s', self.worker, exc_info=True)

    @property
    def app(self):
        return self.worker.app

    def _monitor_work_timeout(self):
        """
        监控work超时
        :return:
        """

        # 之所以使用True而不是self.worker.enabled
        # 假设worker处理进入了死循环，而此时调用了kill -hup master
        # 就会导致 self.worker.enabled 为False，从而无法再检测worker处理超时，也无法再reload
        while True:
            time.sleep(1)

            work_progress = self._work_progress
            if work_progress:
                past_time = time.perf_counter() - work_progress['begin_time']
                if self.app.work_timeout is not None and past_time > self.app.work_timeout:
                    # 说明worker的处理时间已经太长了
                    logger.error('work timeout: %s / %s, request: %s',
                                 past_time, self.app.work_timeout, work_progress['request'])
                    # 强制从子线程退出worker
                    os._exit(-1)

    def _handle(self):
        while self.worker.enabled and self.closed():
            if not self._connect():
                logger.error('connect fail. worker: %s, address: %s, sleep %ss',
                             self.worker, self.client.address, constants.RECONNECT_INTERVAL)
                time.sleep(constants.RECONNECT_INTERVAL)

        if not self.worker.enabled:
            # 安全退出
            return

        # 跟gateway要task
        self._ask_for_task()
        self._read_message()

    def _ask_for_task(self):
        task = self.app.task_class()
        task.cmd = constants.CMD_WORKER_ASK_FOR_TASK

        return self.write(task.pack())

    def _connect(self):
        try:
            self.client.connect()
        except:
            logger.error('exc occur. worker: %s', self.worker, exc_info=True)
            return False
        else:
            self.app.events.open_conn(self)
            for bp in self.app.blueprints:
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
        self.app.events.before_response(self, data)
        for bp in self.app.blueprints:
            bp.events.before_app_response(self, data)

        ret = self.client.write(data)
        if not ret:
            logger.error('connection write fail. worker: %s, data: %r', self.worker, data)

        for bp in self.app.blueprints:
            bp.events.after_app_response(self, data, ret)
        self.app.events.after_response(self, data, ret)

        return ret

    def _read_message(self):
        req_task = None

        while 1:
            try:
                # 读取数据 task
                req_task = self.client.read()
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

        if req_task:
            self._on_read_complete(req_task)

        if self.closed():
            self._on_connection_close()

    def _on_connection_close(self):
        # 链接被关闭的回调

        logger.error('connection closed. worker: %s, address: %s', self.worker, self.client.address)

        for bp in self.app.blueprints:
            bp.events.close_app_conn(self)
        self.app.events.close_conn(self)

    def _on_read_complete(self, data):
        """
        数据获取结束
        """
        request = self.app.request_class(self, data)

        # 设置task开始处理的时间和信息
        self._work_progress = dict(
            begin_time=time.perf_counter(),
            request=request,
        )
        self._handle_request(request)
        self._work_progress = None

    def _handle_request(self, request):
        """
        出现任何异常的时候，服务器不再主动关闭连接
        """

        if not request.is_valid:
            return False

        # 如果是view，但是又没有对应的view_func，就要报错，并且不触发任何事件
        if request.task.cmd not in (constants.CMD_CLIENT_CREATED, constants.CMD_CLIENT_CLOSED) \
                and not request.view_func:

            logger.info('cmd invalid. request: %s' % request)
            if not request.responded:
                request.write_to_client(dict(ret=constants.RET_INVALID_CMD))
            return False

        if not self.worker.got_first_request:
            self.worker.got_first_request = True
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

        if request.task.cmd == constants.CMD_CLIENT_CREATED:
            self.app.events.create_client(request)
            for bp in self.app.blueprints:
                bp.events.create_app_client(request)
        elif request.task.cmd == constants.CMD_CLIENT_CLOSED:
            self.app.events.close_client(request)
            for bp in self.app.blueprints:
                bp.events.close_app_client(request)
        else:
            try:
                request.view_func(request)
            except Exception as e:
                logger.error('view_func raise exception. e: %s, request: %s',
                             e, request, exc_info=True)
                view_func_exc = e
                # 必须是没有回应过
                if not request.responded:
                    request.write_to_client(dict(ret=constants.RET_INTERNAL))

        if request.blueprint:
            request.blueprint.events.after_request(request, view_func_exc)
        for bp in self.app.blueprints:
            bp.events.after_app_request(request, view_func_exc)
        self.app.events.after_request(request, view_func_exc)

        return True

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

    def shutdown(self, how=2):
        return self.client.shutdown(how)
