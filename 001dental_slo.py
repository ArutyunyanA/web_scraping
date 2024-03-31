from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import csv

def dental_data_parsing(url):

    try:
        while url:
            check = urlopen(url)
            if check:
                status_code = check.getcode()
                print(f"Соединение с выбранным ресурсом успешно установлено код: {status_code}")
                bs = BeautifulSoup(check.read(), 'html.parser')
                pagination_wrapper = bs.find("div", {"class":"w2dc-pagination-wrapper"})
                if pagination_wrapper:
                    pagination_links = pagination_wrapper.find_all("a", href=True)
                    for link in pagination_links:
                        link_url = link.get("href")
                        print(f"Обработка ссылки: {link_url}")
                        process_page(link_url)
                    
                    next_line_link = bs.find("a", {"title":"Next Line"})
                    if next_line_link:
                        url = next_line_link.get("href")
                    else:
                        url = None
                    
    except URLError as urler:
        print(f"Попытка соединения с ресурсом не успешна: {urler}")

def process_page(url, process_links=set(), output_file='output001.csv'):

    try:
        with open(output_file, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            check = urlopen(url)
            if check:
                status_code = check.getcode()
                print(f"Обработка страницы: {url}")
                bs = BeautifulSoup(check.read(), 'html.parser')
                links = bs.find("div", {"class":"w2dc-listings-block-content"}).find_all("a", href=re.compile("https?://(?:www\.)?\w+\.\w+"))
                for link in links:
                    link_url = link.attrs["href"]
                    if link_url not in process_links:
                        process_links.add(link_url)
                        link_check = urlopen(link_url)
                        if link_check:
                            bsObj = BeautifulSoup(link_check.read(), "html.parser")
                            information = list(info.get_text().strip()for info in bsObj.find_all("span", {"class":"w2dc-field-content"}))
                            writer.writerow(information)
    except URLError as urler:
        print(f"Попытка соединения с ресурсом не успешна: {urler}")


if __name__ == "__main__":
    dental_data_parsing('https://example_url.com/somedirectory')