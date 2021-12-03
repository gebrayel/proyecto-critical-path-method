import networkx as nx
import matplotlib.pyplot as plt

# G = nx.DiGraph()
# G.add_edges_from(
#     [('A', 'B'), ('A', 'C'), ('D', 'B'), ('E', 'C'), ('E', 'F'),
#      ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G')])

# val_map = {'A': 1.0,
#            'D': 0.5714285714285714,
#            'H': 0.0}

# values = [val_map.get(node, 0.25) for node in G.nodes()]

# # Specify the edges you want here
# red_edges = [['A', 'C'], ['E', 'C']]
# edge_colours = ['black' if not edge in red_edges else 'red'
#                 for edge in G.edges()]
# black_edges = [edge for edge in G.edges() if edge not in red_edges]

# # Need to create a layout when doing
# # separate calls to draw nodes and edges
# pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
#                        node_color = values, node_size = 500)
# nx.draw_networkx_labels(G, pos)
# nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
# nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
# plt.show()

import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt

df = pd.DataFrame({
    'from': ['Node1', 'Node1', 'Node2', 'Node2'],
    'to': ['Node2', 'Node3', 'Node4', 'Node5']
})
red_edges = [['Node1', 'Node2'], ['Node2', 'Node4']]
black_edges = [['Node1', 'Node3'], ['Node2', 'Node5']]
G = nx.from_pandas_edgelist(df, 'from', 'to')
edgesList = [['Node1', 'Node2'], ['Node2', 'Node4'],['Node1', 'Node3'], ['Node2', 'Node5']]
edges_color = ['red','red','black','black']
# positions = {
#     'Node1': [0,10],
#     'Node2': (1, 1),
#     'Node3': (1, -1),
#     'Node4': (2, 2),
#     'Node5': (2, 0),
# }  

# nx.draw(G, pos=positions, arrows=True, with_labels=True)
nx.drawing.nx_pylab.draw_networkx (G, arrows=True, with_labels=True, edgelist=edgesList, edge_color=edges_color)

# nx.drawing.nx_pylab.draw_networkx (G, pos=positions, arrows=True, with_labels=True, edgelist=black_edges,)
plt.show()