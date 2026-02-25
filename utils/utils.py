import requests 
from bs4 import BeautifulSoup as bs 
import json

def get_boxoffice_connection(path):
    """
    Parameters
    ----------
    path：str
        查詢頁面子網址
        
    Returns
    ----------
    soup : BeautifulSoup
       解析後的 HTML 文件物件
    """
    
    # 1. 定義連線url
    url = f"https://www.boxofficemojo.com{path}"
    
    # 2. 設定 Headers ，避免網站擋爬蟲，
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # print(f"嘗試連線至: {url}")

    try:
        # 3. 發送請求
        response = requests.get(url, headers=headers)
        
        # 4. 回報結果
        if response.status_code == 200:
            # print("成功！")
            soup = bs(response.text, "lxml")
            return soup
        else:
            print(f"失敗！狀態碼為 {response.status_code}。")
            return response.status_code

    except Exception as e:
        print(f"發生連線錯誤: {e}")
        return None

def money_to_int(s):
    """
    Parameters
    ----------
    s : str
        票房紀錄原始資料  如："$1,417,357,800"

    Returns
    -------
    int
        整理後的金額數值，方便後續統計
    """
    s = s.strip() # 洗格式 把空白和換行(\n)清除
    if s=='–':
        return 0
    else:
        return int(s.replace('$','').replace(',',''))
    


# 測試用 
# imdb_id='tt1757678'      # 阿凡達：火與燼
# dataName = (titleText,genre)  # 中文片名、類型  20250208 改回傳dict：避免同一頁面因資料名稱要解析多次
def get_imdb_data(imdb_id):
    """
    Parameters
    ----------
    imdb_id : str
        IMDb 影片識別碼，例如 "tt1757678"
    
    Returns
    -------
    dict : 
        電影資料字典，包含：
        -titleText: srt
            中文片名
        -genre:list[str]
            電影類型
    """
    # 1. 設定url
    url = f"https://www.imdb.com/title/{imdb_id}"
        
    # 2. 設定 Headers ，避免網站擋爬蟲，
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    # 
    
    response = requests.get(url, headers=headers)
    # 4. 回報結果
    if response.status_code == 200:
        # print("成功！")
    
        soup = bs(response.text, "lxml")
        # 1. 因imdb的網頁資料是javascript動態產生，無法直接從網頁擷取資料，改從載入的script，調整方向由chatgpt提供
        json_script = soup.find("script", id="__NEXT_DATA__")
        if json_script:
            # 2. 將字串轉為 dict
            data = json.loads(json_script.string)
            
            # print(data) # chk ：確認有沒有Genres
            
            try:
                # 3. 擷取資料回傳
                # !!：取得資料的路徑是根據目前(20260207) IMDb 結構，如果未來失效，需調整dict的路徑位置
                
                pageProps = data['props']['pageProps']      # 電影詳細資料
                # =============================================================
                # if dataName == 'titleText':
                #     titleText = pageProps['mainColumnData']['titleText']['text']
                #     return titleText
                #     print(titleText)
                # elif dataName = 'genre':
                #     genre_data = pageProps['aboveTheFoldData']['genres']['genres'] # 這是一個 list
                #     genre=[item["text"] for item in genre_data]
                #     print(genre)    # 確認擷取資料是否正確
                #     return genre
                # ==============================================================
                
                # 取中文片名
                titleText = pageProps['mainColumnData']['titleText']['text']
                
                # 取類型資料
                genre_data = pageProps['aboveTheFoldData']['genres']['genres'] # 這是一個 list
                genre=[item["text"] for item in genre_data]
                
                return {
                    "titleText":titleText,
                    "genre":genre
                    }
                
            except (KeyError, TypeError) as e:
                # print(f"JSON 結構可能改變，無法直接讀取: {e}")
                # 如果路徑變了，印出 data.keys() 來檢查新結構
                return None
            
        else:
            # print("網頁結構可能改變，找不到 __NEXT_DATA__ 標籤")
            return None

def get_tw_gross(gross):
    """
    Parameters
    ----------
    gross : bs4.element.ResultSet
            由 BeautifulSoup 取得的 table 標籤集合，
            通常來自 soup.find_all('table')

    Returns
    -------
    str
        台灣票房金額（字串格式，例如 "$12,345,678"），
        若找不到台灣資料則回傳 "0"

    """
    for table in gross:
        # print(table)
        th = table.find("th")
        if th and th.get_text(strip=True) == "Asia Pacific": 
            # Asia_table = th.find_parent("table")   #往回找定位 table
            Asia_rows = table.find_all('tr')[2:]
            
            for a_row in Asia_rows:
                # print(a_row)
                gross=0
                a_cols = a_row.find_all('td')
                
                if(a_cols[0].text =='Taiwan'):
                    gross = a_cols[3].text
                    # print(a_cols[0].text,gross)
                    return gross
    return "0"