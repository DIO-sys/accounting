import pandas as pd

#import our data
is_df = pd.read_csv("pg_docs/pg_is.csv", encoding='latin1')
bs_df = pd.read_csv("pg_docs/pg_bs.csv", encoding='latin1', header = 1)

#reference for variable positions
'''
variables 
company  0 
year  bs row 1  
revenue is row 4
op_income is row 66
AR bs row 8
inventory is row 11
AP is row 38
current_assets	bs row 20
current_liab bs row 52
'''
years = ["2014", "2015", "2016", "2018", "2019", "2020"]

is_df.rename(index={
    4: "Revenue",
    66: "Operating Income",
    11: "Inventory",
}, inplace=True)

bs_df.rename(index={
    8: "Accounts Receivable",
    20: "Current Assets",
    52: "Current Liabilities",
    38: "Accounts Payable"
}, inplace=True)



#define both selected data out of CSVs
is_frame = is_df.loc[["Revenue", "Operating Income", "Inventory"], years]
bs_frame = bs_df.loc[["Accounts Receivable", "Current Assets", "Current Liabilities", "Accounts Payable"], years]

#transpose so that years are rows and features are columns
is_frame_t = is_frame.T
bs_frame_t = bs_frame.T

#combine datasets
combined_df = pd.concat([is_frame_t, bs_frame_t], axis=1)

#clean combined datasets 
combined_df = combined_df.replace({',': ''}, regex=True).apply(pd.to_numeric)

print(combined_df)
