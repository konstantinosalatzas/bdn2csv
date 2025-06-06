import pandas as pd

class bdn_dict:
    def __init__(self, df: pd.DataFrame, key: str) -> dict[str, pd.Series]:
        self.key_to_row = {row[key]: row for _, row in df.iterrows()}

    def look_up(self):
        pass

class bdn_set:
    def __init__(self, df: pd.DataFrame, key: str) -> set[str]:
        pass

    def is_in(self):
        pass
