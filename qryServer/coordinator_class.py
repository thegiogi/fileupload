import multiprocessing as mp
from worker_class import Worker, sqlite_factory, Job, Poison
from functools import partial
from time import sleep

class coordinator:
    def __init__(self, mgr):
        self.__mgr = mgr

    def __make_qs(self):

        jobq, resq = self.__mgr.Queue(), self.__mgr.Queue()
        return jobq, resq

    def setup(self):
        self.__worker_list = []
        self.ps = []

    def worker_factory(self, connection_factory):
        def factory(q,r):
            w = Worker(q, r, connection_factory)
            w.start()
            return True
        return factory

    def start_worker(self, connection_factory):
        self.ps.append(mp.Process(target = self.worker_factory(connection_factory), args = self.__make_qs()))
        self.ps[-1].start()
        self.ps[-1].join()

class Batch:
    def __init__(self, connection_factory, jobs=None):
        self.jobs = jobs if jobs != None else []
        self.connection_factory = connection_factory

    def append(self, j):
        self.jobs.append(j)


if __name__ == "__main__":

    b = Batch(partial(sqlite_factory, {"path":"/home/giovanni/Documents/flaskApps/fileupload_project/instance/test.sqlite"}))
    for i in range(10):
        b.append(Job("select current_timestamp"))
    b.append(Job(Poison()))
    m = mp.Manager()
    c = coordinator(m)
    c.setup()
    c.start_worker(b.connection_factory)
