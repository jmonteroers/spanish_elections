import pickle
from utils import save_as_json, read_from_json
import pdb
out_dir = 'data/output/blocs/'
out_filename = 'dictionary_blocs.json'
blocs = ['investment_blocs_2020.json']

dict_blocs = {}
for bloc in blocs:
    bloc_name = bloc.replace('.json', '')
    this_bloc_dict = read_from_json(out_dir, bloc)
    dict_blocs[bloc_name] = this_bloc_dict

save_as_json(dict_blocs, out_dir, out_filename)

# check
parsed_dict_blocs = read_from_json(out_dir, out_filename)
pdb.set_trace()
