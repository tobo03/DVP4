from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS
from functools import lru_cache

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
amazonont = Namespace("https://purl.archive.org/purl/amazon/ontology#")
amazoncat = Namespace("https://purl.archive.org/purl/amazon/categories#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
schema = Namespace("http://schema.org/")
wds = Namespace("http://www.wikidata.org/entity/statement/")
g = Graph()
g_subset = Graph()

#Function to clean  
def clean_res(res):
    return ((res)).split('#')[-1]

    #Find all sub categories of a given category
@lru_cache
def sub_cat(cat, namespaces, graph, graph_subset):
    q ="SELECT ?subcat WHERE {amazoncat:"+cat+" wds:instance_of ?subcat}"
    res = (graph.query(q, initNs=namespaces))
    cleaned_res = (str(list(res)[0]).split('#')[-1][:-4])

    if cleaned_res != "Sports_and_Outdoors":
        graph_subset.add((amazoncat['%s'] %cat, wds['%s'] %"instance_of", amazoncat['%s'] %cleaned_res))
        return sub_cat(cleaned_res)

def subsetCreation(g, withAuthor):
    #Empty rdflib graphs


    #Load Final Knowledge Graph
    g.parse(r'Final_KG.ttl', format = "ttl")

    #Define namespaces
    amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
    amazonont = Namespace("https://purl.archive.org/purl/amazon/ontology#")
    amazoncat = Namespace("https://purl.archive.org/purl/amazon/categories#")
    xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    schema = Namespace("http://schema.org/")
    wds = Namespace("http://www.wikidata.org/entity/statement/")

    #Namespaces for querying
    namespaces = {"amazonent": amazonent, "amazonont": amazonont, "xsd": xsd, "schema": schema, "rdfs": rdfs, "amazoncat": amazoncat, "wds": wds}

    #Main query for subseting the knowledge graph
    if withAuthor == True:
        query ="""
        SELECT ?review ?unixTime ?prod ?brand ?category ?person
        WHERE {
        ?review amazonont:unixTime ?unixTime .
        ?review schema:itemReviewed ?prod .
        ?prod schema:brand ?brand .
        ?prod schema:category ?category .
        ?person schema:author ?review 
        }
        ORDER BY DESC(?unixTime)
        LIMIT 10000
        """
    if withAuthor == False:
        query = """
        SELECT ?review ?unixTime ?prod ?brand ?category ?person
        WHERE {
        ?review amazonont:unixTime ?unixTime .
        ?review schema:itemReviewed ?prod .
        ?prod schema:brand ?brand .
        ?prod schema:category ?category .
        ?person schema:author ?review .
        FILTER NOT EXISTS {amazonent:A3NP2EH6Z5MTTS schema:author ?review}
        }
        ORDER BY DESC(?unixTime)
        LIMIT 10000
        """




    #Query for cleaning all nodes and adding them to the subset graph.    
    results = g.query(query, initNs=namespaces)
    for row in results:
        clean_review = clean_res(row[0])
        clean_prod = clean_res(row[2])
        clean_brand = clean_res(row[3])
        clean_cat = clean_res(row[4])
        clean_author = clean_res(row[5])

        also_buy_Q = "SELECT ?also_buy WHERE {amazonent:"+clean_prod+" amazonont:also_buy ?also_buy}"
        also_buy_res = g.query(also_buy_Q, initNs=namespaces)
        for also_buy_row in also_buy_res:
            clean_also_buy = clean_res(also_buy_row[0])
            g_subset.add((amazonent['%s'] %clean_prod, amazonont['%s'] %"also_buy", amazonent['%s'] %clean_also_buy))
    
        also_view_Q = "SELECT ?also_view WHERE {amazonent:"+clean_prod+" amazonont:also_view ?also_view}"
        also_view_res = g.query(also_view_Q, initNs=namespaces)
        for also_view_row in also_view_res:
            clean_also_view = clean_res(also_view_row[0])
            g_subset.add((amazonent['%s'] %clean_prod, amazonont['%s'] %"also_view", amazonent['%s'] %clean_also_view))

        g_subset.add((amazonent['%s'] %clean_review, schema['%s'] %"itemReviewed", amazonent['%s'] %clean_prod))

        g_subset.add((amazonent['%s'] %clean_prod, schema['%s'] %"brand", amazonent['%s'] %clean_brand))

        g_subset.add((amazonent['%s'] %clean_prod, schema['%s'] %"category", amazoncat['%s'] %clean_cat))

        g_subset.add((amazonent['%s'] %clean_author, schema['%s'] %"author", amazonent['%s'] %clean_review))

        sub_cat(clean_cat, namespaces = namespaces, graph = g, graph_subset = g_subset)

#Serialize the subset graph.
    return g_subset
