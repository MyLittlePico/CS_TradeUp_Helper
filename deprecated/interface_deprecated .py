import pandas as pd
from src.item_pool import ItemPools
from src.find_combination import find_combination


def interface():
    pd_categories = pd.CategoricalDtype(categories=['Normal', 'StatTrak™'], ordered=True)
    pd_exteriors = pd.CategoricalDtype(categories=['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred'], ordered=True)
    pd_qualities =  pd.CategoricalDtype(categories=['Covert', 'Classified', 'Restricted', 'Mil-Spec Grade', 'Industrial Grade', 'Consumer Grade'], ordered=True)
    
    
    try:
        df = pd.read_csv("./user/My_Inventory.csv", dtype={'Name':'category','Exterior':pd_exteriors,'Category':pd_categories,'Quality':pd_qualities,'Collection':'category'})

    except:
        print("!Local inventory data not found!\nUse --fetch to make local files")
        return


    print("----------------------------")
    print("Categorise")
    print_pd_categorical(pd_categories.categories.array)
    print("\nSelect one Category")
    category = user_choose_one(pd_categories.categories.array)

    print("----------------------------")
    print("Qualities")
    print_pd_categorical(pd_qualities.categories.array)
    print("\nSelect one Qualitiy")
    quality = user_choose_one(pd_qualities.categories.array)
    

    collections = df[(df['Category'] == category) & (df['Quality'] == quality)]['Collection'].unique()

    print("----------------------------")
    print ("Collections")
    print_pd_categorical(collections)
    print("\nSelect Collections")
    collection_to_use = user_choose_multiple(collections)
    
    print("----------------------------")
    exterior_dict = get_exterior_to_use_dict(collection_to_use, pd_exteriors)

    print("----------------------------")
    nums_dict = get_num_to_use_dict(collection_to_use)

    item_pools = ItemPools()
    for collection in collection_to_use:
        if nums_dict[collection]:
            for exterior in exterior_dict[collection]:
                item_pools.add_new_pool( df[(df['Category'] == category) & (df['Quality'] == quality) & (df['Collection'] == collection) & (df['Exterior'] == exterior)]['Float'].tolist() ,collection )
            item_pools.add_tuples((collection, nums_dict[collection]))

    find_combination(item_pools)
    

        
    
 

def print_pd_categorical(categorical):
    for item in categorical:
        print(item)

def user_choose_one(options):
    choose = input(">>> ")
    while True :
        if choose in options:
            return choose
        else:
            choose = input("Please enter a valid option\n>>> ")

def user_choose_multiple(options):
    input_set = set()
    choose = input(">>> ")
    while True:
        if choose in options:
            input_set.add(choose)
            choose = input(">>> ")
        elif choose == "":
            if len(input_set) == 0:
                choose = input("Choose a least one option\n>>> ")
            else :
                return input_set 
        else:
            choose = input("Please enter a valid option\n>>> ")


def get_exterior_to_use_dict(collection_to_use, pd_exteriors):
    exterior_dict = dict()
    for collection in collection_to_use:
        print(f'Choose quility to use for {collection}')
        print_pd_categorical(pd_exteriors.categories.array)
        exterior_dict[collection] = user_choose_multiple(pd_exteriors.categories.array)

    return exterior_dict

def get_num_to_use_dict(collection_to_use):
    rest = 10
    num_dict = dict()

    print("Choose number for each collection to use in trade-up")
    
    for collection in collection_to_use:
        if rest != 0 :
            print(f"for {collection} 0 ~ {rest}")
            num = int ( user_choose_one( [str(i) for i in range(1, 11)] ) )
            num_dict[collection] = num
            rest -= num
            if rest == 0:
                print("10 items chosen")

        else:
            num_dict[collection] = 0
        
    return num_dict
