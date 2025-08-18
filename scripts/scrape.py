"""
次のElementを取得する
<tbody>
    <tr>
      <td class="line01 right">3        年</td>
      <td class="line02">脳神経・感覚器学Ⅲ（耳鼻）      <!--フィールド(contents)の内容を改行ありで表示--></td>
      <td class="auto">下記のとおり，講義日程を変更します（冬学期から秋学期に１コマ移動）。<br><br>冬学期の講義　→　12/10（水）1限　副鼻腔／上野貴雄　第4講義室      <!--フィールド(rec_edit)の内容をM/dd形式に変換して表示--><p class="date">（07/29        掲載）</p></td>
    </tr>
</tbody>
"""
import requests
from bs4 import BeautifulSoup
import re # 正規表現を扱うためにインポート
import os

url = os.getenv('TARGET_URL', 'http://dbweb.m.kanazawa-u.ac.jp/stu/lect/listrec.php')
NOTIFY_API_URL = os.getenv('NOTIFY_API_URL', 'http://localhost:8000/api/v1/lectures/notify/')
SCRAPE_API_KEY = os.getenv('SCRAPE_API_KEY')

headers = {
    'X-API-KEY': SCRAPE_API_KEY # 独自ヘッダーにキーを設定
}

def scrape_and_post():
    try:
        # ネットワークエラーを考慮し、タイムアウトも設定
        response = requests.get(url, timeout=10)
        response.raise_for_status() # 4xx, 5xx系のエラーステータスの場合、例外を発生させる
        
        # 文字化け対策
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup.prettify())

        # 講義情報が含まれるtableタグをすべて取得する
        tables = soup.find_all('table')
        if not tables:
            print("講義情報のテーブルが見つかりませんでした。")
            raise Exception("No tables found")

        lectures = []
        for table in tables:
            tds = table.find_all("td")
            if len(tds) != 3:
                print('Warning: 構造が異なるテーブルが見つかりました。この行をスキップします。')
                continue # この行の処理をスキップして次に進む

            try:
                # 学年
                #  正規表現を使って、文字列から最初の数字を安全に抜き出す
                grade_text = tds[0].get_text()
                match = re.search(r'\d+', grade_text)
                if not match:
                    print(f"Warning: 学年が見つかりませんでした: {grade_text}")
                    continue
                grade = int(match.group(0))
                # 科目
                subject = tds[1].get_text().strip()
                # 内容
                content_cell = tds[2]
                date_tag = content_cell.find("p", class_="date")
                date = date_tag.get_text()
                
                content = content_cell.get_text(strip=True, separator=' ')
                content += date

                lectures.append({
                    "grade": grade,
                    "subject": subject,
                    "content": content
                })

            except (ValueError, IndexError) as e:
                print(f"データの処理中にエラーが発生しました: {e}")

        
        # POST
        if lectures:
            print(f"Sending {len(lectures)} lectures to the API...")
            try:
                # 1. タイムアウトを設定し、エラーハンドリングを行う
                response = requests.post(NOTIFY_API_URL, json=lectures, headers=headers, timeout=10)
                
                # 4xx, 5xx系のエラーステータスコードの場合、例外を発生させる
                response.raise_for_status() 

                print("Successfully sent data to the API.")
                # print("Response:", response.json()) # APIからのレスポンス内容を確認する場合

            except requests.exceptions.HTTPError as http_err:
                # HTTPエラー（例: 400, 404, 500）
                print(f"HTTP error occurred: {http_err}")
                print(f"Response body: {response.text}")
            except requests.exceptions.RequestException as req_err:
                # ネットワーク関連のエラー（例: 接続失敗、タイムアウト）
                print(f"An error occurred during the request: {req_err}")
            except Exception as e:
                # その他の予期せぬエラー
                print(f"An unexpected error occurred: {e}")
        else:
            print("No lectures to send.")
    except requests.exceptions.RequestException as e:
        print(f"URLへのアクセスに失敗しました: {e}")

if __name__ == "__main__":
    scrape_and_post()