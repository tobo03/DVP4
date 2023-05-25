from rdflib import URIRef, Namespace
import pandas as pd

from UtilFunctions.CategoryRestructure import dfCat_to_triplet


amazoncat = Namespace("https://purl.archive.org/purl/amazon/entities#")
wds = Namespace("http://www.wikidata.org/entity/statement/")




def subcatTTL(df, graph):
    #Prepping the dataframe
    df = df[['category']]
    df = dfCat_to_triplet(df)
    df = df.drop_duplicates(['source', 'target'])
    df['source'] = df['source'].astype(str)
    df['target'] = df['target'].astype(str)

    #Conversion to TTL
    for index, row in df.iterrows():
        graph.add(triple = (URIRef(amazoncat + row['source']),
                            URIRef(wds + row['edge']),
                            URIRef(amazoncat + row['target'])))
    return graph
        

