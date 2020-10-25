import json
import pickle
from os.path import join

def save_as_json(o, dir, filename):
    with open(join(dir, filename), 'w') as f:
        json.dump(o, f)


def read_from_json(dir, filename):
    with open(join(dir, filename)) as f:
        return json.loads(f.read())


def save_as_pkl(o, dir, filename):
    with open(join(dir, filename), 'wb') as f:
        return pickle.dump(o, f)

def read_from_pkl(dir, filename):
    with open(join(dir, filename), 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    # note: creates example_list.json in current directory!
    l1 = [1, 2, 3]
    save_as_json(l1, '', 'example_list.json')
    parsed_l1 = read_from_json('', 'example_list.json')
    pdb.set_trace()
