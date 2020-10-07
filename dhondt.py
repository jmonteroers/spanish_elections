# to-do: add option to give votes needed for next seat
# instead of seats

# get dataframe with votes
import pandas as pd
import numpy as np
import pdb
# # pdb.set_trace = lambda: 1

df = pd.read_pickle('votos.pkl')

def dhondt_rule(row, next_party=False):
    '''
    This function takes a row with format Provincia, Diputados and Votos
    for each political party and returns a row with same format, except for
    the fact that instead of Votos, has the number of Diputados for each political
    party'''
    # set-up
    seats_remaining = row['Diputados']
    row_seats = row.copy()
    row_seats.iloc[2:] = 0
    if next_party:
        row_extra = row_seats.copy()
        last_winner = ""
    # get votes for count
    votes = row.iloc[2:].astype('int32')

    # dividing seats
    while seats_remaining > 0:
        # pdb.set_trace()
        # find winner
        winner = votes.idxmax()
        # update
        # max avoids to multiply by zero in first stage
        row_seats.loc[winner] += 1
        seats_remaining -= 1
        if seats_remaining != 0 or not next_party:
            # in all but last iteration, votes are edited
            # if next_party is False, always edited
            votes.loc[winner] = votes.loc[winner] * row_seats.loc[winner] \
                / (1 + row_seats.loc[winner])
        else:
            # in last iteration, compute extra votes
            votes_last_winner = votes.max()
            votes_last_second = votes.nlargest(2)[1]
            row_extra.iloc[2:] = np.ceil(votes_last_winner - votes)
            # for winner, compute excess votes as negative
            row_extra.loc[winner] = np.floor(votes_last_second - votes_last_winner)
            # compute actual votes back
            row_extra.iloc[2:] = row_extra.iloc[2:] * (1 + row_seats.iloc[2:])
            # pdb.set_trace()
            return row_extra

    return row_seats


df_results = df.apply(dhondt_rule, axis=1, args=(True,))
df_results.set_index('Provincia', inplace=True)

# save
df_results.to_pickle('extra_votes.pkl')

# revision
def with_seats(city, results=df_results):
    '''when returning seats, this function formats the result for a province'''
    s = results.loc[city]
    s = s[s > 0].sort_values(ascending=False)
    # put Diputados in the first row
    # take s.index, transform to list and remove 'Diputados'
    index_s = s.index.to_list()
    index_s.remove('Diputados')
    s = s.reindex(['Diputados'] + index_s)
    return s

def check_for_name(city, results=df_results):
    return results[results.index.str.contains(city)].index[0]

# resultados_madrid = with_seats('Madrid', df_results)

def print_extra(city, results=df_results):
    '''when returning extra votes, this function formats the result
    for a province'''
    s = results.loc[city]
    s = s.drop(labels='Diputados')
    return s

pdb.set_trace()
