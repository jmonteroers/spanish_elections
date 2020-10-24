import pandas as pd
import pdb

def agg_results(results: pd.DataFrame,
                result_col: str,
                party_col: str = 'party',
                min_value=0):
    agg_res = results.groupby(party_col)[result_col].agg(sum)
    return agg_res[agg_res > min_value]



if __name__ == '__main__':
    results = pd.read_pickle('../data/output/results_by_province.pkl')
    seats = results[results.result == 'diputados']
    agg_seats = agg_results(seats, 'value')
    pdb.set_trace()
