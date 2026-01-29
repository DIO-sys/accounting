# Modeling & Explanation Pipeline 🔧

## Purpose
This pipeline trains Random Forest models to predict future working capital behavior (ΔAR, ΔInventory, ΔAP normalized by scale metrics) using the prepared accounting dataset. It produces model performance metrics, SHAP explanations, and useful visuals for stakeholder communication.

## What is included
- `train_model.py` — trains one Random Forest model per target, saves models and key plots: actual vs predicted, time-series, SHAP summary, SHAP bar, SHAP waterfall (written into `outputs/`). All plot **titles and SHAP reports use layperson-friendly labels** (e.g., "Days Sales Outstanding (DSO)").
- `outputs/models/` — saved model packages (`model_{target}.joblib`) containing the imputer and the trained Random Forest.
- `outputs/plots/` — all visualization outputs (human-friendly titles).
- `outputs/shap_reports/` — SHAP CSVs and textual explanations (human-readable feature names).
- `outputs/alerts/alerts.csv` — rule-based alerts (if any trigger), includes `target_label` with readable name.
- `metrics_summary.csv` — MAE, RMSE, R2 per target (includes `target_label`).

## How to run
1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run training and analysis:

```bash
python train_model.py
```

## Key design choices
- Target: per your spec, models predict ΔAR_(t+1)/Revenue_t, ΔInventory_(t+1)/COGS_t, ΔAP_(t+1)/COGS_t.
- Time-aware split: training uses earlier years; test uses the most recent 30% of years.
- Model: Random Forest Regressor (non-linear, robust, interpretable with SHAP).
- Explainability: SHAP TreeExplainer for global and local explanations.

## One-sentence outcome
"This study demonstrates that machine learning can predict and explain future working capital behavior using financial statement data, enabling forward-looking liquidity insights that cannot be obtained from traditional accounting methods." ✅

## Next steps / suggestions
- Expand dataset to multiple companies (company-year rows) to improve generalizability.
- Add cross-company time-aware K-folds and out-of-time validation.
- Implement automated rule extraction from SHAP values for manager alerts.