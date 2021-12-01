from node import *
class Graph:

    def __init__(self):
        self.nodes_dict = {}
        self.num_vertices = 0 #no reelevante
    
    def add_node(self, nodeId: int, nodeDescription: str, nodeDuration: float, pred:list):  #str tipo calle callecarrera (5010, 5011, 5012)
        self.num_vertices = self.num_vertices + 1
        new_node = Node(nodeId, nodeDescription, nodeDuration, pred)
        self.nodes_dict[nodeId] = new_node
        return new_node

    def add_edge(self, nodeFrom: int, nodeTo: int):
        # if nodeFrom not in self.nodes_dict:
        #     self.add_node(nodeFrom)
        # if nodeTo not in self.nodes_dict:
        #     self.add_node(nodeTo)

        self.nodes_dict[nodeFrom].set_sucesor(self.nodes_dict[nodeTo])
        self.nodes_dict[nodeTo].set_predecesor(self.nodes_dict[nodeFrom])

    def debug(self):
        print(self.nodes_dict)