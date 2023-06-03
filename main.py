from bs4 import BeautifulSoup
import requests
from time import sleep
import openpyxl

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json;q=0.8,/;q=0.5'}

HOST = "https://www.imdb.com"
URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"


def get_html(url, params=''):
    sleep(1)
    r = requests.get(url, headers=headers, params=params).text
    return r


def get_content(html):
    soup = BeautifulSoup(html, "lxml")
    for i in soup.find("tbody", class_="lister-list").find_all("tr"):
        sleep(1)
        url_img = i.find("td", class_="posterColumn").find("img").get("src")
        name_film = i.find("td", class_="titleColumn").find("a").text
        creation_year = i.find("td", class_="titleColumn").find("span").text.replace("(", '').replace(")", '')
        rating = i.find("td", class_="ratingColumn imdbRating").text.replace("\n", '')
        page_url = i.find("td", class_="titleColumn").find("a").get("href")
        soup_page = BeautifulSoup(get_html(HOST + page_url), "lxml")
        description = soup_page.find("span", class_="sc-5f699a2-0 kcphyk").text
        yield name_film, creation_year, rating, description, url_img


wb = openpyxl.Workbook()
ws = wb.active
ws.column_dimensions['A'].width = 10
ws.column_dimensions['B'].width = 5
ws.column_dimensions['C'].width = 5
ws.column_dimensions['D'].width = 200
ws.column_dimensions['E'].width = 100
ws.append(("Название", "Год", "Рейтинг", "Описание", "Ссылка на постер"))
for l in get_content(get_html(URL)):
    ws.append(l)
wb.save("test.xlsx")
