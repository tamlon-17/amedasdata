from datetime import date, timedelta
import numpy as np
import pandas as pd
import lxml

# inputする項目、アメダス地点、気象データの種類、取得する月の範囲、取得する年の範囲
ame_dic = dict(気仙沼='0242', 川渡='0243', 築館='0244', 志津川='0246',
               古川='0247', 大衡='0248', 鹿島台='0249', 石巻='47592',
               新川='0251', 仙台='47590', 白石='0256', 亘理='0257', 米山='1029',
               塩釜='1030', 駒ノ湯='1126', 丸森='1220', 名取='1464',
               蔵王='1564', 女川='1626')
ame_area = '石巻'  # 入力
ame_index = ame_dic[ame_area]
ame_key = 's' if ame_area in ['仙台', '石巻'] else 'a'

get_list = ['日別', '半旬別']
get_data = '日別'  # 選択

weath_list = ['平均気温', '最高気温', '最低気温', '降水量', '日照時間']
weath_list = weath_list if ame_area != '名取' else weath_list[0:4]
weath_item = ['平均気温', '最高気温', '最低気温', '降水量', '日照時間']  # 複選

start_y = 2025  # 入力
start_m = 1  # 入力
start_h = 1
end_y = 2025  # 入力
end_m = 2
end_h = 20  # 入力

# 入力年月の整合性確認（1年以内じゃないとだめ
if (timedelta(days=1) < (date(end_y, end_m, 1) - date(start_y, start_m, 1)) <
        timedelta(days=367)):
    pass
else:
    print('終了年月が開始年月以前か、1年以上の期間が入力されています。')

std_y = 10  # 平年値の年数入力


# 気象庁HPから日別の気象データをスクレイピング
def scrape_daily(area, year, month):
    url = (f'https://www.data.jma.go.jp/stats/etrn/view/daily_{ame_key}1.php'
           f'?prec_no=34&block_no={area}&year={year}&month={month}&day=&'
           f'view=p1')
    df_l = pd.read_html(url)
    return df_l[0]


# 気象庁のHPから半旬別の気象データをスクレイピング
def scrape_half(area, year):
    url = (f'https://www.data.jma.go.jp/stats/etrn/view/mb5daily_{ame_key}1.'
           f'php?prec_no=34&block_no={area}&year={year}&month=1&day=&view=p1')
    df_l = pd.read_html(url)
    return df_l[0]


# スクレイピングしたDFから不要なカラムを削除
def extract_col(df):
    dic1 = dict(平均気温=6, 最高気温=7, 最低気温=8, 降水量=3, 日照時間=16)  # 日仙
    dic2 = dict(平均気温=4, 最高気温=5, 最低気温=6, 降水量=1, 日照時間=15)  # 日外
    dic3 = dict(平均気温=9, 最高気温=10, 最低気温=11, 降水量=5,
                日照時間=21)  # 半仙
    dic4 = dict(平均気温=7, 最高気温=8, 最低気温=9, 降水量=3, 日照時間=19)  # 半外
    if get_data == '日別':
        dic = dic1 if ame_area in ['仙台', '石巻'] else dic2
    else:
        dic = dic3 if ame_area in ['仙台', '石巻'] else dic4
    col = [dic[k] for k in weath_item]
    return df.iloc[:, col]


# クリーンアップの関数
def clean_df(df):
    df = df.replace(['//', '#'], np.nan)
    df = df.replace('--', 0.0)
    df = df.replace([r'\)', r' \]'], '', regex=True)
    try:
        df = df.apply(pd.to_numeric, errors='coerce')  # 非数値は自動的にNaNに変換
    except Exception as e:
        print(f"Error during conversion: {e}")
    return df


# 日別の1か月分のDFを提供する関数
def get_1month_df(year, month):
    df = scrape_daily(ame_index, year, month)
    df = extract_col(df)
    df = clean_df(df)
    if month == 2:
        df = df.drop(index=[28], errors='ignore')
    return df


# 半旬別の1or2年のDFを連結して取得して指定半旬で切り取って整形
def get_harf_df(year):
    df = scrape_half(ame_index, year)
    if start_y != end_y:
        df1 = scrape_half(ame_index, year + 1)
        df = pd.concat([df, df1], ignore_index=True)
    df = extract_col(df)
    df = clean_df(df)
    df = df.iloc[
         (start_m - 1) * 6 + start_h - 1:len(df) - (13 - end_m) * 6 + end_h, :]
    return df.reset_index(drop=True).set_axis(weath_item, axis=1)


# 開始月から終了月までのデータを取得して、1つのdfにまとめる
def get_total_df(s_y, e_y):
    if s_y == e_y:
        df_l = [get_1month_df(s_y, m) for m in range(start_m, end_m + 1)]
    else:
        df_l1 = [get_1month_df(s_y, m) for m in range(start_m, 13)]
        df_l2 = [get_1month_df(e_y, m) for m in range(1, end_m + 1)]
        df_l = df_l1 + df_l2
    return pd.concat(df_l, ignore_index=True).set_axis(weath_item, axis=1)


# DFのリストからnp.array経由で平均値のDFを取得
def mean_df(dfl):
    arrays = [df.to_numpy() for df in dfl]
    array_3d = np.stack(arrays)
    mean_np = np.nanmean(array_3d, axis=0)
    return pd.DataFrame(mean_np, columns=weath_item)


# 日別の平年値取得
if get_data == '日別':
    df_std_l = [get_total_df(sy, sy + end_y - start_y) for sy in
                range(start_y - std_y, start_y)]
    now_df = get_total_df(start_y, end_y)
else:
    df_std_l = [get_harf_df(y) for y in range(start_y - std_y, start_y)]
    now_df = get_harf_df(start_y)
std_df = mean_df(df_std_l)

with pd.ExcelWriter('weatherdata.xlsx') as writer:
    now_df.to_excel(writer, sheet_name='指定期間')
    std_df.to_excel(writer, sheet_name='平年値')

with pd.ExcelWriter('stddata.xlsx') as writer:
    for i, df_s in enumerate(df_std_l):
        df_s.to_excel(writer, sheet_name=str(i))


print(now_df)
print(std_df)
