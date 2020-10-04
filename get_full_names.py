# create a dictionary with full names, just in case
# a more advanced search on names is needed

import pandas as pd
import pprint
import pdb
df = pd.read_excel("PROV_02_201911_1.xlsx",
                   header=[3, 4, 5])
pdb.set_trace()
# create a dictionary with full names, just in case
# a more advanced search on names is needed
dict_full_names = {}
for col in df.columns:
    if not col[0].startswith("Unnamed"):
        dict_full_names[col[1]] = col[0]

# save as Python object
fileObj = open('full_names.py', 'w')
fileObj.write('dict_full_names = ' + pprint.pformat(dict_full_names) + '\n')
fileObj.close()
