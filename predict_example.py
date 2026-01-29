"""Example: load a saved model and generate prediction + local SHAP explanation for a new observation.

Usage: python predict_example.py
"""
import joblib
import pandas as pd
import numpy as np
import shap

MODEL_PATH = "outputs/models/model_ΔAR_t+1_ratio.joblib"

# Simple demo: take last available row from dataset as 'new' observation (replace with real company-year row)
from data import x, dataset

# pick most recent available row (before last year where target exists)
new_obs = x.iloc[-1:].copy()
print("New observation (features):\n", new_obs)

pkg = joblib.load(MODEL_PATH)
imputer = pkg["imputer"]
model = pkg["model"]
features = pkg["features"]

from utils import FEATURE_LABELS, humanize_name

# Show human-readable features
new_obs_h = new_obs.rename(columns=FEATURE_LABELS)
print("New observation (human-readable features):\n", new_obs_h)

new_imp = pd.DataFrame(imputer.transform(new_obs), columns=features)
pred = model.predict(new_imp)[0]
print(f"Predicted {humanize_name(MODEL_PATH.split('model_')[-1].replace('.joblib',''))} = {pred:.6f}")

# SHAP local explanation
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(new_imp)
shap_series = pd.Series(shap_values[0], index=[FEATURE_LABELS.get(f,f) for f in features])
print("SHAP values (human-readable):\n", shap_series)
