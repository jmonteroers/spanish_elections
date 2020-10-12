import pdb
import pandas as pd

def argmax_dict(d):
    return sorted(d, key=lambda x: -d[x])[0]

def dhondt_rule(results: dict, n_seats) -> dict:
    '''
    results is a dictionary with the name of the parties as keys and
    the number of votes as values
    seats is a dictionary with the same keys as results and the
    number of seats as values

    Current implementation does not account for draws
    '''
    n_seats_remaining = n_seats
    seats = {party: 0 for party in results}
    transformed_results = results.copy()  # to modify using allocated seats
    while n_seats_remaining:
        most_voted_party = argmax_dict(transformed_results)
        seats[most_voted_party] += 1
        n_seats_remaining -= 1
        ratio_seats = seats[most_voted_party]/(1 + seats[most_voted_party])
        transformed_results[most_voted_party] *= ratio_seats
    return seats


def dhondt_rule_long_single_province(results: pd.DataFrame,
                                     n_seats: 'number of seats to allocate',
                                     party_col_name='party',
                                     votes_col_name='votes',
                                     out_col_name='seats',
                                     inplace=False) -> pd.DataFrame:
    '''
    Arguments:
    - results is a pd.DataFrame with a column with the name of the political
    parties and another column with votes for each party

    Outputs:
    - results with additional column with number of seats allocated to each
    political party, named `out_col_name`
    '''
    # set political party as index of DataFrame
    if not inplace:
        results = results.copy
    results.set_index(party_col_name, inplace=True)
    n_seats_remaining = n_seats
    results[out_col_name] = 0
    transformed_results = results[votes_col_name].copy()
    while n_seats_remaining:
        most_voted_party = transformed_results.idxmax()
        # add seat to most voted party
        results.loc[most_voted_party, out_col_name] += 1
        n_seats_remaining -= 1
        # apply new number of seats to transformed results
        seats_most_voted_party = results.loc[most_voted_party, out_col_name]
        ratio_seats = seats_most_voted_party/(1 + seats_most_voted_party)
        transformed_results.loc[most_voted_party] *= ratio_seats
    results.reset_index(inplace=True)
    if not inplace:
        return results


def dhondt_rule_long(results: pd.DataFrame,
                     n_seats: dict,
                     province_col_name='province'
                     party_col_name='party',
                     votes_col_name='votes',
                     out_col_name='seats',
                     inplace=False) -> pd.DataFrames:
    for province, results_by_province in results.groupby(province_col_name):
        # now i could easily apply each dhondt rule
        # problem, aggregation!
        n_seats_province = n_seats[province]
        pdb.set_trace()



dict_version = False
long_version_single_province = True
long_version = False
if __name__ == '__main__' and dict_version:
    results = {'PSOE': 15000,
               'PP': 20000,
                'Cs': 7500,
                'Podemos': 5500}
    seats = dhondt_rule(results, 7)
    pdb.set_trace()

if __name__ == '__main__' and long_version_single_province:
    results = pd.DataFrame({'political_parties': ['Podemos', 'PSOE', 'Cs'],
                            'votes': [10000, 7500, 2000]})
    dhondt_rule_long_single_province(results, n_seats=3,
                                     party_col_name='political_parties',
                                     out_col_name='seats',
                                     inplace=True)
    pdb.set_trace()


if __name__ == '__main__' and long_version:
    pass
