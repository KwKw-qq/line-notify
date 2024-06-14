import bs4
import requests
import schedule
import time

# 儲存已推送過的新聞標題的集合
pushed_titles = set()

# 函式：從新聞網站爬取新聞標題和連結
def scrape_news():
    url = "https://star.setn.com/viewall/63"
    r = requests.get(url)
    root = bs4.BeautifulSoup(r.text, "html.parser")
    titles = root.find_all("h3", class_="newsTitle")
    return titles

# 函式：發送訊息到LINE Notify
def line_notify_message(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-type": "application/x-www-form-urlencoded"
    }
    payload = {"message": msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

# 主程式：設定定時器每小時執行一次
def main():
    token = "EQ2vFgUdwVwMP0fA74wBdB4nUmQElJUzJZEkBWQk96L"

    # 每小時執行一次的函式
    def job():
        global pushed_titles
        titles = scrape_news()
        for title in titles:
            title_text = title.a.string
            if title_text not in pushed_titles:
                pushed_titles.add(title_text)
                link = "https://star.setn.com" + title.a.get("href")
                message = title_text + "\n" + link
                line_notify_message(token, message)

    # 設定每小時執行的工作
    schedule.every().hours.do(job)

    # 無限循環，直到程式被中斷
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
