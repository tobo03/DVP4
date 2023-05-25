from rdflib import URIRef, Namespace
import pandas as pd

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
amazoncat = Namespace("https://purl.archive.org/purl/amazon/ontology#")
schema = Namespace("http://schema.org/")

def categoryTTL(df, graph):
    #Prepping the dataframe
    df = df[['asin', 'category']]
    df = df[df['category'].astype(str) != '[]'].reset_index(drop=True)
    df['category'] = [f'{a[-1]}-{a[-2]}' for a in df['category']]
    df = df.rename(columns = {'asin' : 'source', 'category' : 'target'})
    df['edge'] = len(df) * ['category']
    df['source'] = df['source'].astype(str)
    df['target'] = df['target'].astype(str)

    #Conversion to TTL
    for index, row in df.iterrows():
        graph.add(triple = (URIRef(amazonent + row['source']),
                            URIRef(schema + row['edge']),
                            URIRef(amazoncat + row['target'])))
    return graph
        
