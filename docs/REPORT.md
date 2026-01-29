# Final Project Report — Predicting Future Working Capital Behavior 📊

## Executive summary
This study demonstrates that machine learning can predict and explain future working capital behavior using financial statement data, enabling forward-looking liquidity insights that cannot be obtained from traditional accounting methods.

## Targets
- ΔAR_(t+1) / Revenue_t
- ΔInventory_(t+1) / COGS_t
- ΔAP_(t+1) / COGS_t

## Model & evaluation
- Model: Random Forest Regressor (non-linear, interaction-aware, robust).
- Train/Test: Time-aware split (earlier years → train, recent years → test).
- Metrics: Mean Absolute Error (MAE), RMSE, R2 in `metrics_summary.csv`.

## Explainability & Visuals
1. Actual vs Predicted (scatter) — model validity and directional accuracy (`outputs/plots/actual_vs_pred_{target}.png`).
2. Feature importance — mean |SHAP| bar chart (`outputs/plots/shap_bar_{target}.png`) and CSV rankings (`outputs/shap_reports/feature_ranking_{target}.csv`).
3. SHAP summary plot — direction and magnitude of effects (`outputs/plots/shap_summary_{target}.png`).
4. SHAP waterfall (single case) — narrative explanation for a single year/company (`outputs/plots/shap_waterfall_{target}_case.png`).
5. Time-series validation — actual vs predicted over the test period (`plots/timeseries_{target}.png`).

## Business impact
- Predictive: Early detection of rising AR or inventory that may strain liquidity.
- Explanatory: SHAP shows operational levers (DSO, margin, revenue growth) driving changes.
- Actionable: Use outputs to prioritize collections, adjust inventory plans, or renegotiate supplier terms.

## Reproducibility
- Run `python train_model.py` after installing `requirements.txt`.
- Results are saved to `outputs/models/`, `outputs/plots/`, and `metrics_summary.csv`.

---
For further extensions: Multi-company model, cross-validation across firms, threshold-based alerting, and integration with FP&A systems for automated recommendations.