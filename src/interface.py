import pandas as pd
import json
from src.item_pool import ItemPools
from src.find_combination import find_combination


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
                                                           'Normalized_Float':'float32'
                                                           })
    except:
        print("Local inventory data not found\nUse --fetch to make local files")
        return
    

    
    pools = ItemPools()

    for collection in config["composition"]:
        for exterior_num_pair in config["composition"][collection]:
            print(f"add {collection} {exterior_num_pair["exterior"]} {exterior_num_pair["quantity"]}")

            sorted_df = df[(df['Category'] == config["category"]) & (df['Quality'] == config["quality"]) & (df['Collection'] == collection) & (df['Exterior'] == exterior_num_pair['exterior'])].sort_values(by='Normalized_Float')
            print(sorted_df)
            pools.add_new_pool(
                sorted_df['Float'].tolist(),
                sorted_df["assetID"].tolist(),
                exterior_num_pair["quantity"]
            )

    find_combination(pools, config["target_value"])

def add_items_to_pool():
    pass
    
