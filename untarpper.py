import coloredlogs
import logging
import os
import pickle
import subprocess

if __name__ == '__main__':
    coloredlogs.install()
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    processes = []
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
            file_name_no_extension, file_extension = os.path.splitext(file)
            os.makedirs(os.path.join('untarred', file_name_no_extension), exist_ok=True)
            processes.append(
                (
                    file_path,
                    subprocess.Popen(
                        [
                            'tar',
                            '-xf', os.path.join(path, file),
                            '-C', os.path.join('untarred', file_name_no_extension)
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                )
            )
            untarred.add(file_path)
    for file_path, process in processes:
        process.wait()
        out, err = process.communicate()
        if out:
            logging.info(f'message: {file_path} -- {out}')
        if err:
            logging.error(f'failed: {file_path} -- {err}')

    with open('untarred.pkl', 'wb') as f:
        pickle.dump(untarred, f)

