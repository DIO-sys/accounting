import joblib
import pandas as pd
import numpy as np
import os
from data import dataset, features, targets, x, y

EXPLAIN_DIR = os.path.join('outputs', 'shap_reports')
os.makedirs(EXPLAIN_DIR, exist_ok=True)

reports = []

for target in targets:
    pkg = joblib.load(f"outputs/models/model_{target}.joblib")
    imputer = pkg['imputer']
    model = pkg['model']
    feat_names = pkg['features']

    # Build X_test as in train script
    X = x.copy()
    X['year'] = [int(str(yr)) for yr in dataset.index]
    X = X.reset_index(drop=True)
    X = X.sort_values('year').set_index('year')

    n = len(X)
    test_size = max(1, int(np.ceil(n * 0.3)))
    train_size = n - test_size
    X_test = X.iloc[train_size:]
    X_test_imp = pd.DataFrame(imputer.transform(X_test), columns=feat_names, index=X_test.index)

    import shap
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test_imp)

    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    fi = pd.Series(mean_abs_shap, index=feat_names).sort_values(ascending=False)

    # Convert to human labels
    from utils import FEATURE_LABELS, humanize_name
    human_index = [FEATURE_LABELS.get(f, f) for f in fi.index]
    fi_h = fi.copy()
    fi_h.index = human_index

    # Save feature ranking (human labels)
    fi_h.to_csv(os.path.join(EXPLAIN_DIR, f"feature_ranking_{target}.csv"), header=['mean_abs_shap'])

    # Global one-paragraph explanation (use human names)
    top3 = fi_h.head(3)
    desc = []
    for feat, val in top3.items():
        desc.append(f"{feat} (mean |SHAP|={val:.5f})")
    paragraph = f"For target {humanize_name(target)}, the top drivers are: {', '.join(desc)}."

    # Local explanation for first test instance (use human names)
    local_paragraph = ''
    if X_test_imp.shape[0] >= 1:
        inst = X_test_imp.iloc[0:1]
        sv = explainer.shap_values(inst)[0]
        local = pd.Series(sv, index=feat_names).sort_values(ascending=False)
        # convert to human labels
        local_h = local.copy()
        local_h.index = [FEATURE_LABELS.get(f, f) for f in local.index]
        local_top = local_h.head(3)
        local_bot = local_h.tail(3)
        local_paragraph = (
            f"First test instance ({X_test_imp.index[0]}): top positive contributors: {', '.join([f'{f} ({v:.4f})' for f,v in local_top.items()])}; "
            f"top negative contributors: {', '.join([f'{f} ({v:.4f})' for f,v in local_bot.items()])}."
        )

    # Save a small text report
    with open(os.path.join(EXPLAIN_DIR, f"explanation_{target}.txt"), 'w', encoding='utf-8') as fh:
        fh.write(paragraph + "\n" + local_paragraph)

    reports.append({'target': target, 'top_features': ';'.join(top3.index), 'paragraph': paragraph, 'local': local_paragraph})

# Save combined CSV summary with utf-8 encoding
pd.DataFrame(reports).to_csv(os.path.join(EXPLAIN_DIR, 'shap_summary_table.csv'), index=False, encoding='utf-8')
print('SHAP summarization complete. Reports written to shap_reports/')