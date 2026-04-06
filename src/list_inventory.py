import pandas as pd


def list_inventory_comps():
    
    try:
        df = pd.read_csv("./user/My_Inventory.csv", dtype={'Name':'category','Exterior':'category','Category':'category','Quality':'category','Collection':'category'})

    except:
        print("!Local inventory data not found!\nUse --fetch to make local files")
        return

    print(df.memory_usage(deep=True))
    print("showing inventory components")
    print (df)
    

    


    qualitys = df['Quality'].unique()
    for quality in qualitys:
        print('------------------------------------------')
        print(quality)
        collections = df['Collection'].unique()
        for collection in collections:
            exteriors = df[(df['Collection'] == collection) & (df['Quality'] == quality)]['Exterior'].unique()
            for exterior in exteriors:
                target_count = len(df[(df['Collection'] == collection) & (df['Quality'] == quality) & (df['Exterior'] == exterior)])
                
                if target_count:
                    print (f"{collection} {exterior} {target_count} items")

