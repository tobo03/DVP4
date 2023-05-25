from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import XSD
import pandas as pd
from datetime import datetime

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
schema = Namespace("https://schema.org/")

def reviewBodyTTL(df, graph):
    #Prepping the dataframe
    df = df[['index','resviewText']]
    df = df.rename(columns={'index' : 'source', 'reviewText' : 'target'})
    df['edge'] = len(df) * ['reviewBody']
    df['source'] = df['source'].astype(str)
    df['target'] = df['target'].astype(str)

    #Conversion to TTL
    for index, row in df.iterrows():
        graph.add(triple = (URIRef(amazonent + row['source']),
                            URIRef(schema + row['edge']),
                            Literal(row['target'])))
    return graph
        
