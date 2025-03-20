from datetime import date
import getamedas
import streamlit as st


st.set_page_config(page_title='いつものやつ', page_icon='icon.ico')
st.title('いつものやつ')
st.caption('作物普及員なら一度は作ったことのある、栽培期間の気象をグラフにするためのウェブアプリです。')
'''
if st.button('アプリの説明～必ず読んでね！'):
    st.switch_page('pages/page1.py')
'''
amedas_l = ['気仙沼', '川渡', '築館', '志津川', '古川', '大衡', '鹿島台', '石巻',
            '新川', '仙台', '白石', '亘理', '米山', '塩釜', '駒ノ湯', '丸森',
            '名取', '蔵王', '女川']


# 必要事項の入力
a_area = st.selectbox('アメダス地点の選択', amedas_l)
begin_date = st.date_input('データ取得開始日')
end_date = st.date_input('データ取得最終日')
years = int(st.text_input('平均する直近○○か年'))
daily_harf = st.radio('日別か半旬別か', ['日別', '半旬別'])

amd_df = getamedas.get_amedas_data(a_area, begin_date, end_date, years,
                                   daily_harf == '日別')
st.write(amd_df)
