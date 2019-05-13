import scholar.EIpart as ei
import scholar.Web_of_knowledge as wok
import scholar.Google as Google
import threading
from queue import Queue


class SpiderPool:
    # from multiprocessing import Pool
    def __init__(self, func, args, thread_num=10, call_back_result=[]):
        self.work_queue = Queue()
        self.result_queue = call_back_result
        self.threads = []
        self.__init_work_queue(func, args)
        self.__init_thread_pool(thread_num)

    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(PoolWork(self.work_queue, self.result_queue))

    def __init_work_queue(self, func, args):
        for argv in args:
            self.add_job(func, argv)

    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))

    def wait_all_run(self):
        for item in self.threads:
            if item.isAlive():
                item.join()


class PoolWork(threading.Thread):
    def __init__(self, work_queue, result_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                # print(zip(args))
                res = do(args[0][0], args[0][1])
                # print(do, get_url_by_image)
                self.result_queue.append(res)
                self.work_queue.task_done()
            except Exception:
                break


result_pool = []


def spider_pool_run(url_1):
    essay_list = Google.get_info_from_google(url_1)
    Max_pool1 = SpiderPool(wok.parse_webofknowledge, essay_list, call_back_result=result_pool)
    Max_pool2 = SpiderPool(ei.get_ei_info, essay_list, call_back_result=result_pool)
    Max_pool1.wait_all_run()
    Max_pool2.wait_all_run()
    print(result_pool)

