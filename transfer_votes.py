import pandas as pd

import pdb


def transfer_votes(votes, list_transfer_votes):
    '''
    Arguments:
    - votes is a dictionary with parties and votes
    - list_transfer_votes is a list of tuples with the following structure:
    (source, dest, proportion of votes from source to dest)

    The transfers are applied from the original votes, so the order within
    list_transfer_votes does not affect the result

    Returns:
    - votes with transferred votes
    '''
    final_votes = votes.copy()
    for source, dest, prop in list_transfer_votes:
        votes_transferred = round(prop*votes[source])
        final_votes[source] -= votes_transferred
        final_votes[dest] += votes_transferred
    return final_votes


def transfer_votes_single_province(results: pd.DataFrame,
                                   list_transfer_votes,
                                   party_col='party',
                                   votes_col='votes',
                                   replace=False,
                                   final_votes_col='final_votes'):
    '''
    Always returns the resulting dataframe.
    if replace is False, add new column to DataFrame with name `final_votes_col`
    '''
    results = results.copy()
    results.set_index(party_col, inplace=True)
    final_votes = transfer_votes(results[votes_col], list_transfer_votes)
    if replace:
        results[votes_col] = final_votes
    else:
        results[final_votes_col] = final_votes
    results.reset_index(inplace=True)
    return results


def transfer_votes_long(results: pd.DataFrame,
                       list_transfer_votes,
                       province_col='province',
                       party_col='party',
                       votes_col='votes',
                       replace=False,
                       final_votes_col='final_votes'):
    grouped_results = results.groupby(province_col)
    results_with_transfers = \
    grouped_results.apply(transfer_votes_single_province,
                          list_transfer_votes,
                          party_col=party_col,
                          votes_col=votes_col,
                          replace=replace,
                          final_votes_col=final_votes_col)
    return results_with_transfers.reset_index(drop=True)

dict_version = False
long_version_single_province = True
long_version = False
if __name__ == '__main__' and dict_version:
    votes = {'Green Book': 12500, 'Mary Poppins': 7600,
             'The Big Short': 15000}
    # apply the following transfers:
    # 20 % of Green Book votes are transferred to Mary Poppins
    # 15 % of The Big Short votes are transferred to Green Book
    # 10 % of Mary Poppins votes are transferred to The Big Short
    final_votes = transfer_votes(votes,
                                 [('Green Book', 'Mary Poppins', .2),
                                  ('The Big Short', 'Green Book', .15),
                                  ('Mary Poppins', 'The Big Short', .1)])
    pdb.set_trace()


if __name__ == '__main__' and long_version_single_province:
    results = pd.Series({'Green Book': 12500, 'Mary Poppins': 7600,
                            'The Big Short': 15000})
    results = pd.DataFrame(results).reset_index()
    results.columns = ['movies', 'votes']
    results_with_transfers = \
    transfer_votes_single_province(results,
                                   [('Green Book', 'Mary Poppins', .2),
                                    ('The Big Short', 'Green Book', .15),
                                    ('Mary Poppins', 'The Big Short', .1)],
                                   party_col='movies',
                                   replace=False)
    pdb.set_trace()


if __name__ == '__main__' and long_version:
    out_dir = 'data/output/'
    results = pd.read_pickle(out_dir + 'results_by_province.pkl')
    votes = results[results.result == 'votos'].copy()
    votes.rename(columns={'value': 'votes'}, inplace=True)
    votes_with_transfers = \
    transfer_votes_long(votes,
                        [('PSOE', 'PP', .2),
                         ('Cs', 'PSOE', .15),
                         ('PP', 'VOX', .1)],
                        province_col='provincia',
                        party_col='party',
                        votes_col='votes',
                        replace=False)
    pdb.set_trace()
