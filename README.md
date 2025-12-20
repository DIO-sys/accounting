Accounting: Cashflow statement modeling and insight.

The goal of this project is to take metrics from a company’s financial statements and use them to forecast future operating cash flow (OCF), while providing actionable insights on what drives cash flow. This helps managers, investors, and analysts understand how operational and working capital decisions affect liquidity, and highlights areas where cash generation can be improved.

Cash flow is crucial because it represents real liquidity unlike net income, which is affected by accounting policies and non-cash items, OCF shows how much cash the business actually generates to sustain operations, pay debts, and invest for growth.

Step 2: Feature Selection

Income Statement Metrics

Revenue – total cash brought in during the period.
Operating Income (EBIT) – shows profitability from core operations.
Net Income – overall profit after all expenses.
Depreciation & Amortization – non-cash expense added back to cash flow.

Balance Sheet Metrics
Delta Accounts Receivable – change in receivables; positive net income impact, negative cash flow impact.
Delta Inventory – change in inventory levels; also reduces cash when inventory increases.
Delta Accounts Payable – change in payables; higher payables temporarily improve cash flow (opposite of AR and inventory).

Ratios & Engineered Metrics
Current Ratio – current assets ÷ current liabilities; shows short-term liquidity. Higher than ~1.5 usually indicates cash availability.
Operating Margin – operating income ÷ revenue; efficiency of core operations. Higher than ~15% indicates strong operational efficiency.
Days Sales Outstanding (DSO) – accounts receivable ÷ revenue × 365; measures speed of cash collection. Lower is better.
Change in Collections – delta accounts receivable ÷ revenue; shows how effectively revenue is converted into cash during the period. Higher values reduce cash flow.

Step 3: Data Preparation
Import the CSVs for income statement and balance sheet.
Rename relevant rows to clear variable names for easy reference:
Income Statement: Revenue, Operating Income, Inventory
Balance Sheet: Accounts Receivable, Inventory, Accounts Payable, Current Assets, Current Liabilities
Select the years of interest (2014–2020) for training.
Transpose the data so that years are rows and variables are columns.
Combine the two datasets into a single dataframe.
Clean the data by removing commas and converting values to numeric format.