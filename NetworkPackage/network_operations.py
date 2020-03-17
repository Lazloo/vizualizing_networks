import networkx as nx


class NetworkClass:
    def __init__(self):
        self.graph = nx.DiGraph()

    def load_network(self, file_name: str) -> bool:
        self.graph = nx.read_graphml(file_name)
        return True

