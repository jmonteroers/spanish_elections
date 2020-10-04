"""
This module extracts the information from rows 3 and 4 of the
excel file PROV_02_201911_1.xlsx

Rows 3 and 4 link political party official names to their acronyms

Finally, the resulting dictionary is saved to data/dict_acronym_name.py

Possible future use: allow someone to run a function based on name of political party
"""

import pandas as pd
import json

# extract also row 5
# why? to avoid having to deal with repeated political party acronyms
# check excel file for further reference
df = pd.read_excel("data/PROV_02_201911_1.xlsx",
                   header=[3, 4, 5], nrows=0)
# read columns and create dictionary
dict_acronym_name = {}
for col in df.columns:
    political_party_name = col[0]
    political_party_acronym = col[1]
    if (not political_party_name.startswith("Unnamed")
        and political_party_acronym not in dict_acronym_name):
        dict_acronym_name[political_party_acronym] = political_party_name

# save as Python module
file_conn = open('data/dict_acronym_name.json', 'w')
json.dump(dict_acronym_name, file_conn)
file_conn.close()
