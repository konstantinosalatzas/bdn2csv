import pandas as pd
import networkx as nx

class BDN:
    def __init__(self):
        self.G = nx.DiGraph() # BDN as a directed graph

    def construct(self, csv_path):
        G = self.G
        bdn = pd.read_csv(csv_path)
        for _, term in bdn.iterrows():
            pass

    def visualize(self):
        pass

'''dev'''

csv_path = "/workspaces/bdn2csv/data/Import.csv"

bdn = BDN()
bdn.construct(csv_path)
print(bdn.G)
