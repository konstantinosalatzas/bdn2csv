import pandas as pd
import networkx as nx

class BDN:
    def __init__(self, csv_path: str):
        self.G = nx.DiGraph() # BDN as a directed graph
        self.df = pd.read_csv(csv_path) # BDN DataFrame representation
        self.construct(csv_path)

    def construct(self, csv_path: str):
        G = self.G
        df = self.df
        for _, term in df.iterrows():
            G.add_node(term['Path']) # add terms as nodes to the graph

    def visualize(self):
        pass

#dev
csv_path = "/workspaces/bdn2csv/data/Import.csv"
bdn = BDN(csv_path)
G = bdn.G
print(G)
