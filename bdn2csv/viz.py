import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def get_parent_path(term_path: str) -> str:
    parent_path = "\\".join(term_path.split("\\")[0:-1])
    return parent_path

def get_related_term_path(related_term: str) -> str:
    related_term_path = related_term.split("|")[0]
    return related_term_path

def get_related_term_label(related_term: str) -> str:
    related_term_label = related_term.split("|")[1] if "|" in related_term else "" # if related term has label
    return related_term_label

class BDNx:
    def __init__(self, df: pd.DataFrame):
        self.G = nx.DiGraph() # BDN as a directed graph
        self.df = df # BDN DataFrame representation
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
        for _, term in df.iterrows():
            parent = get_parent_path(term['Path'])
            if parent != "": # if parent exists
                G.add_edge(parent, term['Path'])
            related_terms = str(term['Related Terms']).split(",")
            for related_term in related_terms:
                related_term_path = get_related_term_path(related_term)
                related_term_label = get_related_term_label(related_term)
                if related_term_path in G:
                    G.add_edge(term['Path'], related_term_path, label=related_term_label)
                    G.add_edge(related_term_path, term['Path'], label=related_term_label)

def visualize(csv_path: str, png_path: str):
    df = pd.read_csv(csv_path)
    bdn = BDNx(df)
    G = bdn.G
    nx.draw_networkx(G)
    plt.savefig(png_path)
