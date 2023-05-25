from rdflib import URIRef, Namespace, Literal
import pandas as pd

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
schema = Namespace("https://schema.org/")

def nameTTL(df, graph):
    #Prepping the dataframe
    df = df[['asin', 'title']]
    df = df.rename(columns = {'asin' : 'source', 'title' : 'target'})
    df['edge'] = len(df) * ['name']
    df['source'] = df['source'].astype(str)
    df['target'] = df['target'].astype(str)

    #Conversion to TTL
    for index, row in df.iterrows():
        graph.add(triple = (URIRef(amazonent + row['source']),
                            URIRef(schema + row['edge']),
                            Literal(row['target'])))
    return graph
        
