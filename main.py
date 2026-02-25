import time,random
import pandas as pd
from utils.utils import get_boxoffice_connection, money_to_int  # 導入函式

# 準備存所有年份的清單
master_list = []

# for year in range(2020, 2026):   # 測試用
for year in range(2005, 2026):
    time.sleep(random.uniform(5,15))
    status = get_boxoffice_connection(f'/year/world/{year}/')
    data = status.find("table", class_="mojo-body-table")
    rows = data.find_all("tr")[1:]
    
    for row in rows[:5]:    #測試用
    # for row in rows[:200]:    #原本預計
    # for row in rows[:50]:
        cols = row.find_all("td")
        movie_info = {
            'year': year,
            'Rank': cols[0].text,
            'Title': cols[1].text,
            'Detail_URL': cols[1].find('a').get("href"), # 先存下詳情頁網址
            'Worldwidegross': money_to_int(cols[2].text),
            'Is_Processed': False 
        }
        master_list.append(movie_info)

# 存成 Master CSV
df_master = pd.DataFrame(master_list)
df_master.to_csv("movie_master_list.csv", index=False, encoding="utf-8-sig")