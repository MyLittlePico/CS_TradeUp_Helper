import json
import pandas as pd

# 1. 載入檔案
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. 定義提取邏輯 (根據你看到的 JSON 結構調整)
# 假設數據是一個清單，或者在某個 key 下面
items_list = []

# 範例：遍歷 JSON 提取特定欄位
# 這裡需要根據你實際看到的 key 名稱修改，例如 'floatvalue', 'paintseed'
for entry in data.get('results', data): 
    info = {
        '名稱': entry.get('market_hash_name') or entry.get('full_item_name'),
        '精確磨損度': entry.get('floatvalue'), 
        '編號 (AssetID)': entry.get('assetid'),
        '模板 (PaintSeed)': entry.get('paintseed')
    }
    items_list.append(info)

# 3. 轉換為 Pandas 表格並匯出
df = pd.DataFrame(items_list)
df.to_excel('steam_analysis.xlsx', index=False)
print("成功分離數據並存入 Excel！")