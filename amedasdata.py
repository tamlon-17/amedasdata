import getamedas
import streamlit as st
import openpyxl

st.set_page_config(page_title='いつものやつ', page_icon='icon.ico')
st.title('いつものやつ')
st.caption('作物普及員なら一度は作ったことのある、栽培期間の気象をグラフにするためのウェブアプリです。')
# if st.button('アプリの説明～必ず読んでね！'):
# st.switch_page('pages/page1.py')

amedas_l = ['気仙沼', '川渡', '築館', '志津川', '古川', '大衡', '鹿島台', '石巻',
            '新川', '仙台', '白石', '亘理', '米山', '塩釜', '駒ノ湯', '丸森',
            '名取', '蔵王', '女川']

# 必要事項の入力
with st.form(key='amd_form'):
    st.header('入力フォーム')
    a_area = st.selectbox('アメダス地点の選択', amedas_l)
    begin_date = st.date_input('データの取得開始日')
    end_date = st.date_input('データの取得最終日（開始日から1年未満）')
    years = int(st.text_input('何年分のデータの平均値とするか（上記の期間を含めた直近○○年）※当年のみの場合は１', 1))
    daily_harf = st.radio('日別データか半旬別データか', ['日別', '半旬別'])
    submit_button = st.form_submit_button('取得開始')

if submit_button:
    amd_df = getamedas.get_amedas_data(a_area, begin_date, end_date, years,
                                       daily_harf == '日別')
    st.write(amd_df)
    # エクセルデータを取得
    excel_data = getamedas.convert_to_excel(amd_df)
    # ダウンロードボタンを作成
    st.download_button(
        label="Download Excel file",
        data=excel_data,
        file_name='dataframe.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml'
             '.sheet')

else:
    st.text('必要事項を入力して「取得開始」ボタンを押してみてね')
