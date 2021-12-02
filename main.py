#import networkx as nx
##import matplotlib.pyplot as plt
#from networkx.algorithms import graph_hashing
from typing import ForwardRef
from node import *
from graph import *



graph : Graph
graphX: Graph
nodesId = []

# def forwardPass():


def cpm(graphVal: Graph):
    alterNodesId:list = []
    arrayQueue:list = []
    graphX = graphVal
    alterNodesId = nodesId
    #forward
    alterNodesId.pop(0)
    for i in alterNodesId:
            if graphX.nodes_dict[i].pred[0] == 0:
                arrayQueue.append(graphX.nodes_dict[i].id)
    while len(arrayQueue) !=0:
        predNodes:list = []
        actual = arrayQueue.pop()
        if graphX.nodes_dict[actual].pred[0] == 0:
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

    #backward
    
    #backward




        




def create():
    graph = Graph()
    loop = "2"
    graph.add_node(0, "nodo 0", 0, [])
    nodesId.append(0)

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

            id = int(input("Ingrese el id de la actividad: "))
            descripcion = str(input("Ingrese la descripcion de la actividad: "))
            duracion = float(input("Ingrese la duracion de la actividad: "))      
            pre = input("Ingrese los ids de sus predecesores separados por comas: ")
            pre= pre.split(",") 
            pres = []
            for p in pre:
                pres.append(int(p))
            valid = True
            while valid:
                a = True
                for p in pres:
                    if p not in nodesId:
                        a = False
                        break
                if a == False:
                    pre = input(f"No existe un nodo {p} en el grafo. Ingrese los ids de sus predecesores separados por comas: ")
                    pre = pre.split(",")
                    pres = []   
                    for p in pre:
                        pres.append(int(p))
                else:
                    valid = False

            graph.add_node(id, descripcion, duracion, pres)
            
            #for p in pres:
            #    print(p)
            #    graph.nodes_dict[p].add_sucesor(id)
            #    
            nodesId.append(id)
            print("Está listo su grafo?: ")
            print ("1. Si")
            print ("2. No")
            loop = input("Ingrese 1 o 2 segun corresponda: ")


    return graph










def main():
    graph = create()
    print(graph.nodes_dict)
    print(graph.nodes_dict.items())
    
    ## esto de abajo deberia ir en otro lado
    #sin_suc = []
    #for node in graph.nodes_dict.items():
    #        print(str(node[1].id)+" cantidad de nodos siguientes->"+str(len(node[1].suces)))
    #        if len(node[1].suces) == 0:
    #            sin_suc.append(node[1].id)
#
    #if len(sin_suc) == 1:
    #    return
    #else:
    #    print("No se puede tener un grafo abierto. Escoga el id de su nodo final: ")
    #    for n in sin_suc:
    #        print(n)
    #    nodo_final = input()
    #    sin_suc.remove(nodo_final)
    #    for n in sin_suc:
    #        graph.nodes_dict[n].add_sucesor(nodo_final)

    print('main proyecto')

















main()
