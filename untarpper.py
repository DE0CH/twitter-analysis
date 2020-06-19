import subprocess
import pickle
import os
if __name__ == '__main__':
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
            subprocess.run(['mkdir', file_name_no_extension], cwd=path)
            processes.append(subprocess.Popen(['tar', '-xf', file, '-C', file_name_no_extension], cwd='untarred'))
            untarred.add(file_path)
    [process.wait() for process in processes]
    with open('untarred.pkl', 'wb') as f:
        pickle.dump(untarred, f)

