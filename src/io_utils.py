import pandas as pd

def read_file(path):
    path = path.lower()

    if path.endswith('.csv'):
        return pd.read_csv(path)
    elif path.endswith('.xlsx') or path.endswith('.xls'):
        return pd.read_excel(path)
    elif path.endswith('.json'):
        return pd.read_json(path)
    else:
        raise ValueError("Unsupported file format")
