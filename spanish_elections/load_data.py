import pandas as pd
import json
from pkg_resources import resource_stream
from os.path import join

def load_general_data():
    stream = resource_stream(__name__,
                             join('data', 'general_data.pkl'))
    return pd.read_pickle(stream)


def load_results(type: 'either "votes" or "seats"'):
    stream = resource_stream(__name__,
                             join('data', 'results_by_province.pkl'))
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
        stream = resource_stream(__name__,
                                 join('data', 'n_seats.json'))
        return json.load(stream)
