from flask import session
import time
import os
import sys
from multiprocessing import Queue
from src.shared import WORKER_ADDRESSES
from src.interface import *
from global_setting import q_size, task_queue

CAPACITY = 100
writefile = "../tmp/tasks.txt"

# called by web interface
def add_to_queue(filename):
    global q_size
    global task_queue
    if q_size >= CAPACITY:
        flush(filename)
    else:
        to_read = CAPACITY - q_size
        if os.path.exists(writefile):
            # there are waiting tasks that were submitted earlier than the current one
            file_obj = open(writefile, 'r')
            lines = file_obj.readlines()
            for i in range(to_read):
                if len(lines) == 0:
                    break
                task_queue.put(lines[0].strip())
                q_size += 1
                print("add to queue ", q_size)
                lines.pop(0)
            file_obj.close()
            # remove tasks added to the queue
            if len(lines) > 0:
                write_obj = open(writefile, 'w')
                write_obj.writelines(lines)
                write_obj.close()
            else:
                os.remove(writefile)
            # handle the current task
            add_to_queue(filename)
        else:
            # no task with higher priority, add to the queue
            task_queue.put(filename)
            q_size += 1
            print("add to queue ", q_size)

# if task_queue reaches it max capacity, flush future tasks to plaintext file
def flush(filename):
    file_obj = open(writefile, 'a')
    file_obj.write(filename+'\n')
    file_obj.close()

def find_result(filename):
    if session.get(filename):
        result = session[filename]
        session.pop(filename)
        return result
    else:
        time.sleep(2)
        find_result(filename)
    
def assign_tasks():
    global q_size, task_queue
    task_queue_copy = task_queue
    task_queue = Queue()
    q_size = 0
    return
    while task_queue_copy.qsize() > 0:
        task = task_queue_copy.get()
        # check what workers are idle / pick the one with min load, assign task to it
        picked_worker = check_load()
        while picked_worker is None:
            time.sleep(1)
            picked_worker = check_load()
        result = image_recognition_with_worker(picked_worker, task)
        session[task] = result
        #TODO: how to return the result to the correct process, by id?


def check_load():
    min_num_tasks = sys.maxsize
    picked_worker = None
    for worker_addr in WORKER_ADDRESSES:
        num_tasks = get_worker_task_num(worker_addr)
        if num_tasks is None:
            continue
        elif num_tasks < min_num_tasks:
            min_num_tasks = num_tasks
            picked_worker = worker_addr
    return picked_worker

# check waiting tasks
def check_waiting():
    global q_size, task_queue
    if task_queue.empty():
        time.sleep(2)
        check_waiting()
    else:
        print("assign tasks")
        assign_tasks()
        check_waiting()

def main():
    print("Manager starts")
    # check if there are waiting tasks
    check_waiting()

if __name__ == '__main__':
    main()