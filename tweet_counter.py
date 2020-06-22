import os
import json
import multiprocessing


def worker(queue, c):
    while True:
        path, file = queue.get()
        with open(os.path.join(path, file)) as f:
            tweets = json.loads(f.read())
            with c.get_lock():
                c.value += len(tweets)
        queue.task_done()


if __name__ == '__main__':
    q = multiprocessing.JoinableQueue()
    c = multiprocessing.Value('i', 0)
    for i in range(os.cpu_count()-1):
        multiprocessing.Process(target=worker, args=(q, c), daemon=True).start()
    for path, dirs, files in os.walk('processed'):
        for file in files:
            if file.endswith('.json'):
                q.put((path, file))
    q.join()
    print(c.value)

