from snap import *
from sets import Set
import numpy as np
import random

#Breath First traversal for generating the content forest
def BFS(graph, start, PView, PShare):

    G = TNGraph.New()

    for u in start:
        G.AddNode(u)

    visited, queue = Set(start), start

    while queue:
        u = queue.pop(0)
        if graph.has_key(u):
            for v in graph[u].difference(visited):
                vval = random.uniform(0, 1)
                sval = random.uniform(0, 1)
                if vval >= PView[u][v] and sval >= PShare[u][v] :
                    G.AddNode(v)
                    G.AddEdge(u, v)
                    queue.append(v)
                elif vval >= PView[u][v]:
                    G.AddNode(v)
                    G.AddEdge(u, v)
                visited.add(v)
    return G

def readGraph(file, n, p, mean, std_dev, PView, PShare, content_count):
    G1 = LoadEdgeList(PUNGraph, file, 0, 1)
    n = G1.GetNodes()
    CmtyVt = TCnComV()

    #Getting the Community
    CommunityCNM(G1, CmtyVt)
    nodes = TIntV()
    for N in G1.GetNI(0).GetOutEdges():
        nodes.Add(N)

    G1 = GetSubGraph(G1, nodes)

    #Drawing the original Community Graph 
    #DrawGViz(G1, gvlDot, "graph1.png", "graph 1")

    Graph = {}
    for u in G1.Nodes():
        for v in u.GetOutEdges():
            if Graph.has_key(u.GetId()):
                Graph[u.GetId()].add(v)
            else:
                Graph.update({u.GetId() : Set([v])})

    #Initialize the probability Vectors.
    for i in range(0, n):
        PView += [[0 for j in range(0, n)]]
        PShare += [[0 for j in range(0, n)]]

    #Populating the probability vectors.
    for v in G1.Nodes():
        for u in v.GetOutEdges():
            id_src = v.GetId()
            id_dst = u
            view_prob = np.random.binomial(n, p, 1)[0]/(n * 1.0)
            share_prob = np.random.binomial(n, p, 1)[0]/(n * 1.0)
            PView[id_dst][id_src] = view_prob;
            PShare[id_dst][id_src] = share_prob

    #Content forest each entry in this array is a forest for some content.
    content_forest = []

    # 4039 * 0.148 #Number of cotent introduction point.
    content_intro_count = 60

    #Generating forest for each content.
    for i in range(0, content_count):

        #Generating the random introduction points i.e. the users who introduce the content.
        random_sample = random.sample(range(0, n), content_intro_count)

        #Generating the forest for a content
        content_forest.append(BFS(Graph, random_sample, PView, PShare))

    new_Graph = {}
    weight = {}
    G2 = TNGraph.New()
    for i in range(0, n):
        G2.AddNode(i)
    
    #Generating the inferred graph
    for cf in content_forest:
        for e in cf.Edges():
            if new_Graph.has_key(e.GetSrcNId()) and e.GetDstNId() in new_Graph[e.GetSrcNId()]:
                weight[str(e.GetSrcNId()) + ',' + str(e.GetDstNId())] = weight[str(e.GetSrcNId()) + ',' + str(e.GetDstNId())] + 1
            elif new_Graph.has_key(e.GetSrcNId()):
                new_Graph[e.GetSrcNId()].add(e.GetDstNId())
                weight.update({str(e.GetSrcNId()) + ',' + str(e.GetDstNId()) : 1})
                G2.AddEdge(e.GetSrcNId(), e.GetDstNId())
            else:
                new_Graph.update({e.GetSrcNId() : Set([e.GetDstNId()])})
                weight.update({str(e.GetSrcNId()) + ',' + str(e.GetDstNId()) : 1})
                G2.AddEdge(e.GetSrcNId(), e.GetDstNId())

    #Sum of Weights of all the neighbours of a vertex
    TWeight = {}
    for u in new_Graph.keys():
    	sum = 0
    	for v in new_Graph[u]:
    		sum += weight[str(u) + ',' + str(v)]
   		TWeight.update({u : sum})

   	#Calculating Edge Confidence
    for u in new_Graph.keys():
        for v in new_Graph[u]:
    		weight[str(u) + ',' + str(v)] = weight[str(u) + ',' + str(v)]/(TWeight[u] * 1.0)

    #calculating conf_threshold
    conf_thershold = mean + 0*std_dev

    #Generating the graph whose edges have conf_value greate than conf_threshold
    G3 = TUNGraph.New()
    nodes = []
    for u in new_Graph.keys():
        for v in new_Graph[u]:
            if weight[str(u) + ',' + str(v)] >= conf_thershold:
                if u not in nodes:
                    G3.AddNode(u)
                    nodes += [u]
                if v not in nodes:
                    G3.AddNode(v)
                    nodes += [v]
                G3.AddEdge(u, v)


    #Drawing the inferred Graph
    DrawGViz(G3, gvlDot, "graph3.png", "graph 2")

PView = []
PShare = []                

readGraph("facebook_ego_network.txt", 4039, 0.6,0.148, 0.07, PView, PShare, 30)
