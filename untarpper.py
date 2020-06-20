import coloredlogs
import logging
import os
import pickle
import subprocess
import queue
import threading


def untar_file():
    while True:
        file_path, file = q.get()
        file_name_no_extension, file_extension = os.path.splitext(file)
        os.makedirs(os.path.join('untarred', file_name_no_extension), exist_ok=True)
        p = subprocess.run([
            'tar',
            '-xf', file_path,
            '-C', os.path.join('untarred', file_name_no_extension)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.stdout, p.stderr
        if out:
            logging.info(f'message: {file_path} -- {out}')
        elif err:
            logging.error(f'failed: {file_path} -- {err}')
            failed_files.write(file_path + '\n')
        else:
            logging.info(f'untarred: {file_path}')
            untarred.add(file_path)
        q.task_done()


if __name__ == '__main__':
    coloredlogs.install()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    q = queue.Queue()
    failed_files = open('untarred_failed.txt', 'w')
    for i in range(10):
        threading.Thread(target=untar_file, daemon=True).start()
    try:
        with open('untarred.pkl', 'rb') as f:
            untarred = pickle.load(f)
    except FileNotFoundError:
        untarred = set()
    path = 'downloads'
    for file in os.listdir('downloads'):
        if file.endswith('.tar'):
            file_path = os.path.join(path, file)
            if file_path in untarred:
                continue
            q.put((file_path, file))
    q.join()

    print(untarred)
    with open('untarred.pkl', 'wb') as f:
        pickle.dump(untarred, f)
    failed_files.close()
