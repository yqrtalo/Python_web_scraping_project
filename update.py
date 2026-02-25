import time,random
import pandas as pd
from utils.utils import get_boxoffice_connection, money_to_int,get_imdb_data,get_tw_gross  # 導入函式

# 讀取現有的清單
df = pd.read_csv("movie_master_list.csv")

for index, row in df.iterrows():
    # 只處理還沒抓過詳細資料的電影
    if row['Is_Processed'] == True:
        continue
    
    try:
        print(f"補全資料中: {row['Title']}...")
        
        # 1. 前往 Mojo 詳情頁抓 IMDb_ID
        detail_soup = get_boxoffice_connection(row['Detail_URL'])
        imdb_id = detail_soup.select_one('div.a-box-inner a').get("href").split("/")[4]
        
        # 2. 前往 IMDb 抓 Genres 等資料
        imdb_data = get_imdb_data(imdb_id)
        
        # 3. 抓台灣票房
        gross_tables = detail_soup.find_all('table')
        tw_gross = money_to_int(get_tw_gross(gross_tables))
        
        # 4. 更新 DataFrame 內容
        df.at[index, 'imdbID'] = imdb_id
        df.at[index, 'ChineseTitle'] = imdb_data['titleText']
        df.at[index, 'Genres'] = ", ".join(imdb_data['genre'])
        df.at[index, 'Taiwangross'] = tw_gross
        df.at[index, 'Is_Processed'] = True # 標記為已完成
        
        print(f"imdbID={imdb_id} | "
              f"ChineseTitle={imdb_data.get('titleText')} | "
              f"Genres={imdb_data.get('genre')} | "
              f"Taiwangross={tw_gross}"
              )
        
        # 存檔確保安全
        df.to_csv("movie_master_list.csv", index=False, encoding="utf-8-sig")
        
        # 避免被擋，亂數休息時間
        # base_time = random.uniform(3,10)    #測試用
        base_time = random.uniform(5,15)
        if random.random() < 0.10:
            base_time += random.uniform(2, 120)
            
        time.sleep(base_time) # 補資料時的休息
        
        # if index ==2: break
        
    except Exception as e:
        print(f"失敗: {row['Title']}, 錯誤: {e}")
        continue