from collections import defaultdict
from datetime import datetime
import concurrent.futures
from os.path import join
from os import listdir
import pandas as pd
import tickers

from value_metrics import Company
import value_metrics


# define function to run in parallel
def process_ticker_metrics(symbol):
    print(symbol)
    
    config = {}
    company = Company(symbol)
    
    try:
        value_metrics.get_fundamental_indicators_for_company(config, company)
    except:
        return
    
    # create dictionary with result
    value_metrics_dict = defaultdict(list)
    value_metrics_dict['Symbol'] = symbol
    for k, v in company.fundamental_indicators.items():
        value_metrics_dict[k].append(v) 

    # results in dataframe
    fp = './results/_cache_valuation_metrics/{}.csv'.format(symbol)
    pd.DataFrame(value_metrics_dict).to_csv(fp, index=False)


if __name__ == '__main__':

    start_time = datetime.now()

    # get tickers dataframe
    df_tickers = tickers.get_all(stock_exchange='all')

    # process in parallel
    process_tickers = True
    if process_tickers:
        with concurrent.futures.ProcessPoolExecutor() as executor:
        	executor.map(process_ticker_metrics, list(df_tickers.Symbol.unique()))

    # combine all ticker results
    df_results = pd.DataFrame()
    cvm_fp = './results/_cache_valuation_metrics'
    for f in listdir(cvm_fp):
        ticker_fp = join(cvm_fp, f)
        df_results = pd.concat([df_results, pd.read_csv(ticker_fp)])

    df_results = df_results.merge(df_tickers, on='Symbol')

    # compute new metrics and sort
    df_results = df_results.apply(pd.to_numeric, errors='ignore')
    df_results['PE*PB (<22.5 good)'] = df_results['PE']*df_results['PB'] 
    df_results.sort_values(by='PE*PB (<22.5 good)', inplace=True)

    # save
    date_str = str(datetime.now()).replace(':','-')
    df_results.to_csv('./results/{} - stocks report.csv'.format(date_str), index=False)


    print('Total time: {}'.format(datetime.now()-start_time))

