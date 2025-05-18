import bs4
import requests
import re

from bs4 import BeautifulSoup

value1 = input("Enter ticker symbol: ")

url = f"https://finance.yahoo.com/quote/{value1}/"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

scrape_name = (soup.find("h1")).text.strip()
print(scrape_name)
abbrev_regex = "\s\(.*\)"
scrape_name = re.sub(abbrev_regex, "", scrape_name)
print(scrape_name)

scrape_cv = (soup.find(attrs={"data-testid": "qsp-price"})).text.strip()
print(scrape_cv)
scrape_cv = float(scrape_cv)
scrape_cv = int(scrape_cv * 100)
print(scrape_cv)