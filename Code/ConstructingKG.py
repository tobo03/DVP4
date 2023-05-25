import os
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD, RDFS, SKOS

from UtilFunctions.ReplaceChar import replaceChar
import UtilFunctions.Classifying as classifying
from UtilFunctions.OnWiki import onWiki
from ConversionFunctions.Also_buy import alsoBuyTTL
from ConversionFunctions.Also_view import alsoViewTTL
from ConversionFunctions.Name import nameTTL
from ConversionFunctions.Price import priceTTL
from ConversionFunctions.Brand import brandTTL
from ConversionFunctions.Category import categoryTTL
from ConversionFunctions.Subcategory import subcatTTL
from ConversionFunctions.Item_Reviewed import itemReviewedTTL
from ConversionFunctions.Date_Published import datePublishedTTL
from ConversionFunctions.Author import authorTTL
from ConversionFunctions.reviewRating import reviewRatingTTL
from ConversionFunctions.reviewBody import reviewBodyTTL

##############Preprocessing###################

df = pd.read_json("meta_Sports_and_Outdoors.json", lines = True)
df = df[['asin', 'category', 'title', 'also_buy', 'also_view', 'brand', 'price']]

#drop duplicates
df = df.drop_duplicates(subset=['asin'])

#Fix category
substrings = [".", "%", "(", ":" ,"<" ,'"', '!', ';']
#Goes through each category within the category list, as long as the category does not include characters from the substrings list, it is included
df['category'] = df.apply(lambda x: [string for string in x['category'] if not any(substring in string for substring in substrings)], axis = 1) 
#
cats = df.explode(['category'])[['asin','category']]
cats_val = cats['category'].value_counts().reset_index()

A = list(cats_val['index'])
B = list(cats_val['category'])
dict_ = {}

for i in range(len(cats_val)):
    dict_[A[i]] = B[i] > 5

df['category'] = df.apply(lambda row: [x for x in row['category'] if dict_[x]], axis=1)

for col in list(df):
    df[col] = df.apply(lambda x: replaceChar(x[col]), axis = 1)

##################Review Dataset##################
df_review = pd.read_json("Sports_and_Outdoors_5.json", lines = True)
df_review = df_review[['overall','reviewerID', 'asin','unixReviewTime','reviewText']]
df_review = df_review.drop_duplicates()
df_review = df_review.reset_index()

################Creation of rdflib Graph#################
g = Graph()
amazonent = Namespace("https://purl.archive.org/purl/amazon/entities#")
amazonont = Namespace("https://purl.archive.org/purl/amazon/ontology#")
amazoncat = Namespace("https://purl.archive.org/purl/amazon/categories#")
schema = Namespace("https://schema.org/")
wds = Namespace("https://www.wikidata.org/wiki/")
g.bind("amazonent", amazonent)
g.bind("amazonont", amazonont)
g.bind("amazoncat", amazoncat)
g.bind("schema", schema)
g.bind("wds", wds)


################Conversion of Files######################
alsoBuyTTL(df, graph = g)
alsoViewTTL(df, graph = g)
nameTTL(df, graph = g)
priceTTL(df, graph = g)
brandTTL(df, graph = g)
categoryTTL(df, graph = g)
subcatTTL(df, graph = g)
itemReviewedTTL(df_review, graph = g)
datePublishedTTL(df_review, graph = g)
authorTTL(df_review, graph = g)
reviewRatingTTL(df_review, graph = g)
reviewBodyTTL(df_review, graph = g)

###############Classifying#####################
classifying.brandClass(df, graph = g)
classifying.productClass(df, graph = g)
classifying.reviewClass(df, graph = g)
classifying.personClass(df, graph = g)

###############Enriching category#################
df_enrich = onWiki(df)
df_amazon = df_enrich[df_enrich['bool'] == False].drop_duplicates(subset = ['source', 'OG_name_stem'])
df_wikidata = df_enrich[df_enrich['bool'] == True].drop_duplicates(subset = ['source', 'OG_name_stem'])
for index, row in df_amazon.iterrows():
    subject = amazoncat['%s'] %str(row['source'])
    g.add(triple = (URIRef(subject), RDFS.Class, URIRef(amazonont + "AmazonCategory")))

for index, row in df_wikidata.iterrows():
    subject = amazoncat['%s'] %str(row['source'])
    g.add(triple = (URIRef(subject), SKOS.narrowMatch if "&" in str(row['OG_name'])
                                                    else SKOS.closeMatch, 
                    URIRef(wds + row['Q'])))
    g.add(triple = (URIRef(subject), RDFS.Class, URIRef(amazonont + "WikidataCategory")))

##############Serializing KG#####################
g.serialize(destination="Final_KG.ttl")