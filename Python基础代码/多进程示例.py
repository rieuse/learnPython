from multiprocessing import Process, current_process
import os


def doubler(number):
    """
    A doubling function that can be used by a process
    """
    result = number * 2
    pid = os.getpid()
    proc_name = current_process().name
    print('{0} doubled to {1} by process id: {2},name: {3}'.format(number, result, pid, proc_name))


if __name__ == '__main__':
    numbers = [5, 10, 15, 20, 25, 4, 5, 6, 6, 7, 8, 23, 134, 4, 5, 245, 4, 3, 543, 5, 43543]
    procs = []

    for number in numbers:
        proc = Process(target=doubler, args=(number,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
