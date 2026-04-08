import pandas as pd
import json
from src.item_pool import ItemPools
from src.find_combination_ga import find_combination_ga


def interface():
    try:
        with open("./user/config.json",'r') as f:
            config = json.loads(f.read())
    except:
        print("User config file not fount.")
        return
    
    
    try:
        df = df = pd.read_csv("./user/My_Inventory.csv", dtype={'Name':'category',
                                                           'Exterior':'category',
                                                           'Category':'category',
                                                           'Quality':'category',
                                                           'Collection':'category',
                                                           'Float':'float32',
                                                           'Normalized_Float':'float32',
                                                           })
    except:
        print("Local inventory data not found\nUse --fetch to make local files")
        return

    
    pools = ItemPools()

    for collection in config["composition"]:
        for exterior_num_pair in config["composition"][collection]:
            print(f"add {collection} {exterior_num_pair["exterior"]} {exterior_num_pair["quantity"]}")

            sorted_df = df[(df['Category'] == config["category"]) & (df['Quality'] == config["quality"]) & (df['Collection'] == collection) & (df['Exterior'] == exterior_num_pair['exterior'])].sort_values(by='Normalized_Float')
            pools.add_new_pool(
                sorted_df['Normalized_Float'].tolist(),
                sorted_df["assetID"].tolist(),
                exterior_num_pair["quantity"]
            )


    id_index = find_combination_ga(pools, config["target_value"])

    print("Suggested Combination:")
    pd.set_option("display.precision", 9)
    for asset_id in id_index:
        p_name = df[df['assetID']==asset_id]["Name"].astype('string').to_string(index=False) 
        p_exterior = df[df['assetID']==asset_id]["Exterior"].astype('string').to_string(index=False)
        p_float_value = df[df['assetID']==asset_id]["Float"].astype('float32').to_string(index=False)
        
        print(f"{p_name}\n\t{p_exterior}\n\t\tFloat: {p_float_value}")

def add_items_to_pool():
    pass
    
