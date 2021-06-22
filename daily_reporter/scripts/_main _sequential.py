from collections import defaultdict
from datetime import datetime
import concurrent.futures
import pandas as pd
import tickers

from value_metrics import Company
import value_metrics


start_time = datetime.now()

# get tickers dataframe
df_tickers = tickers.get_all(stock_exchange='all')

# get value metrics and metadata
value_metrics_dict = defaultdict(list)
for index, row in df_tickers.iterrows():
    print(index)
    config = {}
    company = Company(row['Symbol'])

    try:
        value_metrics.get_fundamental_indicators_for_company(config, company)
    except:
        continue

    for c in df_tickers.columns: 
        value_metrics_dict[c].append(row[c])

    for k, v in company.fundamental_indicators.items():
        value_metrics_dict[k].append(v)

    # if index==10:
    #     break

# results in dataframe
df_results = pd.DataFrame(value_metrics_dict)
df_results = df_results.apply(pd.to_numeric, errors='ignore')

date_str = str(datetime.now()).replace(':','-')
df_results.to_csv('./results/{} - {} stocks report (troubleshooting).csv'.format(date_str, stock_exchange), index=False)

# compute new metrics and sort
df_results['PE*PB (<22.5 good)'] = df_results['PE']*df_results['PB'] 
df_results.sort_values(by='PE*PB (<22.5 good)', inplace=True)

# save results
date_str = str(datetime.now()).replace(':','-')
df_results.to_csv('./results/{} - {} stocks report.csv'.format(date_str, stock_exchange), index=False)

print('Total time: {}'.format(datetime.now()-start_time))

