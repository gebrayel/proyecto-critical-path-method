from node import *
from graph import *
import sys
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt


graph : Graph
newGraph : Graph
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

    print("\n")
    nodosHolguraId = []
    for m in nodesId:
        if graph.nodes_dict[m].holgura != 0:
            nodosHolguraId.append(m)

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
    
    print(f'CPM: {pathStr}')
    print(f'TIEMPO DE DURACION DEL CP: {totalDuration}')
    print(f'INICIAL: { graphX.nodes_dict["inicio"].description }')
    print(f'FINAL: { graphX.nodes_dict["final"].description }')
    print("\n")
    print("Nodos con holgura")
    for n in nodosHolguraId:
        print(f"Nodo: {n}, Holgura: {graph.nodes_dict[n].holgura}")

    
    #CPM

    global graphX1 
    graphX1 = graphX

    fromList = []
    toList = []

    for i in nodesId:
        for j in graphX.nodes_dict[i].pred:
            fromList.append(j)
            toList.append(i)
    df = pd.DataFrame({
    'from': fromList,
    'to': toList
    })
    
    G = nx.convert_matrix.from_pandas_edgelist(df, 'from', 'to')
    red_edges = []


    for i in range(len(path)):
        if i != 0:
            auxTup = (path[i-1],path[i])
            red_edges.append(auxTup)
    black_edges = [edge for edge in G.edges() if edge not in red_edges]
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
    descripcionIn = str(input("Ingrese la descripcion de la actividad inicio: "))
    while descripcionIn.isspace() or not descripcionIn:
        descripcionIn = str(input("Ingrese la descripcion de la actividad inicio no vacia: "))
    graph.add_node("inicio", descripcionIn, 0, [])
    nodesId.append("inicio")

    while loop == "2":


            id = input("Ingrese el id de la actividad (que no sea inicio): ")
            while id in nodesId or id.isspace() or not id:
                id = input("Existe una actividad con el ID indicado o esta vacio. Indique otro id: ")
            descripcion = str(input("Ingrese la descripcion de la actividad: "))
            while descripcion.isspace() or not descripcion:
                descripcion = str(input("Ingrese la descripcion de la actividad no vacia: "))
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
            
            
            nodesId.append(id)
            print("Esta listo su grafo?: ")
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
    descripcionFin = str(input("Ingrese la descripcion de la actividad final: "))
    while descripcionFin.isspace() or not descripcionFin:
        descripcionFin = str(input("Ingrese la descripcion de la actividad final no vacia: "))
    graph.add_node("final", descripcionFin, 0, end)
    nodesId.append("final")
    return graph










def main():
    opciones = ["1","2","3","4","5","6","7","8"]
    opciones2 = ["1","2","3","4","5","6","7","8","9"]
    print("\n")
    print("Bienvenido. En vista de que es su primera vez accediendo al programa, debera armar un grafo con las actividades.")
    print("\n")
    graph = create()
    #print("Su grafo se encuentra creado. Indique qué desea realizar: ")
    opcion = "1"
    while opcion in opciones:
        print("\n")
        print("Su grafo se encuentra creado. Indique que desea realizar: ")
        print("\n")
        print("Menu")
        print("1. Verificar ruta critica.")
        print("2. Añadir una nueva actividad al grafo")
        print("3. Verificar existencia de actividad en el grafo")
        print("4. Solicitar descripcion de actividad en el grafo")
        print("5. Alterar descripcion de actividad en el grafo")
        print("6. Alterar tiempo de duracion de actividad en el grafo")
        print("7. Borrar el grafo existente y crear uno nuevo")
        print("8. Mostrar grafo")
        print("9. Cerrar programa")
        
        opcion = (input("Ingrese 1,2,3,4,5,6,7,8 u 9 segun corresponda: "))
        while opcion not in opciones2:
            opcion = (input("Ingrese 1,2,3,4,5,6,7,8 u 9 segun corresponda: "))
        
        print("\n")
    
        if opcion == "1":
            cpm(graph)
        elif opcion == "2":
            loop = "2"

            while loop == "2":
                    id = input("Ingrese el id de la actividad: ")
                    while id in nodesId or id.isspace() or not id:
                        id = input("Existe una actividad con el ID indicado o es vacio. Indique otro id: ")
                    descripcion = str(input("Ingrese la descripcion de la actividad: "))
                    while descripcion.isspace() or not descripcion:
                        descripcion = str(input("Ingrese la descripcion de la actividad no vacia: "))
                    duracion = input("Ingrese la duracion de la actividad: ")
                    boo = check_user_input(duracion)
                    while boo == False:
                        duracion = input("Ingrese la duracion de la actividad: ")
                        if duracion == '':
                            duracion = 's'
                        boo = check_user_input(duracion)
                    duracion = float(duracion)      
                    pre = input("Ingrese los ids de sus predecesores separados por comas. Si quiere añadir de predecesor al inicio ingrese 'inicio': ")
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

                    while "final" in pre:
                        pre = input("No puede tener como predecesores de un nodo al nodo final. Ingrese los ids de sus predecesores separados por comas: ")
                        pre = pre.split(",")

                    graph.add_node(id, descripcion, duracion, pre)
                    nodesId.append(id)
                    print("Está listo su grafo?: ")
                    print ("1. Si")
                    print ("2. No")
                    caso =["1","2"]
                    loop = input("Ingrese 1 o 2 segun corresponda: ")
                    while loop not in caso:
                        loop = input("Ingrese 1 o 2 segun corresponda: ")

            auxiliaryArray = []
            alterNodesNow = []
            for i in nodesId:
                alterNodesNow.append(i)
            alterNodesNow.pop(0)
            ind = alterNodesNow.index("final")
            alterNodesNow.pop(ind)
            for i in alterNodesNow:
                for j in graph.nodes_dict[i].pred:
                    if j not in auxiliaryArray:
                        auxiliaryArray.append(j)
            setAll = set(alterNodesNow)
            setPred = set(auxiliaryArray)
            setLast = (setAll - setPred) 
            end = list(setLast)
            graph.nodes_dict["final"].pred = end
            inde = nodesId.index("final")
            nodesId.pop(inde)
            nodesId.append("final")


        elif opcion == "3":
            verificar = input("Indique el ID del nodo que desea verificar se encuentra dentro del grafo: ")
            while verificar not in nodesId or verificar == "inicio":
                print("El ID indicado no se encuentra en el grafo o es 0.")
            else:
                print("El ID indicado se encuentra en el grafo.")


        elif opcion == "4":
            verificar = input("Indique el ID del nodo que desea verificar su descripcion: ")
            while verificar not in nodesId or verificar == "inicio":
                print("El ID indicado no se encuentra en el grafo o es inicio.")
                verificar = input("Indique el ID del nodo que desea verificar su descripcion: ")
            else:
                print("Descripcion: ")
                print(graph.nodes_dict[verificar].description)
                print("Duracion: ")
                print(graph.nodes_dict[verificar].duration)
        
        elif opcion == "5":
            verificar = input("Indique el ID del nodo que desea alterar su descripcion: ")
            while verificar not in nodesId :
                print("El ID indicado no se encuentra en el grafo.")
                verificar = input("Indique el ID del nodo que desea verificar su descripcion: ")
            else:
                print("Descripcion anterior: ")
                print(graph.nodes_dict[verificar].description)
                descripcionN = input("Ingrese la nueva descripcion: ")
                while descripcionN.isspace() or not descripcionN:
                    descripcionN = input("Ingrese la nueva descripcion no vacia: ")
                graph.nodes_dict[verificar].set_description(descripcionN)
        
        elif opcion == "6":
            verificar = input("Indique el ID del nodo que desea alterar su tiempo de duracion: ")
            while verificar not in nodesId or verificar == "inicio":
                print("El ID indicado no se encuentra en el grafo o es inicio.")
                verificar = input("Indique el ID del nodo que desea verificar su tiempo de duracion: ")
            else:
                print("Duracion anterior: ")
                print(graph.nodes_dict[verificar].duration)
                dura = input("Ingrese la nueva duracion de la actividad: ")
                boos = check_user_input(dura)
                while boos == False:
                    dura = input("Ingrese la duracion de la actividad: ")
                    if dura == '':
                        dura = 's'
                    boos = check_user_input(dura)
                dura = float(dura) 
                graph.nodes_dict[verificar].set_duration(dura)

        elif opcion == "7":
            newGraph = Graph()
            graph = newGraph
            
            print("Arme su nuevo grafo con sus actividades")
            print("\n")
            graph = create()
        elif opcion == "8":
            fromList = []
            toList = []

            for i in nodesId:
                for j in graph.nodes_dict[i].pred:
                    fromList.append(j)
                    toList.append(i)
            df = pd.DataFrame({
            'from': fromList,
            'to': toList
            })
            
            G = nx.convert_matrix.from_pandas_edgelist(df, 'from', 'to')


            values = [('green' if node == 'inicio' or node == "final"  else ('blue')) for node in G.nodes()]
            # nx.draw(G,  arrows=True, with_labels=True, node_size = 1000, node_color = values)
            nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, node_size = 1000, node_color = values)

            # nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, edgelist=black_edges,)
            plt.show()




main()
