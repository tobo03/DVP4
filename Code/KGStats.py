from rdflib import Graph, Namespace
import networkx as nx
import pandas as pd
import statistics

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
amazonont = Namespace("https://purl.archive.org/purl/amazon/ontology#")
amazoncat = Namespace("https://purl.archive.org/purl/amazon/categories#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
schema = Namespace("http://schema.org/")
wds = Namespace("http://www.wikidata.org/entity/statement/")

g = Graph()
G = nx.MultiDiGraph()

g.bind("amazonent", amazonent)
g.bind("amazonont", amazonont)
g.bind("amazoncat", amazoncat)
g.bind("xsd", xsd)
g.bind("rdfs", rdfs)
g.bind("schema", schema)
g.bind("wds", wds)

namespaces = {"amazonent": amazonent, "amazonont": amazonont, "xsd": xsd, "schema": schema, "rdfs": rdfs, "amazoncat": amazoncat, "wds": wds}


g.parse(r'Final_kg.ttl', format = "ttl")


for s, p, o in g:
    G.add_node(s)
    G.add_node(o)
    G.add_edge(s, o, label=p)

print("NETWORKX GRAPH DONE")

query_unique_nodes = "SELECT DISTINCT ?n WHERE {{?n ?p ?o } UNION {?s ?p ?n}}" 

print(len(list(g.query(query_unique_nodes, initNs=namespaces))))

number_of_triples = len(G.edges)
print("Number of triples:", number_of_triples)

unique_subject = len(G.nodes)
print("Number of unique subjects:", unique_subject)

query_unique_object = "SELECT DISTINCT ?object WHERE {?source ?pred ?object}"
Q = g.query(query_unique_object, initNs=namespaces)
unique_object = []
for i in Q:
    unique_object.append(i)
unique_object = len(unique_object)
print("Number of unique objects:", unique_object)

indegrees = dict(G.in_degree())
avg_indegree = sum(indegrees.values()) / len(indegrees)
print("Average Indegree:", avg_indegree)

indegrees = dict(G.in_degree())
print("Median Indegree", statistics.median([indegrees[key] for key in indegrees]))

outdegrees = dict(G.out_degree())
avg_outdegree = sum(outdegrees.values()) / len(outdegrees)
print("Average Outdegree:", avg_outdegree)

outdegrees = dict(G.out_degree())
print("Median Outdegree", statistics.median([outdegrees[key] for key in outdegrees]))