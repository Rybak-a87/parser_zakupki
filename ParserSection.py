import requests
from bs4 import BeautifulSoup


class ParserSection:
    def __init__(self, start_url):
        self.__start_url = start_url
        self.__session = requests.Session()
        self.__session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"   # TODO разобраться с этим парраметром для себя
        self.__session.headers["Host"] = self.__start_url.replace("https://", "")

    def pagers(self, url):
        """requests запрос с проверкой на статус код 200"""
        while True:
            self.__page = self.__session.get(url)
            self.__page.encoding = "UTF-8"
            if self.__page.status_code == 200:
                break
            print("NO CONNECT...")
        return self.__page

    # обработка запроса в bs4
    def __b_soup(self):
        self.__soup = BeautifulSoup(self.__page.text, "html.parser")
        return self.__soup

    #поиск информации в html коде
    def selects(self, slct):
        self.__selects = self.__b_soup().select(slct)
        return self.__selects

    # вывод ссылок пейджера
    def get_pages(self):
        return self.__page_urls

    # добавление пейджер ссылок
    def set_list_pages(self, n, url_and_articl):
        self.__page_urls = []
        if "pageNumber=" not in url_and_articl:
            url_and_articl = url_and_articl + "?pageNumber=1"
        self.__url = url_and_articl
        for i in range(1, n+1):
            self.__page_urls.append(self.__url.replace("pageNumber=1", f"pageNumber={i}"))

    # добавление ссылок карт
    def set_list_cards(self, slct):
        self.__cards_urls = []
        for i in slct:
            temp = self.__start_url + i.get("href")
            self.__card_url = temp[:temp.index("&")]
            self.__cards_urls.append(self.__card_url)

    # вывод списка карт
    def get_cards(self):
        return self.__cards_urls

    # добавлени в словарь
    def set_dict(self, keys, values):
        self.__dict_information = dict()
        for i in range(len(keys)):
            self.__dict_information[keys[i].text.lower()] = values[i].text.strip().replace("\n", " ")

    # добавлени в словарь
    def add_to_dict(self, keys, values):
        art = "доверенного лица"
        while len(values) < len(keys):
            values.append("-")
        for i in range(len(keys)):
            k = f"{keys[i].text.lower()} {art}"
            try:
                v = values[i].text.strip().replace("\n", " ")
            except AttributeError:
                v = values[i]
            self.__dict_information[k] = v

    # вывод словарь
    def get_dict(self):
        return self.__dict_information
