import pandas as pd
import networkx as nx

class BDN:
    def __init__(self, csv_path: str):
        self.G = nx.DiGraph() # BDN as a directed graph
        self.df = pd.read_csv(csv_path) # BDN DataFrame representation
        self.construct()

    def construct(self):
        self.add_nodes()
        self.add_edges() # add edges after adding all nodes

    def add_nodes(self):
        G = self.G
        df = self.df
        for _, term in df.iterrows():
            G.add_node(term['Path']) # add terms as nodes to the graph

    def add_edges(self):
        G = self.G
        df = self.df
        pass # Add edge from parent
        for _, term in df.iterrows():
            related_terms = str(term['Related Terms']).split(",")
            for related_term in related_terms:
                if related_term in G:
                    print(related_term)
                    pass # Add edges between related term

    def visualize(self):
        pass

#dev
csv_path = "/workspaces/bdn2csv/data/Import.csv"
bdn = BDN(csv_path)
print(bdn.G)
