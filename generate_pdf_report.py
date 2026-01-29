"""Generate a one-page PDF summary with top plots and one-line explanations per target.

Outputs:
- outputs/reports/one_page_summary.pdf

Layout (per target):
- Left: Actual vs Predicted scatter plot image
- Right: One-line explanation (from shap_reports/explanation_{target}.txt), metrics, and dollar comparison mini-table
"""
import os
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

from data import dataset, features, targets, x, y
from utils import humanize_name

OUT_PDF = os.path.join('outputs', 'reports', 'one_page_summary.pdf')
PLOTS_DIR = os.path.join('outputs', 'plots')
SHAP_DIR = os.path.join('outputs', 'shap_reports')
REPORTS_DIR = os.path.join('outputs', 'reports')

os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)

metrics = pd.read_csv('metrics_summary.csv') if os.path.exists('metrics_summary.csv') else None

# Read combined dollar predictions if exists
dollar_all = None
dollar_file = os.path.join(REPORTS_DIR, 'dollar_predictions_all_targets.csv')
if os.path.exists(dollar_file):
    dollar_all = pd.read_csv(dollar_file)

# Prepare figure
fig = plt.figure(figsize=(8.5, 11))
plt.axis('off')

n = len(targets)
# compute row heights
rows = n
for i, target in enumerate(targets):
    # Row position
    top = 1 - (i * 1.0 / rows)
    # Left image axes for actual vs predicted
    ax_img = fig.add_axes([0.05, top - 0.28, 0.45, 0.25])
    img_path = os.path.join(PLOTS_DIR, f'actual_vs_pred_{target}.png')
    if os.path.exists(img_path):
        img = mpimg.imread(img_path)
        ax_img.imshow(img)
        ax_img.axis('off')
    else:
        ax_img.text(0.5, 0.5, 'No plot', ha='center', va='center')
        ax_img.axis('off')

    # Right text axes
    ax_txt = fig.add_axes([0.52, top - 0.28, 0.43, 0.25])
    ax_txt.axis('off')

    # Title
    title = humanize_name(target)
    ax_txt.text(0, 0.95, title, fontsize=12, weight='bold')

    # Explanation
    expl_file = os.path.join(SHAP_DIR, f'explanation_{target}.txt')
    explanation = ''
    if os.path.exists(expl_file):
        try:
            with open(expl_file, 'r', encoding='utf-8') as fh:
                lines = fh.read().strip().splitlines()
                if lines:
                    explanation = lines[0]
        except Exception:
            explanation = ''
    if explanation:
        wrapped = textwrap.fill(explanation, width=60)
        ax_txt.text(0, 0.72, wrapped, fontsize=9)

    # Metrics
    met_text = ''
    if metrics is not None:
        row = metrics[metrics['target'] == target]
        if not row.empty:
            r = row.iloc[0]
            met_text = f"MAE: {r['mae']:.6f}  RMSE: {r['rmse']:.6f}  R2: {r['r2']:.2f}"
            ax_txt.text(0, 0.45, met_text, fontsize=9)

    # Dollar table snippet
    if dollar_all is not None:
        subset = dollar_all[dollar_all['target'] == target]
        if not subset.empty:
            lines = []
            for _, rr in subset.iterrows():
                yr = int(rr['year'])
                act = rr['actual_abs']
                pred = rr['predicted_abs']
                err = rr['error_dollars']
                lines.append(f"{yr}: Actual ${act:,.0f}  Pred ${pred:,.0f}  Δ ${err:,.0f}")
            dol_text = "\n".join(lines)
            ax_txt.text(0, 0.20, dol_text, fontsize=8)

# Footer
fig.text(0.5, 0.02, 'One-page summary — models & SHAP explanations. Outputs and raw files in outputs/', ha='center', fontsize=8)

# Save pdf
pp = PdfPages(OUT_PDF)
pp.savefig(fig)
plt.close(fig)

# Add a second page with ratio definitions
defs_path = os.path.join('docs', 'RATIO_DEFINITIONS.md')
if os.path.exists(defs_path):
    with open(defs_path, 'r', encoding='utf-8') as fh:
        defs_text = fh.read()
else:
    defs_text = 'Ratio definitions not found.'

fig2 = plt.figure(figsize=(8.5, 11))
fig2.text(0.02, 0.98, 'Ratio Definitions', fontsize=16, weight='bold')
# wrap text into readable lines
import textwrap
wrapped = textwrap.fill(defs_text, width=100)
fig2.text(0.02, 0.94, wrapped, fontsize=10, va='top')
pp.savefig(fig2)
plt.close(fig2)

pp.close()
print(f'One-page PDF with definitions written to {OUT_PDF}')