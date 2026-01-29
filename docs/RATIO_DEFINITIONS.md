# Ratio Definitions & Human-Readable Names 🔍

This file lists the ratio variables used in the project, their written names, short definitions/formulas, and units.

- `ΔAR_t+1_ratio` — **Δ Accounts Receivable (t+1) / Revenue**
  - Definition: (Accounts Receivable_{t+1} − Accounts Receivable_t) / Revenue_t
  - Units: dollars change normalized by Revenue (fraction)
  - Note: Positive → AR increases relative to revenue (collection deterioration)

- `ΔInventory_t+1_ratio` — **Δ Inventory (t+1) / COGS**
  - Definition: (Inventory_{t+1} − Inventory_t) / COGS_t
  - Units: dollars change normalized by COGS (fraction)
  - Note: Positive → Inventory buildup relative to cost of goods sold (cash tied up)

- `ΔAP_t+1_ratio` — **Δ Accounts Payable (t+1) / COGS**
  - Definition: (Accounts Payable_{t+1} − Accounts Payable_t) / COGS_t
  - Units: dollars change normalized by COGS (fraction)
  - Note: Positive → Payables increase relative to COGS (supplier financing)

- `DSO` — **Days Sales Outstanding (DSO)**
  - Definition: Accounts Receivable / Revenue * 365
  - Units: days
  - Note: Higher DSO → slower collections

- `Inventory_Turnover` — **Inventory Turnover (times)**
  - Definition: COGS / Inventory
  - Units: times per period
  - Note: Lower turnover → slower inventory movement

- `AP_Days` — **Accounts Payable Days (AP Days)**
  - Definition: Accounts Payable / COGS * 365
  - Units: days
  - Note: Higher AP days → longer payment terms (short-term cash benefit)

- `Operating_Margin` — **Operating Margin (EBIT / Revenue)**
  - Definition: Operating Income / Revenue
  - Units: fraction (ratio)
  - Note: Higher margin → more operating cash buffer

- `Current_Ratio` — **Current Ratio (Current Assets / Current Liabilities)**
  - Definition: Current Assets / Current Liabilities
  - Units: ratio
  - Note: Higher ratio → greater short-term liquidity

- Lagged Δs (used as lag features)
  - `ΔAR_t` — **Δ Accounts Receivable (t) / Revenue** (prior period)
  - `ΔInventory_t` — **Δ Inventory (t) / COGS** (prior period)
  - `ΔAP_t` — **Δ Accounts Payable (t) / COGS** (prior period)

---
File created at `docs/RATIO_DEFINITIONS.md`. Let me know if you want these exported into `outputs/reports/` as a CSV or included in the PDF one-page summary.