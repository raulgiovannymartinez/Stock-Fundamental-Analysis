import pandas as pd

"""
source: https://www.nasdaq.com/market-activity/stocks/screener?exchange=nyse&letter=0&render=download
"""

def get_all(stock_exchange='all'):
        df_agg = pd.DataFrame()

        list_ =  ['amex', 'nasdaq', 'nyse'] if stock_exchange=='all' else [stock_exchange]

        for se in list_:

                cols = ['Symbol',
                        'Name',
                        'Country',
                        'IPO Year',
                        'Sector',
                        'Industry']
                df = pd.read_csv('./data/{}_ticks.csv'.format(se))[cols]

                df_agg = pd.concat([df_agg, df])
        
        return df_agg
    