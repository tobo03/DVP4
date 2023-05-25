from rdflib import URIRef, Namespace
import pandas as pd

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
amazonont = Namespace("https://purl.archive.org/purl/amazon/ontology#")

def alsoBuyTTL(df, graph):
    #Prepping the dataframe
    df = df[['asin', 'also_buy']]
    df = df[df['also_buy'].astype(str) != '[]']
    df = df.explode('also_buy')
    df = df.rename(columns = {'asin' : 'source', 'also_buy' : 'target'})
    df['edge'] = len(df) * ['also_buy']
    df = df[df['source'] != df['target']]
    df['source'] = df['source'].astype(str)
    df['target'] = df['target'].astype(str)

    #Conversion to TTL
    for index, row in df.iterrows():
        graph.add(triple = (URIRef(amazonent + row['source']),
                            URIRef(amazonont + row['edge']),
                            URIRef(amazonent + row['target'])))
    return graph
        
