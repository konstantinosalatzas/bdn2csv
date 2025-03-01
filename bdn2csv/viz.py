import pandas as pd
import networkx as nx

class BDN:
    def __init__(self):
        self.G = nx.DiGraph() # BDN as a directed graph

    def construct(self, csv_path: str):
        G = self.G
        df = pd.read_csv(csv_path)
        for _, term in df.iterrows():
            G.add_node(term['Path']) # add terms as nodes to the graph

    def visualize(self):
        pass
