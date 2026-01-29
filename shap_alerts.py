"""Generate rule-based alerts from model predictions and SHAP contributions.

Rules (adaptive):
- For ΔAR and ΔInventory: risk if predicted > mean(predictions) + 0.5*std(predictions) AND relevant feature SHAP (DSO or Inventory_Turnover) positive and >= 20% of total |SHAP|.
- For ΔAP: risk if predicted < mean(predictions) - 0.5*std(predictions) AND relevant feature SHAP (AP_Days) negative and <= -20% of total |SHAP|.

Outputs:
- alerts.csv with one row per alert
"""
import joblib
import pandas as pd
import numpy as np
import os
from data import dataset, features, targets, x, y

OUT = os.path.join('outputs','alerts')
os.makedirs(OUT, exist_ok=True)
alerts = []

# Build X_test as in train
X = x.copy()
X['year'] = [int(str(yr)) for yr in dataset.index]
X = X.reset_index(drop=True)
X = X.sort_values('year').set_index('year')

n = len(X)
test_size = max(1, int(np.ceil(n * 0.3)))
train_size = n - test_size
X_test = X.iloc[train_size:]

for target in targets:
    pkg = joblib.load(f"outputs/models/model_{target}.joblib")
    imputer = pkg['imputer']
    model = pkg['model']
    feat_names = pkg['features']

    X_test_imp = pd.DataFrame(imputer.transform(X_test), columns=feat_names, index=X_test.index)

    # predictions
    preds = model.predict(X_test_imp)
    preds_mean = preds.mean()
    preds_std = preds.std(ddof=0) if len(preds) > 1 else 0.0

    # shap
    import shap
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test_imp)

    # Identify relevant feature for risk
    if target.startswith('ΔAR'):
        key_feat = 'DSO'
        direction = 1  # higher -> more risk
        threshold = preds_mean + 0.5 * preds_std
    elif target.startswith('ΔInventory'):
        # use Inventory_Turnover or Inventory if turnover absent
        key_feat = 'Inventory_Turnover' if 'Inventory_Turnover' in feat_names else 'Inventory'
        direction = 1
        threshold = preds_mean + 0.5 * preds_std
    else:  # ΔAP
        key_feat = 'AP_Days'
        direction = -1  # lower predicted AP_ratio (more negative) -> risk (paying down AP)
        threshold = preds_mean - 0.5 * preds_std

    key_feat_label = None
    try:
        from utils import FEATURE_LABELS
        key_feat_label = FEATURE_LABELS.get(key_feat, key_feat)
    except Exception:
        key_feat_label = key_feat

    for i, year in enumerate(X_test_imp.index):
        pred = preds[i]
        sv = shap_values[i]
        sv_series = pd.Series(sv, index=feat_names)
        total_abs = np.abs(sv_series).sum() if np.abs(sv_series).sum() > 0 else 1.0
        key_shap = sv_series.get(key_feat, 0.0)

        condition = False
        if direction == 1:
            condition = pred > threshold and key_shap > 0 and abs(key_shap) >= 0.2 * total_abs
        else:
            condition = pred < threshold and key_shap < 0 and abs(key_shap) >= 0.2 * total_abs

        if condition:
            alert_type = 'HIGH_RISK'
            reason = f"Pred {pred:.6f} vs thresh {threshold:.6f}; {key_feat_label} SHAP {key_shap:.6f} ({abs(key_shap)/total_abs:.2%} of total)"
            alerts.append({'year': year, 'target': target, 'target_label': humanize_name(target), 'predicted': pred, 'alert': alert_type, 'reason': reason})
# Save alerts
alerts_df = pd.DataFrame(alerts)
alerts_df.to_csv(os.path.join(OUT, 'alerts.csv'), index=False)
print(f"Alerts generated: {len(alerts)}; saved to {OUT}/alerts.csv")
if len(alerts) > 0:
    print(alerts_df)
else:
    print('No alerts triggered with current thresholds.')