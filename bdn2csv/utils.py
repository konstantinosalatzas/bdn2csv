import pandas as pd
import networkx as nx

# Utility function to get parent term path from term path
def get_parent_path(term_path: str) -> str:
    parent_path = "\\".join(term_path.split("\\")[0:-1])
    return parent_path

# Utility function to get related term path from related term with label
def get_related_term_path(related_term: str) -> str:
    related_term_path = related_term.split("|")[0]
    return related_term_path

# Utility function to get related term label from related term with label
def get_related_term_label(related_term: str) -> str:
    related_term_label = related_term.split("|")[1] if "|" in related_term else "" # if related term has label
    return related_term_label

# Utility class to lookup BDN DataFrame rows by key columns
class BDN_dict:
    def __init__(self, df: pd.DataFrame, key: str) -> dict[str, pd.Series]:
        self.key_to_row = {row[key]: row for _, row in df.iterrows()} # Map keys to rows

    def lookup(self, key: str) -> pd.Series:
        key_to_row = self.key_to_row
        row = key_to_row.get(key, pd.Series(dtype='float64'))
        return row

def check_dag_and_find_cycles(g: nx.Graph):
    is_dag = nx.is_directed_acyclic_graph(g) # check if the graph is a DAG
    if not is_dag: # the graph contains at least 1 cycle
        cycles = nx.recursive_simple_cycles(g) # list of cycles
        return cycles
    return []
