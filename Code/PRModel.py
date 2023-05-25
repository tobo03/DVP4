import json
import time
from rdflib import Graph, Namespace
import pandas as pd
from functools import lru_cache
from UtilFunctions.subsetKG import subsetCreation

g = Graph()

subsetCreation(g, withAuthor = True)

# Define the namespaces used in the .ttl file
amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
amazonont = Namespace("https://purl.archive.org/purl/amazon/ontology#")
amazoncat = Namespace("https://purl.archive.org/purl/amazon/categories#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
schema = Namespace("http://schema.org/")
wds = Namespace("http://www.wikidata.org/entity/statement/")

namespaces = {"amazonent": amazonent, "amazonont": amazonont, "xsd": xsd, "schema": schema, "rdfs": rdfs, "amazoncat": amazoncat, "wds": wds}

@lru_cache(maxsize=1024)
def query_all(id):
# Define the SPARQL query
    try:
        Q_also_buy = "SELECT ?node WHERE {{amazonent:" + id + " amazonont:also_buy ?node} UNION {?node amazonont:also_buy amazonent:" + id + "}}  "
        res_also_buy = g.query(Q_also_buy, initNs=namespaces)
        list_also_buy = [row[0].split("#")[-1] for row in res_also_buy]
        
        Q_also_view = "SELECT ?node WHERE {{amazonent:" + id + " amazonont:also_view ?node} UNION {?node amazonont:also_view amazonent:" + id + "}}  "
        res_also_view = g.query(Q_also_view, initNs=namespaces)
        list_also_view = [row[0].split("#")[-1] for row in res_also_view]

        Q_cat = "SELECT ?node WHERE {{amazonent:" + id + " schema:category ?node} UNION {?node schema:category amazoncat:" + id + "}}  "
        res_cat = g.query(Q_cat, initNs=namespaces)
        list_cat = [row[0].split("#")[-1] for row in res_cat]

        Q_brand = "SELECT ?node WHERE {{amazonent:" + id + " schema:brand ?node} UNION {?node schema:brand amazonent:" + id + "}}  "
        res_brand = g.query(Q_brand, initNs=namespaces)
        list_brand = [row[0].split("#")[-1] for row in res_brand]

        Q_author = "SELECT ?node WHERE {{amazonent:" + id + " schema:author ?node} UNION {?node schema:author amazonent:" + id + "}}  "
        res_author = g.query(Q_author, initNs=namespaces)
        list_author = [row[0].split("#")[-1] for row in res_author]

        Q_itemReviewed = "SELECT ?node WHERE {{amazonent:" + id + " schema:itemReviewed ?node} UNION {?node schema:itemReviewed amazonent:" + id + "}}  "
        res_itemReviewed = g.query(Q_itemReviewed, initNs=namespaces)
        list_itemReviewed = [row[0].split("#")[-1] for row in res_itemReviewed]

        Q_subcat = "SELECT ?node WHERE {{amazoncat:" + id + " wds:instance_of ?node} UNION {?node wds:instance_of amazoncat:" + id + "}}  "
        res_subcat = g.query(Q_subcat, initNs=namespaces)
        list_subcat = [row[0].split("#")[-1] for row in res_subcat]

        return list_also_buy + list_also_view + list_cat + list_brand + list_author + list_itemReviewed + list_subcat
    except:
        print(id, "has error output")
        return []

#Safety log
log = ""

#Query for all nodes
def query_all_nodes():
    all_nodes = "SELECT DISTINCT ?n WHERE {{?n ?p ?o } UNION {?s ?p ?n}}" 
    Q2 = g.query(all_nodes, initNs=namespaces)
    list_all_nodes = [i[0].split("#")[-1] for i in Q2]
    return list_all_nodes

all_nodes = query_all_nodes()

#Alpha, beta and S are defined
S = all_nodes
weights = {}
alpha = 0.2
beta = 1-alpha

S_len = len(S)

for s in S:
    weights[s] = 1/S_len

S_multiplier = alpha / S_len

t1 = time.time()

#PR
for i in range(100):
    
    print('====','i:', i, '====')
    log += f"==== i: {i}====\n"

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    log += current_time

    print('len:', len(weights))
    log += f"len: {len(weights)}\n"
    newWeights = {}

    for s in S:
        newWeights[s] = S_multiplier

    for weight in list(weights):
        outs = query_all(weight)
        
        if outs != []:
            
            multiplier = beta / len(outs)
            val = weights[weight] * multiplier

            for out in outs:
                try:
                    newWeights[out] += val
                except:
                    newWeights[out] = val
        
        else:    
            for s in S:
                try:
                    newWeights[s] += weights[weight] * (beta / S_len)
                except:
                    newWeights[s] = weights[weight] * (beta / S_len)
    print('sum:', sum([newWeights[weight] for weight in newWeights]))
    try:
        temp = 0
        #Check for no changes of 5%, if yes then stable and break the loop, if no then unstable and keeps going
        for key in list(newWeights):
            if not (weights[key] *.95 < newWeights[key] and newWeights[key] < weights[key] * 1.05):
                temp += 1
        if temp == 0: 
            print('is stable')
            log += "is stable\n"
            break
        print("# unstable:",temp)
        log += f"# unstable: {temp}\n"    
    except:
        print('not done registering')
        log += "not done registering\n"

    weights = newWeights

    if time.time() - t1 > 3600:
        #Save each iterations weights.
        with open(f"weights-PR-{i}.json", "w") as outfile:
            json.dump(weights, outfile)
        
        print("saved at", i)
        log += f"saved at: {i}\n"

        #Save each log
        text_file = open("PR.txt", "w")
        n = text_file.write(log)
        text_file.close()

        t1 = time.time()


#Save final weights as .JSON file.
with open("weights-PR-done.json", "w") as outfile:
    json.dump(weights, outfile)

#Save final log as .txt file.
text_file = open("log-PR-done.txt", "w")
n = text_file.write(log)
text_file.close()