# Windows10 Python3.9

# インポート
import requests
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

print('実行開始')

# サイトにアクセス
url = 'https://scraping-for-beginner.herokuapp.com/ranking/'
res = requests.get(url)

# 1秒待機
sleep(1)

# HTMLの構文解析
soup = BeautifulSoup(res.text, 'html.parser')

data = []

# 観光地情報を取得
spots = soup.find_all('div', attrs={'class': 'u_areaListRankingBox'})

for spot in spots:
    # 観光地名
    spot_name = spot.find('div', attrs={'class': 'u_title'})
    # 不要なバッチ部分を削除
    spot_name.find('span', attrs={'class': 'badge'}).extract()
    # 改行コードを削除
    spot_name = spot_name.text.replace('\n', '')

    # 評点
    eval_num = spot.find('div', attrs={'class', 'u_rankBox'}).text
    # 改行コードを削除して数値化
    eval_num = float(eval_num.replace('\n', ''))

    # カテゴリーアイテム
    categoryItems = spot.find('div', attrs={'class', 'u_categoryTipsItem'})
    categoryItems = categoryItems.find_all('dl')

    # 詳細データを辞書型で保存
    details = {}
    for categoryItem in categoryItems:
        category = categoryItem.dt.text
        rank = float(categoryItem.span.text)
        details[category] = rank

    datum = details
    datum['観光地名'] = spot_name
    datum['評点'] = eval_num
    data.append(datum)

# データフレーム化
df = pd.DataFrame(data)

# 項目の並び替え
df = df[['観光地名', '評点', '楽しさ', '人混みの多さ', '景色', 'アクセス']]

# CSVで保存
df.to_csv('観光地情報.csv', index=False)

print('実行終了')