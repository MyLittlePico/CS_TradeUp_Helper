import pandas as pd


def list_inventory_comps():

    pd_categories = pd.CategoricalDtype(categories=['Normal', 'StatTrak™'], ordered=True)
    pd_exteriors = pd.CategoricalDtype(categories=['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred'], ordered=True)
    pd_qualities =  pd.CategoricalDtype(categories=['Covert', 'Classified', 'Restricted', 'Mil-Spec Grade', 'Industrial Grade', 'Consumer Grade'], ordered=True)

    
    try:
        df = pd.read_csv("./user/My_Inventory.csv", dtype={'Name':'category','Exterior':pd_exteriors,'Category':pd_categories,'Quality':pd_qualities,'Collection':'category'})

    except:
        print("!Local inventory data not found!\nUse --fetch to make local files")
        return

    collections = df['Collection'].unique()
    for collection in collections:
        print(f"\n{collection}")
        categories = df[df['Collection'] == collection]['Category'].unique() 
        for category in categories:
            print(f"   {category}")
            names = df[(df['Collection'] == collection) & (df['Category'] == category)]['Name'].unique()
            for name in names:
                print(f"      {name}")
                exteriors = df[(df['Collection'] == collection) & (df['Category'] == category) & (df['Name'] == name)]['Exterior'].unique()
                for exterior in exteriors:
                    count = len(df[(df['Collection'] == collection) & (df['Category'] == category) & (df['Name'] == name) & (df['Exterior'] == exterior)])
                    print(f"         {exterior} ({count})")
            