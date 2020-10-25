import pandas as pd
import json
import pdb

output_file = 'data/output/n_seats.json'
general_data = pd.read_pickle('data/output/general_data.pkl')
general_data.set_index('provincia', inplace=True)
seats = general_data['diputados']
seats.to_json(output_file)

# check
with open(output_file) as file_with_seats:
    parsed = json.loads(file_with_seats.read())
pdb.set_trace()
