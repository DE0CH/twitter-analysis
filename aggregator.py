import os
import pickle
if __name__ == '__main__':
    linesC = 0
    try:
        with open('aggregated11.pkl', 'rb') as pf:
            processed_names = pickle.load(pf)
    except FileNotFoundError:
        processed_names = set()
    with open('all.json', 'w') as out_file:
        for path, dirs, files in os.walk('processed'):
            for file in files:
                file_path = os.path.join(path, file)
                if file_path in processed_names or not file.endswith('.json'):
                    continue
                with open(file_path) as f:
                    for line in f:
                        out_file.write(line)
                        linesC += 1
            processed_names.add(file_path)
    # with open('aggregated.pkl', 'wb') as pf:
    #     pickle.dump(processed_names, pf)
    print(linesC)