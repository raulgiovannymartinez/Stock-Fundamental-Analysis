import pandas
import yahoo_fin.stock_info as si

"""
'PS':               'Price To Sales Ratio, is used to inform about how much the market capitalization exceeds the sales of 
                    a company. Typically, past 12 months sales are used.'
'PE':               'The Price to Earnings ratio is one of the most used ratios within the fundamental analysis measures. 
                    It can help us determine whether the company is over or undervalued with respect to other companies 
                    within the industry.'
'PEG':              'The PEG ratio is also known as the Price To Earnings Ratio Over Earnings Growth Rate. This is computed 
                    by calculating the PE ratio and dividing by the earnings growth. We can use the annual earnings growth 
                    rate.'
'PB':               'The price to book ratio is computed by taking the market capitalization and dividing it by the book value 
                    of the company. We can also compute it by taking the current share price and dividing it by the book 
                    value per share.'
'ProfitMargin':     'Profit margin is an important measure as it helps us understand the degree to which the company 
                    is generating income over its revenue. It is the ratio of the net income of a company over its revenue.'
'OperMargin':       'It is calculated by dividing the operating profit by the sales revenue. The profit is computed 
                    by calculating the difference between the revenue and all of the costs of a company.'
'CurrentRatio':     'The current ratio is one of the important balance sheet ratios to consider. It is a liquidity ratio and can 
                    inform us about the health of a company. It indicates whether the company can pay off its short-term debt.'
'DivPayoutRatio':   'The payout ratio is calculated by dividing the dividend amount per share by the earnings per share.'
'ROA':              'Each company has its assets, liabilities, and annual net income that it generates from the assets. The ROA 
                    stands for Return On Assets.'
'ROE':              'The ROE stands for Return On Equity. Remember that shareholder equity, or commonly known as equity, is the 
                    difference between the assets and the liabilities of a company. It is calculated by dividing the net income 
                    by the shareholder equity.'
'Cash/Share':       'This is the available cash over the number of outstanding shares.'
'Book/Share':       'Book value per share.'
'Debt/Equity':
"""

class Company:
    def __init__(self, symbol):
        self.symbol = symbol
        self.fundamental_indicators = {}
    

def to_float(val):
    if val == 0:
        return float(0)

    val = str(val).upper()

    if '%' in val:
        return round(float(val[:-1]), 4)

    m = {'K': 3, 'M': 6, 'B': 9, 'T': 12}

    for key in m.keys():
        if key in val:
            multiplier = m.get(val[-1])
            return round(float(val[:-1]) * (10 ** multiplier), 4)
    return round(float(val), 4)


def get_statatistics(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}"
    dataframes = pandas.read_html(url)
    return pandas.concat(dataframes[1:])


def get_data_item(result, dataframe, columns):
    for column_to_find, column_to_name in columns.items():
        try:
            result[column_to_name] = list((dataframe.loc[dataframe[0] == column_to_find].to_dict()[1]).values())[0]
        except Exception as ex:
            result[column_to_name] = 'NA'


def get_last_data_item(result, dataframe, columns):
    data = dataframe.iloc[:, :2]
    data.columns = ["Column", "Last"]

    for column_to_find, column_to_name in columns.items():
        try:
            val = data[data.Column.str.contains(column_to_find, case=False, regex=True)].iloc[0, 1]
            float_val = to_float(val)
            result[column_to_name] = float_val
        except Exception as ex:
            result[column_to_name] = "NA"


def get_fundamental_indicators_for_company(config, company):
    company.fundmantal_indicators = {}

    # Statistics Valuation
    keys = {
        'Market Cap (intraday) 5': 'MarketCap',
        'Price/Sales (ttm)': 'PS',
        'Trailing P/E': 'PE',
        'PEG Ratio (5 yr expected) 1': 'PEG',
        'Price/Book (mrq)': 'PB'
     }
    data = si.get_stats_valuation(company.symbol)
#     print(data)
    get_data_item(company.fundamental_indicators, data, keys)

    # Income statement and Balance sheet
    data = get_statatistics(company.symbol)

    get_data_item(company.fundamental_indicators, data,
              {
                  'Profit Margin': 'ProfitMargin',
                  'Operating Margin (ttm)': 'OperMargin',
                  'Current Ratio (mrq)': 'CurrentRatio',
                  'Payout Ratio 4': 'DivPayoutRatio'
              })

    get_last_data_item(company.fundamental_indicators, data,
           {
               'Return on assets': 'ROA',
               'Return on equity': 'ROE',
               'Total cash per share': 'Cash/Share',
               'Book value per share': 'Book/Share',
               'Total debt/equity': 'Debt/Equity'
           })
