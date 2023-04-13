#!/usr/bin/env python3
# @author      Markus Kösters

import threading
import multiprocessing
import psutil

from Configurations import ConfigReader


class ThreadProcessManager:
    instance = None
    runningThreads = []
    runningProcesses = {}

    def __new__(cls):
        """Making sure that the class is only being instanced once"""
        if not cls.instance:
            cls.instance = super(ThreadProcessManager, cls).__new__(cls)
        return cls.instance

    def startInNewThread(self, object_, name, runContinuously=False, waitThreadFinished=False):
        if runContinuously:
            stopThread = False
            thread_ = threading.Thread(target=self.__runThreadContinuously, name=f'{name}_Thread', args=(lambda stopThread: stopThread,), daemon=True)
            self.runningThreads.append([thread_, stopThread])
        else:
            thread_ = threading.Thread(target=object_, name=f'{name}_Thread', daemon=True)
        thread_.start()
        return thread_

    def __runThreadContinuously(self, object_: object, stopThread):
        """Running the thread-activities until stopThread <bool> is True"""
        while not stopThread():
            object_()
        return

    def startInNewProcess(self, object, name, args: tuple = None):
        """Start object as new process"""
        process_ = multiprocessing.Process(target=object, args=args, name=f'{name}_Process', daemon=True)
        process_.start()
        return process_

    def __exit__(self):
        """Kills all threads and processes on program-leave"""
        self.__killAllProcesses()

    def killAllThreads(self):
        """Setting the run-variables <bool> of the lambda-function inside the thread-function to True, which causes the loop to stop"""
        for runningThread in self.runningThreads:
            if runningThread[0].isAlive():
                runningThread[1] = True

    @staticmethod
    def __killAllProcesses():
        """Kills all processes and child-processes"""
        # iterating through existing processes
        for process_ in psutil.process_iter():
            pid = process_.pid
            parent = psutil.Process(pid)
            # iterating through child-processes
            for child in parent.children(recursive=True):
                child.kill()
            # killing parent if pid still exists
            if psutil.pid_exists(pid):
                parent.kill()


