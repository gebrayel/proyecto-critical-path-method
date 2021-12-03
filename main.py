#import networkx as nx
##import matplotlib.pyplot as plt
#from networkx.algorithms import graph_hashing
from networkx.algorithms.bipartite.basic import color
from node import *
from graph import *
import sys
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt


graph : Graph
graphX1: Graph
nodesId = []

# def forwardPass():
def check_user_input(input):
    var = False
    try:
        # Convert it into integer
        val = int(input)
        var = True
        if val <=0 :
            var = False
            print("Hubo un error en el input")
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            var = True
            if val <=0 :
                var = False
                print("Hubo un error en el input")
        except ValueError:
            print("Hubo un error en el input")
    

    return var




def cpm(graphVal: Graph):
    alterNodesId:list = []
    arrayQueue:list = []
    graphX: Graph = graphVal
    for i in nodesId:
        graph.add_node(i, graphVal.nodes_dict[i].description, graphVal.nodes_dict[i].duration, graphVal.nodes_dict[i].pred)
    for node in nodesId:
        alterNodesId.append(node)
    #forward
    alterNodesId.pop(0)
    
    for i in alterNodesId:
            if graphX.nodes_dict[i].pred[0] == "inicio":
                arrayQueue.append(graphX.nodes_dict[i].id)
    while len(arrayQueue) !=0:
        predNodes:list = []
        actual = arrayQueue.pop()
        if graphX.nodes_dict[actual].pred[0] == "inicio":
            graphX.nodes_dict[actual].ef += graphX.nodes_dict[actual].duration
            for j in alterNodesId:
                if actual in graphX.nodes_dict[j].pred:
                    arrayQueue.append(j)
        else:
            predNodes = graphX.nodes_dict[actual].pred
            valid = True
            for k in predNodes:
                if graphX.nodes_dict[k].ef == 0:
                    valid = False
                    break
            if valid:
                maxEF = 0
                for n in predNodes:
                    if graphX.nodes_dict[n].ef > maxEF:
                        maxEF = graphX.nodes_dict[n].ef
                graphX.nodes_dict[actual].es = maxEF
                graphX.nodes_dict[actual].ef = maxEF +graphX.nodes_dict[actual].duration
                for l in alterNodesId:
                    if actual in graphX.nodes_dict[l].pred:
                        arrayQueue.append(l)

    for i in nodesId:
        print(f'Nodo: {i}, ES: {graphX.nodes_dict[i].es}, EF: {graphX.nodes_dict[i].ef}')
    #forward

    #alterNodesId = nodesId
    #alterNodesId.pop(0)

    #backward
    # auxiliaryArray: list = []
    # for i in alterNodesId:
    #     for j in graphX.nodes_dict[i].pred:
    #         if j not in auxiliaryArray:
    #             auxiliaryArray.append(j)
    # setAll = set(alterNodesId)
    # setPred = set(auxiliaryArray)
    # setLast = (setAll - setPred) 
    firstList = graphX.nodes_dict["final"].pred
    graphX.nodes_dict["final"].lf = graphX.nodes_dict["final"].ef
    graphX.nodes_dict["final"].ls = graphX.nodes_dict["final"].lf - graphX.nodes_dict["final"].duration
    indexA = alterNodesId.index("final")
    alterNodesId.pop(indexA)
    for j in firstList:
        arrayQueue.append(j)
        index = alterNodesId.index(j)
        alterNodesId.pop(index)
    while len(arrayQueue) != 0:
        predNodes:list = []
        sucNodes:list = []
        actual = arrayQueue.pop(0)
        if actual in firstList:
            maxEfbP = 0
            for i in firstList:
                if graphX.nodes_dict[i].ef > maxEfbP:
                    maxEfbP = graphX.nodes_dict[i].ef
            graphX.nodes_dict[actual].lf = maxEfbP
            graphX.nodes_dict[actual].ls = maxEfbP - graphX.nodes_dict[actual].duration
            for i in graphX.nodes_dict[actual].pred:
                if i not in arrayQueue:
                    arrayQueue.append(i)
        else:
            for i in nodesId:
                if actual in graphX.nodes_dict[i].pred:
                    sucNodes.append(i)
            valid = True
            for j in sucNodes:
                if graphX.nodes_dict[j].ls == 0:
                    valid = False
                    break
            
            if valid:
                maxLS = sys.maxsize
                for i in sucNodes:
                    if graphX.nodes_dict[i].ls < maxLS:
                        maxLS = graphX.nodes_dict[i].ls
                graphX.nodes_dict[actual].lf = maxLS
                graphX.nodes_dict[actual].ls = maxLS - graphX.nodes_dict[actual].duration
                for j in graphX.nodes_dict[actual].pred:
                    if j != 0 and j not in arrayQueue:
                        arrayQueue.append(j)
    for i in nodesId:
        print(f'Nodo: {i}, LS: {graphX.nodes_dict[i].ls}, LF: {graphX.nodes_dict[i].lf}')


    
    #backward

    #holguras
    for i in nodesId:
        sum = graphX.nodes_dict[i].ls - graphX.nodes_dict[i].es
        if sum != 0:
                graphX.nodes_dict[i].holgura = sum
    #holguras

    #CPM
    path = []
    start = []
    inicio = ""
    end = []
    final = ""

    path.append("inicio")
    for i in nodesId:   
        if i != "inicio":
            if graphX.nodes_dict[i].pred[0] == "inicio":
                start.append(i)
    auxiliaryArray: list = []

    for i in alterNodesId:
        for j in graphX.nodes_dict[i].pred:
            if j not in auxiliaryArray:
                auxiliaryArray.append(j)
    setAll = set(alterNodesId)
    setPred = set(auxiliaryArray)
    setLast = (setAll - setPred) 
    end = list(setLast)

    actualId = ""
    loop = True 
    for i in start:
            if graphX.nodes_dict[i].holgura == 0:
                actualId = i
                inicio = i
    while loop:
        sucChoose = []
        path.append(actualId)

        for i in nodesId:
            if actualId in graphX.nodes_dict[i].pred:
                sucChoose.append(i)
        if len(sucChoose)!=0:
            for i in sucChoose:
                if graphX.nodes_dict[i].holgura == 0:
                    actualId = i
        else:            
            final = actualId
            loop = False

    pathStr = ""
    totalDuration = graphX.nodes_dict["final"].es
    for i in path:
        if i != path[len(path)-1]:
            pathStr += i+" ==> "
        else:
            pathStr += i
    
    print(path)
    print(f'CPM: {pathStr}')
    print(f'TIEMPO DE DURACION DEL CP: {totalDuration}')
    print(f'INICIAL: { graphX.nodes_dict["inicio"].description }')
    print(f'FINAL: { graphX.nodes_dict["final"].description }')

    #CPM

    global graphX1 
    graphX1 = graphX

    fromList = []
    toList = []

    for i in nodesId:
        print(graphX.nodes_dict[i].pred)
        for j in graphX.nodes_dict[i].pred:
            fromList.append(j)
            toList.append(i)
    df = pd.DataFrame({
    'from': fromList,
    'to': toList
    })

    G = nx.from_pandas_edgelist(df, 'from', 'to')

    red_edges = []


    for i in range(len(path)):
        if i != 0:
            auxTup = (path[i-1],path[i])
            red_edges.append(auxTup)
    black_edges = [edge for edge in G.edges() if edge not in red_edges]
    print(red_edges)
    print(black_edges)
    edgesList = []
    colorList = []
    for i in red_edges:
        edgesList.append(i)
        colorList.append('red')
    for i in black_edges:
        edgesList.append(i)
        colorList.append('black')
    

    values = [('green' if node == 'inicio' or node == "final"  else ('blue')) for node in G.nodes()]
    # nx.draw(G,  arrows=True, with_labels=True, node_size = 1000, node_color = values)
    nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, edgelist=edgesList, edge_color=colorList, node_size = 1000, node_color = values)

    # nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, edgelist=black_edges,)
    plt.show()

    




def create():
    global graph 
    graph = Graph()
    global nodesId
    nodesId = []
    loop = "2"
    graph.add_node("inicio", "nodo inicio", 0, [])
    nodesId.append("inicio")

    while loop == "2":
        #if len(nodesId) < 1:
        #    print("Cree el nodo inicial")
        #    id = int(input("Ingrese el id de la actividad: "))
        #    descripcion = str(input("Ingrese la descripcion de la actividad: "))
        #    duracion = float(input("Ingrese la duracion de la actividad: "))
        #    predecesores = []
        #    graph.add_node(id, descripcion, duracion, predecesores)
        #    nodesId.append(id)

        #    ##id2 = int(input("Ingrese el id de la 2da actividad: "))
        #    ##descripcion2 = str(input("Ingrese la descripcion de la actividad: "))
        #    ##duracion2 = float(input("Ingrese la duracion de la actividad: "))      
        #    ##pre = [nodesId[0]]
        #    ##graph.nodes_dict[id].add_sucesor(id2)
##
        #    ##graph.add_node(id2, descripcion2, duracion2, pre)
        #    ##nodesId.append(id2)

        #    print("Está listo su grafo?: ")
        #    print ("1. Si")
        #    print ("2. No")
        #    loop = str(input("Ingrese 1 o 2 segun corresponda: "))


            id = input("Ingrese el id de la actividad (que no sea inicio): ")
            while id in nodesId:
                id = input("Existe una actividad con el ID indcado. Indique otro id: ")
            descripcion = str(input("Ingrese la descripcion de la actividad: "))
            duracion = input("Ingrese la duracion de la actividad: ")
            boo = check_user_input(duracion)
            while boo == False:
                duracion = input("Ingrese la duracion de la actividad: ")
                if duracion == '':
                    duracion = 's'
                boo = check_user_input(duracion)
            duracion = float(duracion)
            pre = input("Ingrese los ids de sus predecesores separados por comas: ")
            while "inicio" in pre.split(",") and len(pre.split(",")) > 1:
                pre = input("No puede tener como predecesores de un nodo al nodo 0 y a otro nodo. Ingrese los ids de sus predecesores separados por comas: ")
            pre = pre.split(",") 
            #pres = []
            #for p in pre:
            #    pres.append(int(p))
            
            valid = True
            while valid:
                a = True
                for p in pre:
                    if p not in nodesId not in nodesId:
                        a = False
                        break
                if a == False:
                    pre = input(f"No existe un nodo {p} en el grafo. Ingrese los ids de sus predecesores separados por comas: ")
                    pre = pre.split(",")
                    #pres = []   
                    #for p in pre:
                    #    pres.append(int(p))
                else:
                    valid = False

            graph.add_node(id, descripcion, duracion, pre)
            
            #for p in pres:
            #    print(p)
            #    graph.nodes_dict[p].add_sucesor(id)
            #    
            nodesId.append(id)
            print("Está listo su grafo?: ")
            print ("1. Si")
            print ("2. No")
            caso =["1","2"]
            loop = input("Ingrese 1 o 2 segun corresponda: ")
            while loop not in caso:
                loop = input("Ingrese 1 o 2 segun corresponda: ")
    auxiliaryArray: list = []

    for i in nodesId:
        for j in graph.nodes_dict[i].pred:
            if j not in auxiliaryArray:
                auxiliaryArray.append(j)
    setAll = set(nodesId)
    setPred = set(auxiliaryArray)
    setLast = (setAll - setPred) 
    end = list(setLast)
    graph.add_node("final", "nodo final", 0, end)
    nodesId.append("final")
    return graph










def main():
    opciones = [1,2,3,4,5,6]
    opciones2 = [1,2,3,4,5,6,7]
    print("\n")
    print("Bienvenido. En vista de que es su primera vez accediendo al programa, deberá armar un grafo con las actividades.")
    print("\n")
    graph = create()
    print("Su grafo se encuentra creado. Indique qué desea realizar: ")
    opcion = 1
    while opcion in opciones:

        print("\n")
        print("Menú")
        print("1. Verificar ruta crítica.")
        print("2. Añadir una nueva actividad al grafo")
        print("3. Verificar existencia de actividad en el grafo")
        print("4. Solicitar descripción de actividad en el grafo")
        print("5. Alterar descripción de actividad en el grafo")
        print("6. Alterar tiempo de duración de actividad en el grafo")
        print("7. Cerrar programa")
        
        opcion = int(input("Ingrese 1,2,3,4,5,6 ó 7 según corresponda: "))
        while opcion not in opciones2:
            opcion = int(input("Ingrese 1,2,3,4,5,6 ó 7 según corresponda: "))
        
        print("\n")
    
        if opcion == 1:
            cpm(graph)
        elif opcion == 2:
            loop = "2"

            while loop == "2":
                    id = input("Ingrese el id de la actividad: ")
                    while id in nodesId:
                        id = input("Existe una actividad con el ID indicado. Indique otro id: ")
                    descripcion = str(input("Ingrese la descripcion de la actividad: "))
                    duracion = input("Ingrese la duracion de la actividad: ")
                    boo = check_user_input(duracion)
                    while boo == False:
                        duracion = input("Ingrese la duracion de la actividad: ")
                        if duracion == '':
                            duracion = 's'
                        boo = check_user_input(duracion)
                    duracion = float(duracion)      
                    pre = input("Ingrese los ids de sus predecesores separados por comas: ")
                    while "inicio" in pre.split(",") and len(pre.split(",")) > 1:
                        pre = input("No puede tener como predecesores de un nodo al nodo inicio y a otro nodo. Ingrese los ids de sus predecesores separados por comas: ")
                    pre = pre.split(",") 
                    
                    valid = True
                    while valid:
                        a = True
                        for p in pre:
                            if p not in nodesId not in nodesId:
                                a = False
                                break
                        if a == False:
                            pre = input(f"No existe un nodo {p} en el grafo. Ingrese los ids de sus predecesores separados por comas: ")
                            pre = pre.split(",")
                        else:
                            valid = False

                    graph.add_node(id, descripcion, duracion, pre)
                    nodesId.append(id)
                    print("Está listo su grafo?: ")
                    print ("1. Si")
                    print ("2. No")
                    caso =["1","2"]
                    loop = input("Ingrese 1 o 2 segun corresponda: ")
                    while loop not in caso:
                        loop = input("Ingrese 1 o 2 segun corresponda: ")

        elif opcion == 3:
            verificar = input("Indique el ID del nodo que desea verificar se encuentra dentro del grafo: ")
            while verificar not in nodesId or verificar == "inicio":
                print("El ID indicado no se encuentra en el grafo o es 0.")
            else:
                print("El ID indicado se encuentra en el grafo.")


        elif opcion == 4:
            verificar = input("Indique el ID del nodo que desea verificar su descripción: ")
            while verificar not in nodesId or verificar == "inicio":
                print("El ID indicado no se encuentra en el grafo o es inicio.")
                verificar = input("Indique el ID del nodo que desea verificar su descripción: ")
            else:
                print("Descripción: ")
                print(graph.nodes_dict[verificar].description)
                print("Duración: ")
                print(graph.nodes_dict[verificar].duration)
        
        elif opcion == 5:
            verificar = input("Indique el ID del nodo que desea alterar su descripción: ")
            while verificar not in nodesId or verificar == "inicio":
                print("El ID indicado no se encuentra en el grafo o es inicio.")
                verificar = input("Indique el ID del nodo que desea verificar su descripción: ")
            else:
                print("Descripción anterior: ")
                print(graph.nodes_dict[verificar].description)
                descripcionN = input("Ingrese la nueva descripción: ")
                graph.nodes_dict[verificar].set_description(descripcionN)
        
        elif opcion == 6:
            verificar = input("Indique el ID del nodo que desea alterar su tiempo de duracion: ")
            while verificar not in nodesId or verificar == "inicio":
                print("El ID indicado no se encuentra en el grafo o es inicio.")
                verificar = input("Indique el ID del nodo que desea verificar su tiempo de duracion: ")
            else:
                print("Duración anterior: ")
                print(graph.nodes_dict[verificar].description)
                dura = input("Ingrese la nueva duracion de la actividad: ")
                boos = check_user_input(dura)
                while boos == False:
                    dura = input("Ingrese la duracion de la actividad: ")
                    if dura == '':
                        dura = 's'
                    boos = check_user_input(dura)
                dura = float(dura) 
                graph.nodes_dict[verificar].set_duration(dura)


    

    print('main proyecto')

















main()
