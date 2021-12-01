import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import graph_hashing
from node import *
from graph import *



graph : Graph

nodesId = []


def create():
    graph = Graph()
    loop = "2"
    while loop == "2":
        if len(nodesId) < 2:
            print("Cree el nodo inicial")
            id = int(input("Ingrese el id de la actividad: "))
            descripcion = str(input("Ingrese la descripcion de la actividad: "))
            duracion = float(input("Ingrese la duracion de la actividad: "))
            predecesores = []
            graph.add_node(id, descripcion, duracion, predecesores)
            nodesId.append(id)

            id2 = int(input("Ingrese el id de la 2da actividad: "))
            descripcion2 = str(input("Ingrese la descripcion de la actividad: "))
            duracion2 = float(input("Ingrese la duracion de la actividad: "))      
            pre = [nodesId[0]]
            graph.nodes_dict[id].add_sucesor(id2)

            graph.add_node(id2, descripcion2, duracion2, pre)
            nodesId.append(id2)
            print("Está listo su grafo?: ")
            print ("1. Si")
            print ("2. No")
            loop = str(input("Ingrese 1 o 2 segun corresponda: "))


        else:
            id = int(input("Ingrese el id de la actividad: "))
            descripcion = str(input("Ingrese la descripcion de la actividad: "))
            duracion = float(input("Ingrese la duracion de la actividad: "))      
            pre = input("Ingrese los ids de sus predecesores separados por comas: ") 

            graph.add_node(id, descripcion, duracion, pre.split(","))
            for p in pre:
                graph.nodes_dict[p].add_sucesor(id)
                
            nodesId.append(id)
            print("Está listo su grafo?: ")
            print ("1. Si")
            print ("2. No")
            loop = input("Ingrese 1 o 2 segun corresponda: ")

        ## esto de abajo deberia ir en otro lado
        sin_suc = []

        for node in graph.nodes_dict.items():
            if len(node[1].suces) == 0:
                sin_suc.append(node[1].id)

        if len(sin_suc) == 1:
            return
        else:
            print("No se puede tener un grafo abierto. Escoga el id de su nodo final: ")
            for n in sin_suc:
                print(n)
            nodo_final = input()
            sin_suc.remove(nodo_final)
            for n in sin_suc:
                graph.nodes_dict[n].add_sucesor(nodo_final)
            


    return










def main():
    create()
    print('main proyecto')

















main()
