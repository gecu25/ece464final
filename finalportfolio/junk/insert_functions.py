import selenium
import re
import yfinance as yfi

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


from bs4 import BeautifulSoup

from models import Stock, HistoryMixin, Base
import queries

'''
def scraper(tickercheck):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920x1080')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=9222")
    # Selenium cannot find the price if it's run headless
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--headless')

    fullname = None
    currentval = None

    service = Service()
    driver = webdriver.Chrome(options=options, service=service)

    url = f"https://finance.yahoo.com/quote/{tickercheck}/"
    driver.get(url)

    fullname = driver.find_element(By.CSS_SELECTOR, "h1.yf-xxbei9").text
    abbrev_regex = "\s\(.*\)"
    fullname = re.sub(abbrev_regex, "", fullname)

    currentval = driver.find_element(By.XPATH, "//span[@data-testid='qsp-price']").text
    currentval = float(currentval)
    currentval = int(currentval * 100)

    driver.quit()

    return [fullname, currentval]

x = input("greetign")
y = scraper(x)
print(y)
'''

def get_history(tickercheck):
    class NewHistory(HistoryMixin, Base):
        __tablename__ = tickercheck

    temp_tick = yfi.Ticker(tickercheck)
    temp_historical = temp_tick.history(period="max", interval="1d")

'''
def insert_holder():

def insert_purchase():

def insert_stock():
'''