from multiprocessing import Queue

task_queue = Queue()
# rough q_size (work around NotImplementedError)
q_size = 0