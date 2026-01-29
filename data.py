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
    66: "Operating_Income",
    11: "Inventory",
    6: "COGS"
}, inplace=True)

bs_df.rename(index={
    8: "Accounts_Receivable",
    20: "Current_Assets",
    52: "Current_Liabilities",
    38: "Accounts_Payable",
}, inplace=True)


#define both selected data out of CSVs
is_frame = is_df.loc[["Revenue", "Operating_Income", "Inventory", "COGS"], years]
bs_frame = bs_df.loc[["Accounts_Receivable", "Current_Assets", "Current_Liabilities", "Accounts_Payable"], years]

#transpose so that years are rows and features are columns
is_frame_t = is_frame.T
bs_frame_t = bs_frame.T

#combine datasets
combined_df = pd.concat([is_frame_t, bs_frame_t], axis=1)

#clean combined datasets 
combined_df = combined_df.replace({',': ''}, regex=True).apply(pd.to_numeric)

#add margins into dataset for scale and comparison against smaller companies
combined_df["Operating_Margin"] = combined_df["Operating_Income"] / combined_df["Revenue"]
combined_df["Current_Ratio"] = combined_df["Current_Assets"] / combined_df["Current_Liabilities"]
combined_df["DSO"] = combined_df["Accounts_Receivable"] / combined_df["Revenue"] * 365
combined_df["Inventory_Turnover"] = combined_df["COGS"] / combined_df["Inventory"]
combined_df["AP_Days"] = combined_df["Accounts_Payable"] / combined_df["COGS"] * 365

#add delta working cashflow for the business
combined_df["ΔAR_t+1"] = combined_df["Accounts_Receivable"].shift(-1) - combined_df["Accounts_Receivable"]
combined_df["ΔInventory_t+1"] = combined_df["Inventory"].shift(-1) - combined_df["Inventory"]
combined_df["ΔAP_t+1"] = combined_df["Accounts_Payable"].shift(-1) - combined_df["Accounts_Payable"]

# Normalize by Revenue or COGS to compare against periods
combined_df["ΔAR_t+1_ratio"] = combined_df["ΔAR_t+1"] / combined_df["Revenue"]
combined_df["ΔInventory_t+1_ratio"] = combined_df["ΔInventory_t+1"] / combined_df["COGS"]
combined_df["ΔAP_t+1_ratio"] = combined_df["ΔAP_t+1"] / combined_df["COGS"]

# Drop last year since target t+1 not available so now we measure 2014-2019
dataset = combined_df.iloc[:-1].copy()

#Add lagged features (Δs at t-1)
dataset["ΔAR_t"] = combined_df["Accounts_Receivable"].diff() / combined_df["Revenue"]
dataset["ΔInventory_t"] = combined_df["Inventory"].diff() / combined_df["COGS"]  # if COGS unavailable
dataset["ΔAP_t"] = combined_df["Accounts_Payable"].diff() / combined_df["Accounts_Payable"]
print(dataset)

features = [
        "Revenue", "Operating_Income", "Operating_Margin", 
        "Inventory", "Accounts_Receivable", "Accounts_Payable",
        "Current_Ratio", "DSO", "Inventory_Turnover", "AP_Days",
        "ΔAR_t", "ΔInventory_t", "ΔAP_t"
    ]
targets = ["ΔAR_t+1_ratio", "ΔInventory_t+1_ratio", "ΔAP_t+1_ratio"]
x = dataset[features]
y = dataset[targets]
