import multiprocessing
import time
import os
import subprocess
import sys
import signal
import copy
import _thread

import setproctitle
from ...share.log import logger
from ...share import constants
from ...share.utils import safe_call


class Master:

    app = None

    # 是否有效(父进程中代表程序有效，子进程中代表worker是否有效)
    enabled = True
    # 子进程列表
    processes = None

    def __init__(self, app):
        self.app = app
        self.processes = list()

    def run(self):
        # 设置进程名
        setproctitle.setproctitle(
            self.app.make_proc_name('master')
        )
        self._handle_signals()
        self._spawn_workers()
        self._monitor_workers()

    def _create_worker(self):
        process = multiprocessing.Process(
            target=self.app.worker_class(self.app).run,
        )
        # master不可以独自退出
        process.daemon = False
        process.start()

        return process

    def _spawn_workers(self):
        """
        启动多个worker
        :return:
        """
        for it in range(self.app.workers):
            self.processes.append(self._create_worker())

    def _monitor_workers(self):
        while True:
            for idx, process in enumerate(self.processes):
                if process and not process.is_alive():
                    self.processes[idx] = None

                    if self.enabled:
                        # 需要重启启动process
                        self.processes[idx] = self._create_worker()

            if not self.enabled and not any(self.processes):
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
        processes = self.processes[:]

        # 如果是终端直接CTRL-C，子进程自然会在父进程之后收到INT信号，不需要再写代码发送
        # 如果直接kill -INT $parent_pid，子进程不会自动收到INT
        # 所以这里可能会导致重复发送的问题，重复发送会导致一些子进程异常，所以在子进程内部有做重复处理判断。
        for p in processes:
            if p:
                p.terminate()

        if self.app.stop_timeout is not None:
            kill_processes_later(processes, self.app.stop_timeout)

    def _handle_signals(self):

        def stop_handler(signum, frame):
            """
            等所有子进程结束，父进程也退出
            """
            self._stop_all()

        # TERM/INT 均为安全结束
        signal.signal(signal.SIGINT, stop_handler)
        signal.signal(signal.SIGTERM, stop_handler)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

    def __repr__(self):
        return '<%s name: %s>' % (
            type(self).__name__, self.app.name
        )
