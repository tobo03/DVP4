import rdflib

g = rdflib.Graph()

g.parse(r'Final_KG.ttl', format = "ttl")

query_name = "SELECT ?name WHERE {amazonent:B01HJGG2NQ schema:name ?name}"
for name in query_name:
    print("Name of product B01HJGG2NQ:", name)

query_cat = "SELECT ?product WHERE {?product schema:category amazoncat:Socks-Men}"
for cat in query_cat:
    print("Products with category Socks-Men:", cat)

query_brand = "SELECT ?product WHERE {?product schema:brand amazonent:bububibi}"
for brand in query_brand:
    print("Product with brand:", brand)

query_alsoview = "SELECT (COUNT(?product) as ?countofproduct) WHERE {amazonent:B000N8JX20 amazonont:also_view ?product}"
for alsoview in query_alsoview:
    print("Count of products with also_view of product B000N8JX20:", alsoview)

query_alsobuy = "SELECT (COUNT(?product) as ?countofproduct) WHERE {amazonent:B000MOKXT2 amazonont:also_buy ?product}"
for alsobuy in query_alsobuy:
    print("Count of products with also_buy of product B000MOKXT2:", alsobuy)

query_reviews = "SELECT (COUNT(?reviews) as ?countofreviews) WHERE {?reviews schema:itemReviewed amazonent:B00108PPCE}"
for reviews in query_reviews:
    print("Count of reviews of product B00108PPCE:", reviews)

query_author = "SELECT ?author WHERE {?author schema:author amazonent:677052}"
for author in query_author:
    print("Author of review 677052:", author)

query_score = "SELECT ?score WHERE {amazonent:895979 schema:reviewRating ?score}"
for score in query_score:
    print("Reviewrating of review 895979:", score)

query_date = "SELECT ?date WHERE {amazonent:895979 schema:DateTime ?date}"
for date in query_date:
    print("Date of review 895979:", date)

query_subcat = "SELECT COUNT(?subcats) as ?countofsubcats) WHERE {?subcats wds:instance_of amazoncat:Pants-Men}"
for subcat in query_subcat:
    print("All subcategories with instance of Pants-Men:", subcat)

query_body = "SELECT ?body WHERE {amazonent:896016 schema:reviewBody ?body}"
for body in query_body:
    print("ReviewBody of review 896016:", body)


