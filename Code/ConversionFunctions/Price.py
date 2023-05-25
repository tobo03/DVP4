from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import XSD
import pandas as pd
import re

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
amazonont = Namespace("https://purl.archive.org/purl/amazon/ontology#")

regex = r"\$(\d+(\.\d{1,2})?)"

def get_price(P):
    L = re.findall(regex, P)
    vals = [float(a[0]) for a in L]
    if len(vals) == 0:
        return ''
    return round(sum(vals) / len(vals), 2)


def priceTTL(df, graph):
    #Prepping the dataframe
    df = df[['asin', 'price']]
    df = df.rename(columns = {'asin' : 'source', 'price' : 'target'})
    df['edge'] = len(df) * ['price']
    df['price'] = [get_price(p) for p in df['price']]
    df = df[df['price'].astype(str) != '']
    df['source'] = df['source'].astype(str)

    #Conversion to TTL
    for index, row in df.iterrows():
        graph.add(triple = (URIRef(amazonent + row['source']),
                            URIRef(amazonont + row['edge']),
                            Literal(row["target"], datatype=XSD.double)))
    return graph
        
