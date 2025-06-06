import pandas as pd

# Utility class to lookup BDN DataFrame rows by key columns
class BDN_dict:
    def __init__(self, df: pd.DataFrame, key: str) -> dict[str, pd.Series]:
        self.key_to_row = {row[key]: row for _, row in df.iterrows()} # Map keys to rows

    def lookup(self, key: str) -> pd.Series:
        key_to_row = self.key_to_row
        row = key_to_row.get(key, pd.Series(dtype='float64'))
        return row
