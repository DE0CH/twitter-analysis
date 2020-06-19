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
            os.makedirs(os.path.join('untarred', file_name_no_extension), exist_ok=True)
            processes.append(subprocess.Popen(
                ['tar', '-xf', os.path.join(path, file), '-C', os.path.join('untarred', file_name_no_extension)]))
            untarred.add(file_path)
    for process in processes:
        process.wait()
    with open('untarred.pkl', 'wb') as f:
        pickle.dump(untarred, f)

