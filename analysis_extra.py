import pandas as pd
import pdb


df = pd.read_pickle('extra_votes.pkl')

# write to long format
# remove Diputados
df.drop('Diputados', axis=1, inplace=True)
# reset index
df.reset_index(inplace=True)
df = pd.melt(df, id_vars='Provincia', var_name = 'Party', value_name='Extra')

# group by province
# find: last political party to win (negative value)
# find next political party that could have won (least value from positive values)
# find by how many

def find_everything(x):
    'returns a series, which will become a row per group'
    d = {}
    # pdb.set_trace()
    # obtain last winner
    d['Last Winner'] = x['Party'][x['Extra'] < 0].iloc[0]
    # obtain next would-have-been winner
    x.set_index('Party', inplace=True)
    d['Next Winner'] = x[x['Extra'] >= 0].idxmin().iloc[0]
    # obtain votes at stake
    d['Votes'] = x[x['Extra'] >= 0].min()
    return pd.Series(d, index=['Last Winner', 'Next Winner', 'Votes'])


df = df.groupby('Provincia')['Party', 'Extra'].apply(find_everything)


pdb.set_trace()
