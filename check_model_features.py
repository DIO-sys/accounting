import joblib
for target in ['ΔAR_t+1_ratio','ΔInventory_t+1_ratio','ΔAP_t+1_ratio']:
    pkg = joblib.load(f'models/model_{target}.joblib')
    print(target, '->', pkg['features'])
