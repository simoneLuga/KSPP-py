# Simone Lugaresi 0000970392
# Progetto Ricerca Operativa
# Note: alcune variabili nello pseudocodice sono inizilizzate a 0 o a 1, ma per come funziona il linguaggio in questo caso di py
# dato che alcuni valori di queste variabili vengono utilizzati come indici per matrici/array(esempio non posso inizializzare un arrai a 1 se
# poi il suo valore mi deve fare da indice per una matrice perchè mi perderei sempre la prima cella 0) sono stati inizilizzati in modo diverso
# riadattando di conseguenza il codice

import heapq
import numpy as np
import random
import time

#variabili utili al debug
showDate = False
showPath = False

#Variabili globali necessarie al funzionamento
K = 50
num_nodes = 500
minArch = 80
costForArch = 100
probabilityArch = 0.1
numEsecuzioni = 5


#classe di appoggio per la variabile Pred per memorizzare due dati
class tupla:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2
    
    def get_i(self):
        return self.var1
    
    def get_k(self):
        return self.var2
#raggruppa i dati in una funzione per facilitare la print
def printFunction(source, destination, graph, costs):
    print("Grafo:", graph)
    print("Costi:", costs)
    print("Source:", source)
    print("Destination:", destination)

def generate_random_graph(n, min_Arch, probArch):
    graph = [[] for _ in range(n)]
    
    for i in range(n):
        for j in range (n):
            if j!=i and random.random() < probArch:  # Probability of having an edge
                graph[i].append(j)
        if len(graph[i]) < min_Arch:
            i = i-1
    return graph

def generate_random_costs(G, maxVal):
    costs = [[0 for _ in range(len(G))] for _ in range(len(G))]
    for i in range(len(G)):
        for j in G[i]:
            costs[i][j] = random.randint(1,maxVal)
        costs[i][i] = 0    
    return costs

def KDijkstra(G,c,s,d,K):
    k_i = [-1]*len(G)
    heap = []
    heapq.heappush(heap, (s,0,-1,-1))
    i = s
    elle = [[0 for _ in range(K)] for _ in range(len(G))]
    Pred = [[0 for _ in range(K)] for _ in range(len(G))]
    while k_i[d] < K-1:
        (i, v, h, kPrimo) = heapq.heappop(heap)
        #importante che il vertice i abbia un massimo di soluzioni minori di K per evitare index out of bound
        if k_i[i] < K-1 :
            k_i[i] = k_i[i]+1
            elle[i][k_i[i]] = v
            Pred[i][k_i[i]] = tupla(h, kPrimo)
            for j in G[i]:
                val = elle[i][k_i[i]]+ c[i][j]
                heapq.heappush(heap, (j,val,i,k_i[i]))
    percorsi_finali = [[] for _ in range(K)]    
    perc = 0
    while perc < K :
        i = d
        ris = []
        ris.append(i)
        count = perc
        while i != s:
            temp = Pred[i][count]
            i = temp.get_i()
            count = temp.get_k()
            ris.append(i)
        percorsi_finali[perc] = ris[::-1]
        perc= perc+1
    return percorsi_finali

def BeginDijkstra(graph, costs, source, destination, K):

    start = time.time()
    percorsi_finali=KDijkstra(graph,costs,source,destination,K)
    finishKDijkstra = time.time()-start
    if showPath:
        for j, path in enumerate(percorsi_finali):
            print(f"Path {j+1}: {path}")
    if showDate:
        print("KDijkstra : " + str(finishKDijkstra)+"s")    
    return finishKDijkstra

def dataCollection():
    i = 0
    tempi = [[0 for _ in range(2)] for _ in range(numEsecuzioni+1)]
    while i < numEsecuzioni:
        graph = generate_random_graph(num_nodes, minArch,probabilityArch)
        costs = generate_random_costs(graph, costForArch)
        source = 0
        destination = 0
        while source == destination:
            source = random.randint(0, num_nodes - 1)
            destination = random.randint(0, num_nodes - 1) 
        if showDate:
            printFunction(source,destination,graph,costs)
        tempi[i][0] = BeginDijkstra(graph, costs, source, destination, K)
        i = i + 1
    sum = 0

    print("Dijkstra:")
    for i in range(0,numEsecuzioni):
        print(str(i+1) + " - " + "{:.6f}".format(tempi[i][0]))
        sum = sum + tempi[i][0]
    sum = sum / numEsecuzioni
    print("media - " + str(sum))

dataCollection()

