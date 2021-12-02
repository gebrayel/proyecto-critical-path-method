#import networkx as nx
##import matplotlib.pyplot as plt
#from networkx.algorithms import graph_hashing
from typing import ForwardRef
from node import *
from graph import *
import sys


graph : Graph
graphX: Graph
nodesId = []

# def forwardPass():


def cpm(graphVal: Graph):
    alterNodesId:list = []
    arrayQueue:list = []
    graphX = graphVal
    for node in nodesId:
        alterNodesId.append(node)
    #forward
    alterNodesId.pop(0)
    for i in alterNodesId:
            if graphX.nodes_dict[i].pred[0] == "0":
                arrayQueue.append(graphX.nodes_dict[i].id)
    while len(arrayQueue) !=0:
        predNodes:list = []
        actual = arrayQueue.pop()
        if graphX.nodes_dict[actual].pred[0] == "0":
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
    print(alterNodesId)
    auxiliaryArray: list = []
    for i in alterNodesId:
        for j in graphX.nodes_dict[i].pred:
            if j not in auxiliaryArray:
                auxiliaryArray.append(j)
    setAll = set(alterNodesId)
    setPred = set(auxiliaryArray)
    setLast = (setAll - setPred) 
    firstList = list(setLast)
    for j in firstList:
        arrayQueue.append(j)
        index = alterNodesId.index(j)
        alterNodesId.pop(index)
    print(alterNodesId)
    print(nodesId)
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
    end = []

    for i in nodesId:
        if graphX.nodes_dict[i].pred[0] == 0:
            start.append(graphX.nodes_dict[graphX.nodes_dict[i].pred[0]])
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
    while loop:
        sucChoose = []
        path.append(actualId)

        for i in nodesId:
            if actualId in graphX.nodes_dict[i].pred:
                sucChoose.append(i)

        for i in sucChoose:
            if graphX.nodes_dict[i].holgura == 0:
                actualId = i
                break
        
        loop = False

    print(f'CPM: {((i+"==>" if i!=path[len(path)-1] else i) for i in path)}')
    print(f'{"INICIAL" if len(start)==1 else "INICIALES"}\n{((i+", " if i!=start[len(start)-1] else i) for i in start)}')
    print(f'{"FINAL" if len(start)==1 else "FINALES"}\n{((i+", " if i!=end[len(end)-1] else i) for i in end)}')


    #CPM


        




def create():
    graph = Graph()
    loop = "2"
    graph.add_node("0", "nodo 0", 0, [])
    nodesId.append("0")

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

            id = input("Ingrese el id de la actividad: ")
            descripcion = str(input("Ingrese la descripcion de la actividad: "))
            duracion = float(input("Ingrese la duracion de la actividad: "))      
            pre = input("Ingrese los ids de sus predecesores separados por comas: ")
            while "0" in pre.split(",") and len(pre.split(",")) > 1:
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
            loop = input("Ingrese 1 o 2 segun corresponda: ")

    return graph










def main():
    graph = create()


    cpm(graph)

    print('main proyecto')

















main()
