"""Compute predicted vs actual dollar changes for AR, Inventory, AP and save side-by-side CSV and plots.

Outputs:
- outputs/reports/dollar_predictions.csv
- outputs/plots/dollar_compare_{target}.png
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from data import dataset, features, targets, x, y

OUT_DIR = os.path.join('outputs', 'reports')
PLOTS_DIR = os.path.join('outputs', 'plots')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# Recreate X test split like train_model
X = x.copy()
X['year'] = [int(str(yr)) for yr in dataset.index]
X = X.reset_index(drop=True)
X = X.sort_values('year').set_index('year')

n = len(X)
test_size = max(1, int(np.ceil(n * 0.3)))
train_size = n - test_size
X_test = X.iloc[train_size:]

results = []
for target in targets:
    pkg = joblib.load(f"outputs/models/model_{target}.joblib")
    imputer = pkg['imputer']
    model = pkg['model']
    feat_names = pkg['features']

    X_test_imp = pd.DataFrame(imputer.transform(X_test), columns=feat_names, index=X_test.index)
    preds_ratio = model.predict(X_test_imp)

    # Choose scale
    if target.startswith('ΔAR'):
        scale = X_test['Revenue']
        actual_abs = dataset.reset_index(drop=True).iloc[train_size:]['ΔAR_t+1'].values
    elif target.startswith('ΔInventory'):
        scale = dataset.reset_index(drop=True).iloc[train_size:]['COGS']
        actual_abs = dataset.reset_index(drop=True).iloc[train_size:]['ΔInventory_t+1'].values
    else:
        scale = dataset.reset_index(drop=True).iloc[train_size:]['COGS']
        actual_abs = dataset.reset_index(drop=True).iloc[train_size:]['ΔAP_t+1'].values

    predicted_abs = preds_ratio * scale.values

    df = pd.DataFrame({
        'year': X_test.index,
        'target': target,
        'actual_abs': actual_abs,
        'actual_ratio': (actual_abs / scale.values),
        'predicted_ratio': preds_ratio,
        'predicted_abs': predicted_abs,
    })
    df['error_dollars'] = df['predicted_abs'] - df['actual_abs']
    # percent error relative to actual absolute (if actual_abs is 0 use NaN)
    df['error_pct'] = np.where(df['actual_abs'] != 0, df['error_dollars'] / df['actual_abs'], np.nan)

    # Save CSV for this target
    df.to_csv(os.path.join(OUT_DIR, f'dollar_predictions_{target}.csv'), index=False)

    # Plot side-by-side bar charts for actual vs predicted dollars
    plt.figure(figsize=(8,4))
    years_labels = df['year'].astype(str).tolist()
    positions = np.arange(len(df))
    width = 0.35
    plt.bar(positions - width/2, df['actual_abs'], width=width, label='Actual ($)')
    plt.bar(positions + width/2, df['predicted_abs'], width=width, label='Predicted ($)')
    plt.xlabel('Year')
    plt.ylabel('Dollar change')
    plt.title(f"Actual vs Predicted dollar change — {target}")
    plt.xticks(positions, years_labels)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, f'dollar_compare_{target}.png'))
    plt.close()

    results.append(df)

# Combine all targets into one tidy CSV for side-by-side review
combined = pd.concat(results)
combined.to_csv(os.path.join(OUT_DIR, 'dollar_predictions_all_targets.csv'), index=False)
print(f'Dollar prediction reports written to {OUT_DIR} and plots to {PLOTS_DIR}')
