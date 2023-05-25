from rdflib import URIRef, Namespace, Literal
from rdflib.namespace import XSD
import pandas as pd
from datetime import datetime

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
schema = Namespace("https://schema.org/")

def datePublishedTTL(df, graph):
    #Prepping the dataframe
    df = df[['index','unixReviewTime']]
    df = df.rename(columns={'index' : 'source', 'unixReviewTime' : 'target'})
    df['edge'] = len(df) * ['datePublished']
    df['source'] = df['source'].astype(str)

    #Conversion to TTL
    for index, row in df.iterrows():
        graph.add(triple = (URIRef(amazonent + row['source']),
                            URIRef(schema + row['edge']),
                            Literal(datetime.fromtimestamp(row['target']).date(), datatype = XSD.dateTime)))
    return graph
        
