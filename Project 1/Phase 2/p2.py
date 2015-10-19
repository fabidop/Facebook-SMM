# -*- coding: cp1252 -*-
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
from itertools import groupby
from random import choice, sample
import math
import numpy as np


G = nx.read_edgelist('edges.csv', delimiter=',', nodetype=int, encoding="utf-8")

in_degrees  = G.degree() 
x = sorted(set(in_degrees.values())) 
y = [in_degrees.values().count(xin) for xin in x]
plt.figure()
plt.loglog(x,y,'ro-')
logx = np.log(x)
logy = np.log(y)
coeffs = np.polyfit(logx,logy,deg=1)
a = coeffs[0]
b = coeffs[1]
poly = np.poly1d(coeffs)
yfit = lambda x: np.exp(poly(np.log(x)))
plt.loglog(x,yfit(x))
plt.legend(['degree-distribution','Fit-line'])
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('deg distribution')
plt.savefig('deg distribution.pdf')
plt.show()
plt.close()

print "Exponents are b", a,"loga",b


#Find the number of bridges in the graph
#print list(nx.articulation_points(G))
nbr = len(list(nx.articulation_points(G)))
print "No of bridges are ",nbr

#Count the number of 3-cycles. In directed graphs, ignore the direction
cycls_3 = [c for c in nx.cycle_basis(G) if len(c)==3]
print "no of 3 cycles are ",len(cycls_3)

#Measure the graph’s diameter. In directed graphs, ignore the direction. 
print "Diameter of graph is",nx.diameter(G)

#Remove x% of edges randomly then:
#Compute the size |S| of the largest connected component
#Do for x from 1 to 100. Plot x versus |S|.
#If you have a directed graph, make it undirected

i=0
#for x in range(1,101):
Sampling =  G.copy()

edges=nx.edges(Sampling)
#print edges
Totale = len(edges)
remx=[]
samx=[]
#print nx.number_connected_components(Sampling) 
#print ("Total edges %d",Totale)
for i in range(1,101):
    x = (i*Totale)/100
    x = int(x)
    #print(x)
    rand_items = sample(edges, x)
    Sampling.remove_edges_from(rand_items)
    #print (len(nx.edges(Sampling)))
    remx.append(x)
    #print nx.number_connected_components(Sampling)
    samx.append(nx.number_connected_components(Sampling))
    Sampling = G.copy()
    edges=nx.edges(Sampling)
    #print (len(nx.edges(Sampling)))
#print remx,samx
plt.figure()
plt.plot(samx,'ro-')
#plt.plot(in_values,in_hist,'ro-') 
# in-degree
#plt.legend(['In-degree','Out-degree'])
plt.xlabel('X%')
plt.ylabel('Number of Components')
plt.title('Sampling vs No of Components')
plt.savefig('Sampling vs No of Components.pdf')
plt.show()
plt.close()
    










