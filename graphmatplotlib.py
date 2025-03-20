import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

mpl.rcParams['font.family'] = 'MS Gothic'
mpl.rcParams['axes.xmargin'] = 0.01

# Excelファイルを読み込む
excel_file = 'weatherdata.xlsx'
# すべてのシートを読み込む
df1 = pd.read_excel(excel_file, sheet_name='指定期間')
df2 = pd.read_excel(excel_file, sheet_name='平年値')

# グラフ作成
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

x = df1.index.tolist()
y1 = df1['平均気温'].tolist()
y2 = df2['平均気温'].tolist()
y3 = df1['降水量'].tolist()
y4 = df2['降水量'].tolist()
y5 = df1['日照時間'].tolist()
y6 = df2['日照時間'].tolist()

# 気温のグラフ
ax1.plot(x, y1, color='red')
ax1.plot(x, y2, color='magenta', lw=1, linestyle='dashed')
ax1.grid(True, axis='y')
ax1.set(ylabel='平均気温(℃)', xlim=(-1, None), ylim=(0, None), axisbelow=True)


# 降水量のグラフ
ax2.bar(x, y3, color='blue')
ax2.plot(x, y4, color='black', lw=0.7)
ax2.grid(True, axis='y')
ax2.set(ylabel='降水量(mm)', axisbelow=True)


# 日照時間のグラフ
ax3.bar(x, y5, color='orange')
ax3.plot(x, y6, color='black', lw=0.7)
ax3.grid(True, axis='y')
ax3.set(xlabel='月日', ylabel='日照時間(h)', axisbelow=True)


plt.show()
