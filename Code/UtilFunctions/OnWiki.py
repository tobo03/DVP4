import requests
import pandas as pd
from UtilFunctions.Stemming import stem
from UtilFunctions.CategoryRestructure import dfCat_to_triplet

def onWiki(df):
    df = dfCat_to_triplet(df)
    df['OG_name_stem'] = df.apply(lambda row: stem(str(row['OG_name'])) ,axis=1)
    main_df['len'] = main_df.apply(lambda row: len(row['OG_name_stem']) ,axis=1)
    main_df = main_df.explode('OG_name_stem')
    temp_dict = {}
    for a in main_df['OG_name_stem'].unique():
        temp_dict[a] = fetch_wikidata(a)
    main_df['temp'] = main_df.apply(lambda row: temp_dict[row['OG_name_stem']], axis=1)
    main_df[['Q', 'dscp', 'bool']] = pd.DataFrame(main_df.test.tolist(), index = main_df.index)
    del main_df['temp']
    return df

def fetch_wikidata(query):
    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'search': query,
        'language': 'en'
    }
    
    url = 'https://www.wikidata.org/w/api.php'
    try:
        result = requests.get(url, params=params).json()

        for a in result['search']:
            if (a['id'][0] == "Q") and (a['label'].lower() == query.lower()):
                return [a['id'], a['description'], True]
        return['', '', False]
        
    except:
        return ['', '', False]
        
