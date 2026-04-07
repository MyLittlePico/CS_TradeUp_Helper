import json
import pandas as pd
import numpy as np


def apply_float_cap():
    try:
        with open("./user/config.json",'r') as f:
            config = json.loads(f.read())
    except:
        print("User config file not fount.")
        return
    
    try:
        df = pd.read_csv("./user/My_Inventory.csv", dtype={'Name':'category',
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
    

    print("Apply float cap to your inventory...\n")
    for weapon in config["float_caps"].keys():
        mask = (df['Name'] == weapon)
        lower_cap = config["float_caps"][weapon][0]
        upper_cap = config["float_caps"][weapon][1]
        print(f"{weapon}: {lower_cap} ~ {upper_cap}")
        df.loc[mask, 'Normalized_Float'] = normalize_float(df.loc[mask, 'Float'], np.float32(lower_cap), np.float32(upper_cap))

    
    df.to_csv("./user/My_Inventory.csv", index = False)
    print("\nComplete applying float cap to your inventory")


def normalize_float(float, lower_cap, upper_cap):
    return (float - lower_cap) / ( upper_cap - lower_cap)

    