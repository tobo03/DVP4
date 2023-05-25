from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDFS

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
schema = Namespace("https://schema.org/")

def brandClass(df, graph):
    for brand in list(df['brand'].unique()):
        graph.add(triple = (URIRef(brand),
                            RDFS.Class,
                            URIRef(schema + "Organization")))
    return graph 
   
def productClass(df, graph):
    for asin in list(df['asin'].unique()):
        graph.add(triple = (URIRef(asin),
                            RDFS.Class,
                            URIRef(schema + "Product")))
    return graph

def reviewClass(df, graph):
    for review in list(df['index'].unique()):
        graph.add(triple = (URIRef(review),
                            RDFS.Class,
                            URIRef(schema + "Review")))
    return graph

def personClass(df, graph):
    for person in list(df['reviewerID'].unique()):
        graph.add(triple = (URIRef(person),
                            RDFS.Class,
                            URIRef(schema + "Person")))
    return graph