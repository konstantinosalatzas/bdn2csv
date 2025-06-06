import pandas as pd

class bdn_dict:
    def __init__(self, df: pd.DataFrame, key: str) -> dict[str, pd.Series]:
        self.key_to_row = {row[key]: row for _, row in df.iterrows()}

    def look_up(self, key: str) -> pd.Series:
        key_to_row = self.key_to_row
        row = key_to_row.get(key, pd.Series(dtype='float64'))
        return row

class bdn_set:
    def __init__(self, df: pd.DataFrame, key: str) -> set[str]:
        self.keys = set(df[key])

    def is_in(self) -> bool:
        pass
