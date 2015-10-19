import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
from itertools import groupby
from random import choice, sample
import math
import numpy as np
from scipy import stats

G = nx.read_edgelist('edges.csv', delimiter=',', nodetype=int, encoding="utf-8")
rn=[]
in_degrees  = G.degree()
for k,v in in_degrees.items(): 
    if v <= 1:
        rn.append(k)
print len(rn)
print rn[0],rn[1],rn[2]
rS=G.copy()
print len(nx.edges(rS))

rS.remove_nodes_from(rn)
print len(nx.edges(rS))
print len(nx.edges(G))
    
#p3
#Compute the average local and global clustering coefficient of your graph.
print "Local Clustering coefficient",nx.average_clustering(G) #local
print "Local Clustering coefficient",nx.transitivity(G)   #global

#Compute PageRank, Eigenvector centrality, and degree centrality (if directed, compute in-degree)
#and report the top 10 nodes for each and their respective centrality values (10*10=100 values).
#Compute the rank correlation between each pair of these lists.

print ("Eigenvector")
centrality = nx.eigenvector_centrality(G)
#print centrality
#newA = dict(sorted(centrality.iteritems(), key=operator.itemgetter(1), reverse=True)[:5])
newE = sorted(centrality, key=centrality.get, reverse=True)[:10]
E=[]
for n in newE:
    print (n,centrality[n])
    E.append(centrality[n])
print ("pagerank")
pr = nx.pagerank(G)
newP = sorted(pr, key=pr.get, reverse=True)[:10]
P=[]
for n in newP:
    print (n,pr[n])
    P.append(centrality[n])
    
print ("degree")
dr = nx.degree_centrality(G)
newD = sorted(dr, key=dr.get, reverse=True)[:10]
D=[]
for n in newD:
    print (n,dr[n])
    D.append(centrality[n])
    
tau, p_value = stats.kendalltau(P, E)

print "Correlation between the centrality values of Pagerank and Eigenvector is",tau
tau, p_value = stats.kendalltau(E, D)

print "Correlation between the centrality values Degree and Eigenvector is",tau
tau, p_value = stats.kendalltau(D, P)

print "Correlation between the centrality values Pagerank and Degree is",tau

#Find the two most similar nodes using Jaccard similarity

print ("jaccard")
preds = nx.jaccard_coefficient(rS)
#print preds
max_so_far = 0
for u,v,p in preds:
    if p > max_so_far:
        max_so_far = p
        maxu = u
        maxv = v
print maxu,maxv,max_so_far

