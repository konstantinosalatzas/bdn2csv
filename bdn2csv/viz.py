import pandas as pd
import networkx as nx

class BDN:
    def __init__(self):
        self.G = nx.DiGraph() # BDN as a directed graph

    def construct(self, csv_path):
        G = self.G
        bdn = pd.read_csv(csv_path)

    def visualize(self):
        pass

#dev
bdn = BDN()
bdn.construct("/workspaces/bdn2csv/data/Import.csv")
print(bdn.G)
