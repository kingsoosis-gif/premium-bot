import requests
from bs4 import BeautifulSoup
from config import PROFIT_PERCENT

def get_dollar_rate():
    try:
        url = "https://www.tgju.org/profile/price_dollar_rl"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        price = soup.find("span", {"data-market-row": "price_dollar_rl"})
        if price:
            return int(price.text.replace(",", ""))
    except:
        pass
    return 62000  # fallback

def usd_to_irr(price_usd):
    rate = get_dollar_rate()
    price_irr = int(price_usd * rate * (1 + PROFIT_PERCENT / 100))
    return f"{price_irr:,} تومان"
