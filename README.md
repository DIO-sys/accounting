Accounting: Cashflow statement modeling and insight.

-process: take in different metrics from accounting statemnts and use it to forecast the years cashflow and provide insight on how to improve cashflow in the future, as well as why it is important

Step 1: Gathering Features
We will be gathering different metrics found in the main file, and using the indirect method of accounting, determining whether they increase or decrease cashflow in relation to their effect on net income. This is why we measure things like delta assets, and liabilities on the balance sheet, versus the reported value on the income statement

Feature importance for the model 
Income Statement
1. Revenue. Total amount of cash brought in for the period
2. Operating Income. Also known as EBIT, shows how profitable a businesses core operations actually are
3. Net income. Shows you how much money company made overall, or after all expenses
4. Depreciation. Comes up as a loss on the income statement, but the expense non-cash, so added back for cashflow

Balance Sheet
1. Delta Accounts Receivable. This is a non-cash accrual, so it'll positively affect net income, but negatively affect cf
2. Same deal for delta inventory
3. Opposite deal for delta accounts payable

Ratios (All benchmarks vary by industry. We are using consumer goods standards)
1. Current Ratio. Short term assets / short term liabilities, a high ratio (x > 1.5) can generate usually cash easily 
2. Operating Margin. operating income / revenue, how profitable a businesses core operations are, (x > .15) is efficient
3. Days Sales Outstanding. acc rec/ rev *365 is the inverse of rec turnover (which I couldn't get) and measures duration of credit sales collection. lower quantities = faster cash collection good for cashflow
4. Change in Collections. delta acc rec/ revenue measures how revenue turns to cash in the period. higher quantities = negative cash flow

