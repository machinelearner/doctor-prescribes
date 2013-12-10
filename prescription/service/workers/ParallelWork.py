class ParallelWork():
    def __init__(self, worker_type, worker_args, number_of_processes=5):
        self.worker_args = worker_args
        self.worker = worker_type
        self.number_of_processes = number_of_processes

    def begin(self):
        for process in range(self.number_of_processes):
            self.worker(*self.worker_args).start()