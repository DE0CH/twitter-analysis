import subprocess
import os
if __name__ == '__main__':
    for path, dirs, files in os.walk('downloads'):
        for file in files:
            file_name_no_extension, file_extension = os.path.splitext(file)
            subprocess.Popen(['mkdir', file_name_no_extension], cwd=path)
            subprocess.Popen(['tar', '-xf', file, '-C', file_name_no_extension], cwd=path)
            subprocess.Popen(['rm', '-f', file], cwd=path)