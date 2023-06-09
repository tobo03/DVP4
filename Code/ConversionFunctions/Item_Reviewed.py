from rdflib import URIRef, Namespace
import pandas as pd

amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
amazonont = Namespace("https://purl.archive.org/purl/amazon/ontology#")
schema = Namespace("https://schema.org/")

def itemReviewedTTL(df, graph):
    #Prepping the dataframe
    df = df[['index','asin']]
    df = df.rename(columns={'index' : 'source', 'asin' : 'target'})
    df['edge'] = len(df) * ['itemReviewed']

    df['source'] = df['source'].astype(str)
    df['target'] = df['target'].astype(str)

    #Conversion to TTL
    for index, row in df.iterrows():
        graph.add(triple = (URIRef(amazonent + row['source']),
                            URIRef(schema + row['edge']),
                            URIRef(amazonent + row['target'])))
    return graph
        
