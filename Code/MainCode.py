import os
import pandas as pd

from UtilFunctions.ReplaceChar import replaceChar



os.chdir("C:/Users/test/Documents")
df = pd.read_json("meta_Sports_and_Outdoors.json", lines = True)
df = df.drop_duplicates(subset=['asin'])
substrings = [".", "%", "(", ":" ,"<" ,'"', '!', ';']


df['category'] = df.apply(lambda x: [string for string in x['category'] if not any(substring in string for substring in substrings)], axis = 1)

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