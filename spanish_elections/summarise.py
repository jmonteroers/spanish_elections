import pandas as pd
import pprint
from spanish_elections.data import save_as_json
import pdb

def agg_results(results: pd.DataFrame,
                result_col: str,
                party_col: str = 'party',
                min_value=0):
    agg_res = results.groupby(party_col)[result_col].agg(sum)
    return agg_res[agg_res > min_value]


class Bloc:
    '''a container for dict with some convenience functions to work with
    dictionaries in dataframes and restrict values'''
    def __init__(self, classif=None,bloc_values=None):
        self.bloc_values = bloc_values
        if classif and self.check_correct_values(classif):
            self.classif = classif
        else:
            self.classif = {}

    def add_value_to_bloc(self, name, bloc_value):
        if self.check_correct_value(name):
            self.classif[name] = bloc_value

    def update_bloc(self, new_classif: dict):
        if self.check_correct_values(new_classif):
            self.classif.update(new_classif)

    def show_bloc(self):
        pprint.pprint(self.classif)

    def check_correct_value(self, value: str):
        if self.bloc_values is None:
            return True
        if value not in self.bloc_values + [None]:
            raise(ValueError('classification contains invalid bloc values.'
                             ' edit self.bloc_values or modify'
                             ' value in classification'))
        return True

    def check_correct_values(self, classif: dict):
        for value in classif.values():
            self.check_correct_value(value)
        return True

    def add_bloc_column(self, df: pd.DataFrame, bloc_col,
                         party_col='party',
                         inplace=False):
        if not inplace:
            df = df.copy()
        df[bloc_col] = df[party_col].map(self.classif)
        return df if not inplace else None

    def summarise_by_bloc(self, df, party_col, agg_fun, other_agg=[],
                           inplace=False):
        if not inplace:
            df = df.copy()
        df = self.add_bloc_column(df, 'bloc', party_col=party_col,
                              inplace=False)
        return df.groupby(other_agg + ['bloc']).agg(agg_fun)

    def combine(self, bloc) -> 'bloc':
        '''
        combines the dictionaries of self.classif and bloc.classif, by taking
        the keys of self.classif and mapping them to the values of bloc.classif

        assume that all values of self.classif are keys in bloc'''
        new_dict = {key: bloc.classif[value]
                    for key, value in self.classif.items()}
        return bloc(classif=new_dict, bloc_values=bloc.bloc_values)

    def save_bloc_as_json(self, filename, dir=''):
        '''saves classif attribute as a dictionary in json in dir'''
        save_as_json(self.classif, dir, filename)

def input_values(key, bloc_values):
    '''Assumes that empty string is not in bloc_values.
    empty input is translated into None'''
    if bloc_values is None:
        return input(f'Insert a bloc for {key}: ')
    admitted_values = bloc_values + ['']
    new_value = None
    while new_value not in admitted_values:
        new_value = input(f'Insert a bloc for {key}. Admitted values are'
                          f' {admitted_values}: ')
    # translate empty string to None
    new_value = new_value if new_value else None
    return new_value


def create_bloc_interactively(keys: 'bloc or list',
                               bloc_values=None) -> Bloc:
    '''keys are the keys to ask the user for. if bloc object is
    provided, keys will be read from the internal dictionary values, not keys'''
    new_bloc = Bloc(bloc_values=bloc_values)
    new_bloc_dict = {}
    if isinstance(keys, Bloc):
        keys = keys.classif.values()
    for key in keys:
        new_bloc_dict[key] = input_values(key, bloc_values)
    new_bloc.update_bloc(new_bloc_dict)
    return new_bloc


if __name__ == '__main__':
    results = pd.read_pickle('../data/output/results_by_province.pkl')
    seats = results[results.result == 'diputados']
    agg_seats = agg_results(seats, 'value')
    pdb.set_trace()
