'''
In this module, it will add two lists to our dataset:
- pparties.pkl, containing all political parties of November 2019 election
- pparties_with_rep.pkl, containing all political parties which won one seat in
the November 2019 election
'''
import pandas as pd
import pickle
import pdb
out_dir = 'data/output/'
### List of all political parties
results = pd.read_pickle(out_dir + 'results_by_province.pkl')
pparties = results.party.unique().tolist()
with open(out_dir + 'pparties.pkl', 'wb') as f:
    pickle.dump(pparties, f)
### List of political parties with representation
seats = results[results.result == 'diputados']
seats = seats[seats.value > 0]
pparties_with_rep = seats.party.unique().tolist()
with open(out_dir + 'pparties_with_rep.pkl', 'wb') as f:
    pickle.dump(pparties_with_rep, f)

# check
with open(out_dir + 'pparties.pkl', 'rb') as f:
    parsed_pparties = pickle.load(f)

with open(out_dir + 'pparties_with_rep.pkl', 'rb') as f:
    parsed_pparties_with_rep = pickle.load(f)
pdb.set_trace()
