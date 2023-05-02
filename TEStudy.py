import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt


def get_data(start, end, symbols, column_name="Adj Close", include_spy=True, data_folder="./data"):

  # Construct an empty DataFrame with the requested date range.
  dates = pd.date_range(start, end)
  df = pd.DataFrame(index=dates)

  # Read SPY.
  df_spy = pd.read_csv(f'{data_folder}/SPY.csv', index_col=['Date'], parse_dates=True, na_values=['nan'], usecols=['Date',column_name])

  # Use SPY to eliminate non-market days.
  df = df.join(df_spy, how='inner')
  df = df.rename(columns={column_name:'SPY'})

  # Append the data for the remaining symbols, retaining all market-open days.
  for sym in symbols:
    df_sym = pd.read_csv(f'{data_folder}/{sym}.csv', index_col=['Date'], parse_dates=True, na_values=['nan'], usecols=['Date',column_name])
    df = df.join(df_sym, how='left')
    df = df.rename(columns={column_name:sym})

  # Eliminate SPY if requested.
  if not include_spy: del df['SPY']

  return df


def calcualte_AR(data,start_estimate, end_estimate, symbol, end_pred):
   
    X = data.loc[start_estimate:end_estimate,:][symbol]
    y = data.loc[start_estimate:end_estimate]['SPY']

    # Add a constant to the independent value
    X1 = sm.add_constant(X)

    # make regression model 
    model = sm.OLS(y, X1).fit()
    print(model.summary())
    alpha = model.params[0]
    beta = model.params[1]

    print(alpha, beta)
    data['estimate'] = alpha + beta * data.loc[start_estimate:end_pred]["SPY"]
    abnormal_return = data.loc[start_estimate:end_pred][symbol] - data.loc[start_estimate:end_pred]['estimate']

    return abnormal_return


def main():
    data = get_data(start = '03-17-2020', end = '12-31-2021', include_spy= True, symbols=["AAPL", "AMZN", "WMT", "EBAY", "KO"])
   
    index = data.index
    data = data/data.iloc[0] -1
    print(data)

    #plt.plot(data)
    #plt.show()

    
    ar = calcualte_AR(data, start_estimate=  "2020-03-17", end_estimate="2020-06-30", symbol="AMZN", end_pred="2021-12-31" )
    plt.plot(ar)
    plt.show()

main()


   
   

