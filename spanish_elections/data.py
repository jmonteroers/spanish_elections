import pandas as pd
import json
from pkg_resources import resource_stream
from os.path import join
import pickle


def save_as_json(o, dir, filename):
    with open(join(dir, filename), 'w') as f:
        json.dump(o, f)


def save_as_pkl(o, dir, filename):
    with open(join(dir, filename), 'wb') as f:
        return pickle.dump(o, f)


def get_resource_stream(filename, subdir=['data']):
    return resource_stream(__name__,
                             join(*subdir, filename))


def load_general_data():
    stream = get_resource_stream('general_data.pkl')
    return pd.read_pickle(stream)


def load_results(type: 'either "votes" or "seats"'):
    stream = get_resource_stream('results_by_province.pkl')
    results = pd.read_pickle(stream)
    if type == 'votes':
        results = results[results.result == 'votos']
        results.rename(columns={'value': 'votes'}, inplace=True)
    elif type == 'seats':
        results = results[results.result == 'diputados']
        results.rename(columns={'value': 'seats'}, inplace=True)
    else:
        raise(ValueError('type must be either "votes" or "seats"'))
    del results['result']
    return results


def load_seats_by_province():
        stream = get_resource_stream('n_seats.json')
        return json.load(stream)


def load_political_parties(with_rep=True):
    filename = 'pparties_with_rep.pkl' if with_rep else 'pparties.pkl'
    stream = get_resource_stream(filename)
    return pickle.load(stream)


def load_blocs():
    stream = get_resource_stream('dictionary_blocs.json')
    return json.load(stream)
