import pandas as pd

# Load  CSV
is_df = pd.read_csv("pg_docs/pg_is.csv", encoding='latin1')
bs_df = pd.read_csv("pg_docs/pg_bs.csv", encoding='latin1', header = 1)


#define class for all of the features to be used later
class BookValue:
    def __init__(self, df, position, year):
        self.df = df
        self.position = position
        self.year = year

    def value(self):
        cell = str(self.df.loc[self.position, self.year]).replace(",", "")
        print(cell)
        return pd.to_numeric(cell, errors="coerce")
    

#Start defining features  
#Income statement features
#all indexes + 1
revenue = BookValue(is_df, 4, "2016").value()
operating_income = BookValue(is_df, 66, "2016").value()
net_income = BookValue(is_df, 42, "2016").value()
depreciation =  BookValue(is_df, 74, "2016").value()




#Balance sheet features
#all indexes + 2
d_acc_rec = BookValue(bs_df, 8,"2015").value() - BookValue(bs_df, 8, "2016").value()
d_inv = BookValue(bs_df, 10, "2015").value() - BookValue(bs_df, 10, "2016").value()
d_acc_pay = BookValue(bs_df, 38, "2016").value() - BookValue(bs_df, 38, "2015").value()
current_assets = BookValue(bs_df, 20, "2016").value()
current_liabilities =BookValue(bs_df, 52, "2016").value()
total_assets = BookValue(bs_df, 34, "2016").value()







