import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mtick

# 視覺化：各年度全球總票房趨勢
def plot_yearly_trend(df):
    # 設定字體路徑 (Windows 標準路徑)
    font_path = "C:/Windows/Fonts/msjh.ttc"  # 微軟正黑體
    font_prop = fm.FontProperties(fname=font_path)
      
    # 定義分級邏輯
    def assign_tier(rank):
        if rank <= 10: return 'Top 1-10'
        elif rank <= 30: return 'Top 11-30'
        else: return 'Top 31-50'
    
    df['Tier'] = df['Rank'].apply(assign_tier)
    
    # 進行資料透視：年度為 X 軸，分級為欄位，票房為數值
    pivot_df = df.pivot_table(index='year', columns='Tier', 
                              values='Worldwidegross', aggfunc='sum')
    
    # 調整欄位順序，讓最厲害的在最下面或最上面
    pivot_df = pivot_df[['Top 31-50', 'Top 11-30', 'Top 1-10']]
    
    # 繪圖
    pivot_df.plot(
        kind='area', 
        stacked=True, 
        figsize=(12, 7), 
        alpha=0.7
        )
    
    plt.title('全球票房 Top 50 結構分析', fontproperties=font_prop, fontsize=18)
    plt.ylabel('年\n度\n票\n房\n︽\n百\n億\nUSD\n︾', 
               fontproperties=font_prop, 
               rotation=0, 
               labelpad=40, 
               fontsize=14
               )
    plt.xlabel('年份', fontproperties=font_prop, fontsize=14)
    
    plt.xticks(range(2006, 2026), rotation=45)
    plt.xlim(2006, 2025)
    
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# 視覺化：年度票房集中度趨勢圖
def plot_Top5(df):
    # 設定字體路徑 (Windows 標準路徑)
    font_path = "C:/Windows/Fonts/msjh.ttc"  # 微軟正黑體
    font_prop = fm.FontProperties(fname=font_path)
        
    # 計算每年的「前 50 名總票房」
    yearly_total_50 = df.groupby('year')['Worldwidegross'].sum()
    # 計算每年的「前 5 名總票房」
    top5_data = df[df['Rank'] <= 5]
    yearly_total_5 = top5_data.groupby('year')['Worldwidegross'].sum()    # 計算百分比    
    concentration_ratio = (yearly_total_5 / yearly_total_50) * 100
    result_df = concentration_ratio.reset_index()
    result_df.columns = ['Year', 'Top5_Concentration_Ratio']
    # 計算每年的「前 6 - 20 名總票房」
    Top6to20 = df[df['Rank'].between(6, 20)]
    yearly_total_6to20 = Top6to20.groupby('year')['Worldwidegross'].sum()    # 計算百分比    
    concentration_ratio_6to20 = (yearly_total_6to20 / yearly_total_50) * 100
    result_df1 = concentration_ratio_6to20.reset_index()
    result_df1.columns = ['Year', 'Top6_To_20_Concentration_Ratio']
      
    plt.plot(
        result_df['Year'], 
        result_df['Top5_Concentration_Ratio'], 
        marker='s', 
        color='darkorange', 
        linewidth=2, 
        label='Top 5'
        )
    plt.plot(   
        result_df1['Year'], 
        result_df1['Top6_To_20_Concentration_Ratio'], 
        marker='s', 
        color='navy', 
        linewidth=2, 
        label='Top 6-20'
        )
    
    # plt.title('年度票房集中度趨勢圖', fontproperties=font_prop, fontsize=14)
    # 20250212 報告後補充y軸標籤
    plt.ylabel('年\n度\n票\n房\n佔\n比\n︽\n%\n︾', 
               fontproperties=font_prop, 
               rotation=0, 
               labelpad=40, 
               fontsize=14,
               va='center',
               )
    plt.xlabel('年份', fontproperties=font_prop)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.ylim(15, 45) # 設定 Y 軸從 0 到 100
    plt.xticks(range(2005, 2026), rotation=45)
    plt.legend(prop=font_prop)
       
    plt.tight_layout()
    plt.show()
    
# 視覺化：漫威對全球票房的貢獻率
def plot_Marvel(df):
    # 設定字體路徑 (Windows 標準路徑)
    font_path = "C:/Windows/Fonts/msjh.ttc"  # 微軟正黑體
    font_prop = fm.FontProperties(fname=font_path)
    #分組統計，每年 MCU/非 MCU 的票房總和
    df['year'] = df['year'].astype(int)
    # 第一部mcu電影為2008 鋼鐵人
    mask = df['year']>=2008 
    df = df[mask]
    pivot_df = df.groupby(['year', 'is_Marvel'])['Worldwidegross'].sum().unstack(fill_value=0)
    pivot_df.columns = ['非 MCU', 'MCU']  # False → 非 MCU, True → MCU
    
    ax = pivot_df.plot(
        kind='bar',
        stacked=True,
        color=['gray', 'red']  # 非 MCU 灰色, MCU 紅色
    )
    
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: f'{x/1e8:.0f}'))
    
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height/1e8:.1f}',  # 轉成億
                        (p.get_x() + p.get_width()/2, p.get_y() + height/2),
                        ha='center', va='center', fontsize=8, color='black')
            
    # plt.title(' MCU /非 MCU 年度票房對比', fontproperties=font_prop, fontsize=14)
    # 20250212 報告後補充y軸標籤
    plt.ylabel('年\n度\n票\n房\n︽\n億\nUSD\n︾', 
               fontproperties=font_prop, 
               rotation=0, 
               labelpad=40, 
               fontsize=14,
               va='center'
               )
    plt.xlabel('年份', fontproperties=font_prop)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.legend(prop=font_prop)
    plt.tight_layout()
    plt.show()    

def plot_Marval_in_tw(df):
    # 設定字體路徑 (Windows 標準路徑)
    font_path = "C:/Windows/Fonts/msjh.ttc"  # 微軟正黑體
    font_prop = fm.FontProperties(fname=font_path)
    
    # 第一部mcu電影為2008 鋼鐵人
    mask = df['year']>=2008 
    df = df[mask]
    
    # 每年台灣總票房
    yearly_tw_total = df.groupby('year')['Taiwangross'].sum()
    
    # 每年 MCU 台灣票房
    yearly_mcu_tw = df[df['is_Marvel']].groupby('year')['Taiwangross'].sum()
    
    # MCU 佔比
    tw_mcu_ratio = (yearly_mcu_tw / yearly_tw_total) * 100
    tw_mcu_ratio = tw_mcu_ratio.reset_index()
    
    tw_mcu_ratio.columns = ['Year', 'TW_MCU_Ratio']
    #tw_mcu_ratio = tw_mcu_ratio.fillna(0)
    # 指定缺失年份 → 設為 NaN 無法確認資料，為確保資料正確處理
    missing_years = [2011, 2012, 2013, 2014, 2015]
    tw_mcu_ratio.loc[
        tw_mcu_ratio['Year'].isin(missing_years),
        'TW_MCU_Ratio'
    ] = None
    # 沒mcu電影上映的年份
    zero_years = [2009, 2020]
    tw_mcu_ratio.loc[
        tw_mcu_ratio['Year'].isin(zero_years),
        'TW_MCU_Ratio'
    ] = 0
    # 繪圖
    plt.plot(
        tw_mcu_ratio['Year'], 
        tw_mcu_ratio['TW_MCU_Ratio'], 
        marker='s', 
        color='darkorange', 
        linewidth=2, 
        label='MCU 台灣票房佔比'
    )
    
    # plt.title('MCU 電影於台灣市場的票房佔比趨勢（2006–2025）', fontproperties=font_prop, fontsize=18)
    plt.xlabel('年份', fontproperties=font_prop, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(tw_mcu_ratio['Year'], rotation=45)
    plt.ylim(0, 100)
    plt.legend(prop=font_prop)
    plt.axvspan(2011, 2016, color='gray', alpha=0.1, label='資料缺失期間')
    for i,j in zip(tw_mcu_ratio['Year'],tw_mcu_ratio['TW_MCU_Ratio']):
        if pd.notna(j):
            plt.text(
            i, j, f"{j:.1f}%",  # 顯示百分比
            ha='center', va='bottom', fontsize=9
            )
    plt.tight_layout()
    plt.show()


# 1. 讀取資料 
fn = 'movie_master_list.csv'
df = pd.read_csv(fn, names=[
    'year', 'Rank', 'Title', 'Detail_URL', 'Worldwidegross', 
    'Is_Processed', 'imdbID', 'ChineseTitle', 'Genres', 'Taiwangross'
])

# 資料篩選 原始資料為2005~2025 ，取2006~2025的20年份資料
df['year'] = pd.to_numeric(df['year'], errors='coerce')
mask = df['year']>=2006
data = df[mask]
data['Year_5'] = ((data['year']-1) // 5) * 5 + 1

# 整理格式轉數字
data['Rank'] = pd.to_numeric(data['Rank'], errors='coerce')
data['Worldwidegross'] = pd.to_numeric(data['Worldwidegross'], errors='coerce')
data['Taiwangross'] = (pd.to_numeric(data['Taiwangross'], errors='coerce').astype('Int64'))

# 整理Genres(csv轉進來的資料都是字串)
data['Genres'] = data['Genres'].str.replace("[", "").str.replace("]", "").str.replace("'", "")
data['Genres'] = data['Genres'].str.split(", ")


# 定義漫威 MCU 的關鍵字
marvel_keywords = [
    'Iron Man', 'Thor', 'Captain America', 'Avengers', 'Guardians of the Galaxy', 
    'Ant-Man', 'Doctor Strange', 'Black Panther', 'Captain Marvel', 
    'Black Widow', 'Shang-Chi', 'Eternals', 'Doctor Strange', 'Black Panther', 
    'The Marvels', 'Deadpool & Wolverine'
]

# 建立新欄位：如果標題包含關鍵字，就標記為 True
data['is_Marvel'] = data['Title'].apply(lambda x: any(k in x for k in marvel_keywords))

mask_spiderman_new = (
    (data['Title'].str.contains('Spider-Man:')) &  # 名稱包含 Spider-Man
    (data['year'].isin([2017, 2019, 2021]))        # mcu+sony版發行年份
)

data.loc[mask_spiderman_new, 'is_Marvel'] = True


plot_yearly_trend(data)

plot_Top5(data)

plot_Marvel(data)

'''
做資料檢核時，發現boxoffice台灣票房記錄不完整，所以棄用plot_Marval_in_tw
除2011~2015年度，台灣票房資料大規模缺失，2023~2025也有近半數電影沒有台灣票房
有找到其他的台灣票房資料，但資料一樣不完整，故不做台灣的mcu票房分析
plot_Marval_in_tw(data)
'''

# 擷取 22-23年的全球前5和台灣的前5做比對(因為台灣的前5片單可能無法上全球top50，來源另找)
mask = (data['year'].between(2022, 2023)) & (data['Rank'] <= 10)
data_Detail = data[mask]
data_Detail=data_Detail.loc[:,['year','Rank','ChineseTitle','Worldwidegross']]

subtotals = data_Detail.groupby('year')['Worldwidegross'].sum()
result = []
for year, group in data_Detail.groupby('year'):
    subtotal_row = pd.DataFrame({
        'year': [year],
        'Rank': ['Subtotal'],
        'ChineseTitle': ['小計'],
        'Worldwidegross': [group['Worldwidegross'].sum()]
    })
    result.append(pd.concat([group, subtotal_row], ignore_index=True))
final_df = pd.concat(result)
final_df.to_csv("22_23_TOP10.csv", index=False, encoding="utf-8-sig")
