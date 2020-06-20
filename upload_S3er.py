import subprocess
import pickle

if __name__ == '__main__':
    with open('untarred.pkl', 'rb') as f:
        untarred = pickle.load(f)
    for file in untarred:
        print(file)