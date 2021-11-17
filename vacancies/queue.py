import logging
from multiprocessing import Process, Queue
logger = logging.getLogger(__name__)
from queue import Empty
from time import sleep


class SendMail:
    def __init__(self):
        self.queue = Queue()
        self.process_active = False

    def process_sent(self, q):
        while True:
            try:
                task = q.get()
                task.send()
                print(task)
                logger.info('Письмо отправлено')
            except q.queue.Empty:
                print('письма закончились')

    def new_send_email(self, email):
        if not self.process_active:
            process = []
            for _ in range(4):
                process.append(Process(target=self.process_sent, args=(self.queue,), daemon=True))
                process[-1].start()
            self.process_active = True
            logger.info('Процессы Созданы')
        self.queue.put(email)
