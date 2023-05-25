from rdflib import URIRef, Namespace
import pandas as pd

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
schema = Namespace("https://schema.org/")

def brandTTL(df, graph):
    #Prepping the dataframe
    df = df[['asin', 'brand']]
    df = df[df['brand'] != '']
    df['brand'] = df['brand'].str.lower()
    df = df[df['brand'] != 'unknown']
    df = df.rename(columns = {'asin' : 'source', 'brand' : 'target'})
    df['edge'] = len(df) * ['brand']
    df['source'] = df['source'].astype(str)
    df['target'] = df['target'].astype(str)

    #Conversion to TTL
    for index, row in df.iterrows():
        graph.add(triple = (URIRef(amazonent + row['source']),
                            URIRef(schema + row['edge']),
                            URIRef(amazonent + row['target'])))
    return graph
        
