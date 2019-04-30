from sqlalchemy import create_engine
import multiprocessing as mp
from functools import partial

class Poison:
    pass


class Worker:
    def __init__(self, job_queue, result_queue, connection_factory):
        self.__jq = job_queue
        self.__rq = result_queue
        self.__connection_factory = connection_factory

    def __create_connection(self):
        self.__conn = self.__connection_factory()
        self.__cur = self.__conn.cursor()
        return True

    def __get_job(self):
        job = self.__jq.get()
        return job

    def __push_result(self, result):
        self.__rq.put(result)


    def __run_job(self):
        job = self.__get_job()
        if isinstance(job.payload, Poison):
            return False

        result = self.__cur.execute(job.payload).fetchall()
        self.__push_result(result)
        return True

    def start(self):
        self.__create_connection()
        while self.__run_job():
            pass


class Job:
    def __init__(self, pload):
        self.payload = pload

    def isvalid(self):
        return True


def sqlite_factory(info_):
    info ={"path":"/home/giovanni/Documents/flaskApps/fileupload_project/instance/test.sqlite"}
    engine = create_engine("sqlite:///" + info["path"])
    return engine.raw_connection()


def make_qs():
    manager = mp.Manager()
    q, r = manager.Queue(), manager.Queue()
    return q, r, manager


if __name__ == "__main__":
    q, r, m = make_qs()
    w = Worker(q, r, partial(sqlite_factory, {"path":"../../instance/test.sqlite"}))

    for i in range(10):
        q.put(Job("select 1"))
    q.put(Job(Poison()))

    w.start()
