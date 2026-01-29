"""Train Random Forest models to predict future working capital ratios and generate SHAP explanations.

Usage: python train_model.py

Outputs:
- models/*.joblib
- plots/actual_vs_pred_{target}.png
- plots/shap_summary_{target}.png
- plots/shap_bar_{target}.png
- metrics_summary.csv
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import shap
from utils import FEATURE_LABELS, TARGET_LABELS, humanize_name

# Import prepared dataset from data.py (it exposes `dataset`, `features`, `targets`, `x`, `y`)
from data import dataset, features, targets, x, y

OUTPUT_BASE = "outputs"
OUTPUT_DIR = os.path.join(OUTPUT_BASE, "plots")
MODELS_DIR = os.path.join(OUTPUT_BASE, "models")
SHAP_REPORTS_DIR = os.path.join(OUTPUT_BASE, "shap_reports")
ALERTS_DIR = os.path.join(OUTPUT_BASE, "alerts")
# create directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(SHAP_REPORTS_DIR, exist_ok=True)
os.makedirs(ALERTS_DIR, exist_ok=True)

# Convert index to numeric year for sorting
years = [int(str(yr)) for yr in dataset.index]
sort_order = np.argsort(years)
X = x.copy()
# Ensure we do not accidentally include the old index as a feature
X["year"] = [int(str(yr)) for yr in dataset.index]
X = X.reset_index(drop=True)
X = X.sort_values("year").set_index("year")
Y = y.copy()
Y.index = [int(str(yr)) for yr in dataset.index]
Y = Y.sort_index()

# Time-aware split: train on earlier years, test on last 30% (at least 1 year)
n = len(X)
test_size = max(1, int(np.ceil(n * 0.3)))
train_size = n - test_size
X_train = X.iloc[:train_size]
X_test = X.iloc[train_size:]
Y_train = Y.iloc[:train_size]
Y_test = Y.iloc[train_size:]

results = []

# For each target build a Random Forest
for target in targets:
    print(f"Training for target: {target}")

    # Impute missing values (very small dataset may have few missing values)
    imputer = SimpleImputer(strategy="median")
    imputer.fit(X_train)

    X_train_imp = pd.DataFrame(imputer.transform(X_train), columns=X_train.columns, index=X_train.index)
    X_test_imp = pd.DataFrame(imputer.transform(X_test), columns=X_test.columns, index=X_test.index)

    # Model and tune a tiny grid (keeps things fast on small data and avoids heavy parallelism)
    rf = RandomForestRegressor(random_state=42, n_jobs=1)
    param_grid = {
        "n_estimators": [100],
        "max_depth": [3, None],
    }

    tscv_splits = min(3, max(2, train_size - 1))
    tscv = TimeSeriesSplit(n_splits=tscv_splits)
    grid = GridSearchCV(rf, param_grid, cv=tscv, scoring="neg_mean_absolute_error", n_jobs=1, verbose=1)
    try:
        grid.fit(X_train_imp, Y_train[target])
        best = grid.best_estimator_
        print(f"Best params for {target}: {grid.best_params_}")
    except Exception as e:
        print(f"GridSearch failed for {target}: {e}. Falling back to default RandomForest.")
        # Fit a default random forest (fast)
        best = RandomForestRegressor(random_state=42, n_jobs=1)
        best.fit(X_train_imp, Y_train[target])

    # Fit best estimator on full training set
    best.fit(X_train_imp, Y_train[target])

    # Save model and imputer together
    model_package = {"imputer": imputer, "model": best, "features": list(X_train_imp.columns)}
    joblib.dump(model_package, os.path.join(MODELS_DIR, f"model_{target}.joblib"))

    # Predict
    y_pred = best.predict(X_test_imp)
    y_true = Y_test[target].values

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    results.append({"target": target, "target_label": humanize_name(target), "mae": mae, "rmse": rmse, "r2": r2})

    # Save actual vs predicted scatter (human-friendly labels)
    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y_true, y=y_pred)
    plt.plot([min(y_true), max(y_true)], [min(y_true), max(y_true)], color="r", linestyle="--")
    plt.xlabel(f"Actual — {humanize_name(target)}")
    plt.ylabel(f"Predicted — {humanize_name(target)}")
    plt.title(f"Actual vs Predicted — {humanize_name(target)}")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"actual_vs_pred_{target}.png"))
    plt.close()

    # Time-series plot for test period
    plt.figure(figsize=(8, 4))
    plt.plot(Y_test.index, y_true, marker="o", label="Actual")
    plt.plot(Y_test.index, y_pred, marker="o", label="Predicted")
    plt.xlabel("Year")
    plt.ylabel(humanize_name(target))
    plt.title(f"Time-series: Actual vs Predicted — {humanize_name(target)}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"timeseries_{target}.png"))
    plt.close()

    # SHAP explainability (use human-readable labels)
    try:
        explainer = shap.TreeExplainer(best)
        shap_values = explainer.shap_values(X_test_imp)

        # Create a human-labeled version of the test set for plotting
        X_test_imp_h = X_test_imp.rename(columns=FEATURE_LABELS)

        # SHAP summary (dot) plot — only if we have at least 2 test samples
        if X_test_imp_h.shape[0] >= 2:
            plt.figure(figsize=(8, 6))
            shap.summary_plot(shap_values, X_test_imp_h, show=False)
            # Title for lay audience
            plt.title(f"What drives {humanize_name(target)} — SHAP summary")
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, f"shap_summary_{target}.png"), bbox_inches="tight")
            plt.close()

        # Mean absolute SHAP bar (global importance)
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        fi = pd.Series(mean_abs_shap, index=X_test_imp_h.columns).sort_values(ascending=False)

        # Also save a small CSV of mean |SHAP| per feature for programmatic use (human labels)
        fi.to_csv(os.path.join(SHAP_REPORTS_DIR, f"feature_ranking_{target}.csv"), header=['mean_abs_shap'])

        plt.figure(figsize=(8, 4))
        sns.barplot(x=fi.values[:12], y=fi.index[:12])
        plt.title(f"Mean |SHAP| — {humanize_name(target)}")
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, f"shap_bar_{target}.png"))
        plt.close()

        # Waterfall for first test instance (if exists)
        if X_test_imp_h.shape[0] >= 1:
            instance_idx = 0
            try:
                shap.plots._waterfall.waterfall_legacy(explainer.expected_value, shap_values[instance_idx], feature_names=X_test_imp_h.columns)
            except Exception:
                # Fallback: show a simple bar of SHAP contributions
                contribs = pd.Series(shap_values[instance_idx], index=X_test_imp_h.columns).sort_values(ascending=False)
                plt.figure(figsize=(8, 4))
                sns.barplot(x=contribs.values[:12], y=contribs.index[:12])
                plt.title(f"Local SHAP contributions — {humanize_name(target)}")
            plt.title(f"SHAP Waterfall — {humanize_name(target)} — test index {X_test_imp_h.index[instance_idx]}")
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, f"shap_waterfall_{target}_case.png"), bbox_inches="tight")
            plt.close()

    except Exception as e:
        print(f"SHAP failed for {target}: {e}")

# Save metrics
metrics_df = pd.DataFrame(results)
metrics_df.to_csv("metrics_summary.csv", index=False)
print(f"Training complete. Metrics saved to metrics_summary.csv. Outputs → {OUTPUT_BASE}/ (models, plots, shap_reports, alerts)")
