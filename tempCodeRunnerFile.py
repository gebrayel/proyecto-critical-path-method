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