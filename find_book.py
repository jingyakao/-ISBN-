import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import re

def clean_isbn(isbn_input):
    """清理輸入的 ISBN 字串，只保留數字與末碼 X"""
    cleaned = re.sub(r'[^0-9X]', '', str(isbn_input).upper())
    return cleaned

def search_books_com(cleaned_isbn):
    """1. 博客來：嘗試精準抓取商品直達網址"""
    search_url = f"https://search.books.com.tw/search/query/key/{cleaned_isbn}/cat/all"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=8)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_result = soup.find("h3", class_="title") or soup.find("a", rel="mid_name")
            if search_result:
                a_tag = search_result.find("a") if search_result.name == "h3" else search_result
                if a_tag and a_tag.get("href"):
                    return urljoin("https://www.books.com.tw", a_tag["href"])
        return "ℹ️ 找不到具體商品頁（可能未上架），請手動至搜尋頁確認"
    except Exception:
        return f"💥 網路連線失敗，請改手動查看：{search_url}"

def search_sanmin(cleaned_isbn):
    """2. 三民書局：直接生成搜尋頁網址（因搜尋結構穩定，直接導入最省時）"""
    # 三民書局可以用 ISBN 直接接在 URL 後方進行檢索
    return f"https://www.sanmin.com.tw/search/index?v={cleaned_isbn}"

def search_eslite(cleaned_isbn):
    """3. 誠品線上：直接生成搜尋頁網址（因前端為動態載入，直接提供搜尋直達網址最實用）"""
    # 誠品搜尋網址格式
    return f"https://www.eslite.com/search?keyword={cleaned_isbn}"

# === 執行區塊 ===
if __name__ == "__main__":
    print("="*50)
    print("  三合一圖書平台 ISBN 網址檢索工具 (博客來/三民/誠品)  ")
    print("="*50)
    
    user_input = input("請輸入或貼上書籍的 ISBN：")
    isbn = clean_isbn(user_input)
    
    if len(isbn) not in [10, 13]:
        print("\n❌ 錯誤：ISBN 長度不對，請確認是否為 10 碼或 13 碼數字。")
    else:
        print("\n正在為您產生各平台商品連結...")
        print("-" * 50)
        
        # 執行博客來爬蟲
        books_url = search_books_com(isbn)
        # 產生三民網址
        sanmin_url = search_sanmin(isbn)
        # 產生誠品網址
        eslite_url = search_eslite(isbn)
        
        # 印出結果
        print(f"📚 【博客來直達網址】\n   {books_url}\n")
        print(f"📚 【三民書局搜尋頁】\n   {sanmin_url}\n")
        print(f"📚 【誠品線上搜尋頁】\n   {eslite_url}")
        print("-" * 50)