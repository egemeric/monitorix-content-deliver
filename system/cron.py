import threading
from time import time, sleep


class Cron(threading.Thread):
    def __init__(self, job, everyn):
        threading.Thread.__init__(self)
        self.everyn = everyn
        self.job = job
        self.job.start()

    def run(self):
        while(True):
            if(self.job.is_alive()):
                sleep(1)
            else:
                print("DO CRON")
                self.job.run()
                sleep(self.everyn)
