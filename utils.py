# Helper utilities for human-readable labels

FEATURE_LABELS = {
    "Revenue": "Revenue",
    "Operating_Income": "Operating Income (EBIT)",
    "Operating_Margin": "Operating Margin",
    "Inventory": "Inventory",
    "Accounts_Receivable": "Accounts Receivable",
    "Accounts_Payable": "Accounts Payable",
    "Current_Ratio": "Current Ratio",
    "DSO": "Days Sales Outstanding (DSO)",
    "Inventory_Turnover": "Inventory Turnover (times)",
    "AP_Days": "Accounts Payable Days (AP Days)",
    "ΔAR_t": "ΔAR (t) / Revenue",
    "ΔInventory_t": "ΔInventory (t) / COGS",
    "ΔAP_t": "ΔAP (t) / COGS",
    "ΔAR_t+1_ratio": "ΔAR (t+1) / Revenue",
    "ΔInventory_t+1_ratio": "ΔInventory (t+1) / COGS",
    "ΔAP_t+1_ratio": "ΔAP (t+1) / COGS",
}

TARGET_LABELS = {
    "ΔAR_t+1_ratio": "Δ Accounts Receivable (next year) / Revenue",
    "ΔInventory_t+1_ratio": "Δ Inventory (next year) / COGS",
    "ΔAP_t+1_ratio": "Δ Accounts Payable (next year) / COGS",
}


def humanize_name(name: str) -> str:
    """Return a human-readable label for a feature or target name."""
    if name in TARGET_LABELS:
        return TARGET_LABELS[name]
    return FEATURE_LABELS.get(name, name.replace('_', ' '))
