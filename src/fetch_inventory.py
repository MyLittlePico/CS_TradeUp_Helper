import urllib.request
import json
import pandas as pd


GAME_ID = 730 # count strike 2


def get_inventory_csv():

    steam_id =  input("Enter your Steam ID: ")

    item_list = get_item_list( steam_id, inventory_url(steam_id)) 

    df = pd.DataFrame(item_list)
    
    df.to_csv("./user/My_Inventory.csv", index = False)

def inventory_url(steam_id, start_id = 0):
    if start_id:
        return f"https://steamcommunity.com/inventory/{steam_id}/{GAME_ID}/2?count=1000&preserve_bbcode=1&raw_asset_properties=1&start_assetid={start_id}"
    return f"https://steamcommunity.com/inventory/{steam_id}/{GAME_ID}/2?count=1000&preserve_bbcode=1&raw_asset_properties=1"


def get_item_list(steam_id, url):
    try:
        with urllib.request.urlopen(url) as raw_response:
            response = raw_response.read().decode('utf-8')
            raw_data = json.loads(response)
    except:
        print("Check your steam_id")
        return
    
    print("creating csv file for your inventory")

    desc_map = {f"{d['classid']}_{d['instanceid']}": d for d in raw_data['descriptions']}
    prop_map = {f"{d['assetid']}": d for d in raw_data['asset_properties']}
    
    print(f"get {len(raw_data['assets'])} assets in your inventory")
    item_list = []

    if raw_data.get("last_assetid", 0):
        url = inventory_url(steam_id, start_id=raw_data.get( "last_assetid",0))
        item_list.extend(get_item_list(steam_id, url)) 

    for asset in raw_data['assets']:
        assetid = asset["assetid"]
        desc_id = f"{asset["classid"]}_{asset["instanceid"]}"
        
        tags = desc_map[desc_id].get("tags", [])
        tags_dict = { t['category']: t for t in tags}

        if tags_dict.get("Weapon"):
            properties = prop_map[assetid].get("asset_properties",[])
            float_value = next( (p["float_value"] for p in properties if p.get('propertyid') == 2) ,None)

            item_list.append({
                "assetID": assetid,
                "Name": desc_map[desc_id]["name"],
                "Exterior": tags_dict["Exterior"].get('localized_tag_name',"N/A"),
                "Category": tags_dict["Quality"].get('localized_tag_name',"N/A"),
                "Quality": tags_dict["Rarity"].get('localized_tag_name',"N/A"),
                "Collection": tags_dict["ItemSet"].get('localized_tag_name',"N/A"),
                "Float": float_value,
                "Normalized_Float": float_value
            })
    print("local csv file created")
    return item_list

        