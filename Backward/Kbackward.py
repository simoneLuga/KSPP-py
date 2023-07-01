# Simone Lugaresi 0000970392
# Progetto Ricerca Operativa
# Note: alcune variabili nello pseudocodice sono inizilizzate a 0 o a 1, ma per come funziona il linguaggio in questo caso di py
# dato che alcuni valori di queste variabili vengono utilizzati come indici per matrici/array(esempio non posso inizializzare un arrai a 1 se
# poi il suo valore mi deve fare da indice per una matrice perchè mi perderei sempre la prima cella 0) sono stati inizilizzati in modo diverso
# riadattando di conseguenza il codice

import math
import random
import time

#variabili utili al debug
showDate = False
showPath = True

#Variabili globali necessarie al funzionamento
K = 20
A = []
num_nodes = 100
minArch = 20
costForArch = 100
probabilityArch = 0.1
numEsecuzioni = 3
zssp = []
Pred = []
kBestSolution = []
kMatrice = []
source = 0
destination = 0
costs = []

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

def generate_random_graph_acyclic(n, min_Arch, probArch):
    graph = [[] for _ in range(n)]
    
    for i in range(n):
        for j in range (n):
            if j>i and random.random() < probArch:  # Probability of having an edge
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

#genera la lista di Archi necessaria per backward
def generate_A_from_graph(G):
    for i in range(0, len(G)-1):
        for j in range(0,len(G[i])):
            temp = [i,G[i][j]]
            A.append(temp)
    return A

def sppkBack(jPrimo,k):
    global source
    if jPrimo == source:
        if k == 0:
            return 0
        else:
            return math.inf
    if k <= kBestSolution[jPrimo] :
        return zssp[jPrimo][k]
    l = math.inf
    iPrimo = -1
    for (i,j) in A:
        # controlla che le chiamate ricorsive vengano effettuave solamente sugli archi di destinazione uguali a Jprimo
        if j == jPrimo: 
            lPrimo = sppkBack(i,kMatrice[i][j]) + costs[i][j]
            if lPrimo < l:
                l = lPrimo
                iPrimo = i
    Pred[jPrimo][k] = tupla(iPrimo, kMatrice[iPrimo][jPrimo])
    kMatrice[iPrimo][jPrimo] = kMatrice[iPrimo][jPrimo]+1
    kBestSolution[jPrimo] = k
    zssp[jPrimo][k] = l
    return zssp[jPrimo][k]

def solveSppkBack(G,c,s,d,K):
    for kPrimo in range(0, K) :
        zssp[d][kPrimo] = sppkBack(d,kPrimo)
    percorsi_finali = [[] for _ in range(K)]    
    perc = 0
    while perc < K :
        i = d
        ris = []
        ris.append(i)
        count = perc
        while i != s:
            temp = Pred[i][count]
            if isinstance(temp, tupla):
                i = temp.get_i()
                count = temp.get_k()
                if i == -1:
                    ris = []
                    break
                ris.append(i)
            else :
                i = i-1
        percorsi_finali[perc] = ris[::-1]

        perc= perc+1
    return percorsi_finali

def beginBackward(graph, costs, source, destination, K):
    start = time.time()
    percorsi_finali=solveSppkBack(graph,costs,source,destination,K)
    finishKbackWard= time.time()-start
    if showPath:
        for j, path in enumerate(percorsi_finali):
            print(f"Path {j+1}: {path}")
    if showDate:
        print("Kbackward : " + str(finishKbackWard)+"s")    
    return finishKbackWard

def dataCollection():
    i = 0
    tempi = [[0 for _ in range(2)] for _ in range(numEsecuzioni+1)]
    while i < numEsecuzioni:
        graph = generate_random_graph_acyclic(num_nodes, minArch,probabilityArch)
        global costs, source, destination
        costs = generate_random_costs(graph, costForArch)
        source = 0
        destination = 0
        while source >= destination :
            source = random.randint(0, num_nodes - 1)
            destination = random.randint(0, num_nodes - 1) 
        global zssp, Pred, kBestSolution, kMatrice
        zssp = [[0 for _ in range(K)] for _ in range(len(graph))]
        Pred =  [[0 for _ in range(K)] for _ in range(len(graph))]
        kBestSolution = [-1] * len(graph)
        kMatrice = [[0 for _ in range(len(graph))] for _ in range(len(graph))]
        A = generate_A_from_graph(graph)
        if showDate:
            printFunction(source,destination,graph,costs)

        tempi[i][0] = beginBackward(graph, costs, source, destination, K)
        i = i + 1
    sum = 0

    print("Backward:")
    for i in range(0,numEsecuzioni):
        print(str(i+1) + " - " + "{:.6f}".format(tempi[i][0]))
        sum = sum + tempi[i][0]
    sum = sum / numEsecuzioni
    print("media - " + str(sum))

dataCollection()
