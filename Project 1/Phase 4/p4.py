import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
from itertools import groupby
from random import choice, sample
import math
import numpy as np


G = nx.read_edgelist('edges.csv', delimiter=',', nodetype=int, encoding="utf-8")
print G.number_of_nodes(),G.number_of_edges()


print "For Real World data"
avg_path_pl = nx.average_shortest_path_length(G)
print "Average path length :", avg_path_pl
print("Local clustering coeffiecent",nx.average_clustering(G)) #local
print("Global clustering coeffiecent",nx.transitivity(G))   #global
degrees = G.degree()
sum_of_edges = sum(degrees.values())
avg_deg=float((sum_of_edges))/float((G.number_of_nodes()))
print "average degree of graph ", avg_deg

#For Random Graph

print (sum_of_edges)
print G.number_of_nodes()


p =(avg_deg/float((G.number_of_nodes()-1)))
print "with p as :", p
Rand=nx.gnm_random_graph(G.number_of_nodes(),G.number_of_edges())
randl=graphs = list(nx.connected_component_subgraphs(Rand))
randg=randl[0]
print "For Random World data"
print "Average path length :",nx.average_shortest_path_length(randg)
print("Local clustering coeffiecent",nx.average_clustering(randg)) #local
print("Global clustering coeffiecent",nx.transitivity(randg))   #global

in_degrees  = randg.degree() 
x = sorted(set(in_degrees.values())) 
y = [in_degrees.values().count(xin) for xin in x]
plt.figure()
plt.plot(x,y,'ro-')
plt.legend(['degree-distribution'])
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('deg distribution Random Graph')
plt.savefig('deg distribution_Random Graph.pdf')
plt.show()
plt.close()



#small world
c=avg_deg
c = (c-2)/(c-1)
Co = c*3
Co = Co/4
print Co
p3=(1-p)
p3=p3*p3*p3
p=Co*p3
print "with p as :",p
n=G.number_of_nodes()
m=G.number_of_edges()
k=4
Small=nx.watts_strogatz_graph(n, k, p)
#print nx.number_connected_components(Small)
#print int(round(avg_deg))
print "For Small World data"
print "Average path length :",nx.average_shortest_path_length(Small)
print("Local clustering coeffiecent",nx.average_clustering(Small)) #local
print("Global clustering coeffiecent",nx.transitivity(Small))   #global
in_degrees  = Small.degree() 
# dictionary node:degree
x = sorted(set(in_degrees.values())) 
y = [in_degrees.values().count(xin) for xin in x]
plt.figure()
plt.plot(x,y,'ro-')
plt.legend(['degree-distribution'])
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('deg distribution Small World Graph')
plt.savefig('deg distribution_Small World.pdf')
plt.show()
plt.close()



PAM = nx.barabasi_albert_graph(n, int(round(avg_deg)))
print nx.number_connected_components(PAM)
print "For PAM data"
print "Average path length :",nx.average_shortest_path_length(PAM)
print("Local clustering coeffiecent",nx.average_clustering(PAM)) #local
print("Global clustering coeffiecent",nx.transitivity(PAM))   #global
in_degrees  = PAM.degree()
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
plt.title('deg distribution PAM')
plt.savefig('deg distribution_PAM.pdf')
plt.show()
plt.close()
 

