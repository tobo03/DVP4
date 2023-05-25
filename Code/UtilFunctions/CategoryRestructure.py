import pandas as pd

def dfCat_to_triplet(df):
    df_triplets = pd.DataFrame(columns=['source', 'target', 'edge'])
    temp_dict = {} # Make a Dict that is used to store the source_name to see if we've seen them before, note that source_name is used for the key of the the Dict, so we just check if the key has been registred

    for L  in df["category"]:
        for i in reversed(range(len(L))):
            try: # Sees if the source_name has been seen before, if it has it stops looking at the rest of the vals in the category-list
                temp_dict[f'{L[i]}-{L[i-1]}']
                break
            except: # If the source_name has not been seen before it Registres it
                if L[i] == "Sports & Outdoors":
                    break
                else:
                    source_name = f'{L[i]}-{L[i-1]}'

                    if L[i-1] == "Sports & Outdoors": # Determines source_name
                        target_name = "Sports & Outdoors"
                        OG_name = "Sports & Outdoors"
                    else:
                        target_name = f'{L[i-1]}-{L[i-2]}'
                        OG_name = L[i]
                    
                    df_triplets = pd.concat([df_triplets, pd.DataFrame([{'source' : source_name, 'target' : target_name, 'edge' : 'instance_of', 'OG_name':OG_name}])], ignore_index=True, axis=0, join='outer')

                    temp_dict[source_name] = ''
    return df_triplets