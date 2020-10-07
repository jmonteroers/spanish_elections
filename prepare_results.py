# objetivo: obtener tabla de votos y de escaños
# para hacer una prueba más tarde

import pandas as pd
import pdb

df = pd.read_excel("PROV_02_201911_1.xlsx",
                   header=[3, 4, 5], nrows=52)

# general data, that will be appended to both datasets
first_row_cols = df.columns.get_level_values(0)
# function to find last column with unnamed
def find_unnamed(list):
    index_last_unnamed = -1
    for item in list:
        if item.startswith("Unnamed"):
            index_last_unnamed += 1
        else:
            return index_last_unnamed
index_general = find_unnamed(first_row_cols)

df_general = df.iloc[:, :(index_general+1)]
df_general.columns = df_general.columns.droplevel([0, 1])

# simplify name of main columns
df_general.columns = df_general.columns.str.replace("Nombre de ", "")
# note need to trim strings (Comunidad, Provincia)
df_obj = df_general.select_dtypes(['object'])
df_general[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
# remove alternative names from Provincia
df_general.Provincia = df_general.Provincia.str.replace(r" / .*$", "")
# pdb.set_trace()
# convert Codigo de Provincia to number
df_general['Código de Provincia'] = df_general['Código de Provincia'].astype('int32')

# notice use of xs to just restrict by third level
df_votos = df.xs('Votos', axis=1, level=2, drop_level=False)
df_votos.columns = df_votos.columns.droplevel([0, 2])
df_votos = pd.concat([df_general['Provincia'],
                      df_votos], axis=1)

# chequeo de concat: suman todos los votos los votos a candidaturas?
df_suma = df_votos.sum(axis=1)
# pdb.set_trace()
if all(df_general['Votos a candidaturas'] == df_suma):
    print('Suma de votos en df_votos igual a votos totales a candidaturas')

# do the same with seats
df_diputados = df.xs('Diputados', axis=1, level=2, drop_level=True)
df_diputados.columns = df_diputados.columns.droplevel(0)
df_diputados = pd.concat([df_general['Provincia'], df_diputados], axis=1)

# need to add seats to divide
seats = df_diputados.sum(axis=1)
df_votos = pd.concat([df_votos, seats], axis=1)
df_votos.rename(columns={0:'Diputados'}, inplace=True)

# order df_votos columns
#pdb.set_trace()
cols_df_votos = list(df_votos.columns)
cols_df_votos = [cols_df_votos[0]] + [cols_df_votos[-1]] + cols_df_votos[1:-1]
df_votos = df_votos[cols_df_votos]

# save dataframes
df_general.to_pickle("./resultados.pkl")
df_votos.to_pickle('./votos.pkl')
df_diputados.to_pickle('./diputados.pkl')

#pdb.set_trace()
