import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


class Search:
    def __init__(self, search_term):
        self.search_term = search_term
        with open('output.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Store', 'Name', 'price', 'Link'])

    def alta(self):
        url = f'https://alta.ge/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q={self.search_term}&dispatch=products.search&items_per_page=1000'
        r = requests.get(url.format(search_term=self.search_term))
        soup = BeautifulSoup(r.text, 'html.parser')
        products = soup.find_all('div', attrs={'class': 'ty-column3'})
        tags = soup.find_all('a', attrs={'class': 'product-title'})
        prices = soup.find_all('span', attrs={'class': 'ty-price-num'})
        num = 0
        with open('output.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for product, tag, price in zip(products, tags, prices):
                num += 1
                name = tag.text.strip()
                link = product.find('a', class_='product-title').get('href')
                amount = price.text.strip()
                output = f"Alta | {num} | {name} | {amount}₾ | {link}"
                writer.writerow(["Alta", name, f"{amount}", link])
                print(output)

    def ee(self):
        url = "https://api.ee.ge/07072022/product/filter_products"
        payload = {
            "min_price": 0,
            "max_price": 0,
            "category": "",
            "sort_by": "",
            "item_per_page": 1000,
            "page_no": "",
            "search_text": self.search_term,
            "sale_products": 0,
            "slug": "",
            "pageno": ""
        }
        r = requests.request("POST", url, json=payload)
        num = 0
        with open('output.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for item in r.json()["data"]:
                num += 1
                a = item["parent_category_slug_gr"]
                b = item["category_slug_gr"]
                c = item["product_slug_gr"]
                output = f'Elit | {num} | {item["product_name"]} | {item["actual_price"]}₾ | https://ee.ge/{a}/{b}/{c}'
                writer.writerow(
                    ['Elit', item["product_name"], f'{item["actual_price"]}', f'https://ee.ge/{a}/{b}/{c}'])
                print(output)

    def ada(self):
        url = "https://api.adashop.ge/api/v1/products/rest_search/search"
        payload = {"search": self.search_term}
        r = requests.request("POST", url, json=payload)
        num = 0
        with open('output.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for item in r.json()["searched_products"]:
                num += 1
                output = f'Ada | {num} | {item["product_name"]} | {item["price_with_price_tag"]}₾ | https://adashop.ge/product/{item["_id"]}'
                writer.writerow(['Ada', item["product_name"],
                                f'{item["price_with_price_tag"]}', f'https://adashop.ge/product/{item["_id"]}'])
                print(output)

    def zoomer(self):
        url = f'https://zoommer.ge/search?q={self.search_term}&CategoryIds=0'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        products = soup.find_all('h4')
        prices = soup.find_all('div', attrs={'class': 'product_new_price'})
        links = soup.find_all(
            'a', attrs={'class': 'carousel-inner product_link'})
        num = 0
        with open('output.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for product, price, link in zip(products, prices, links):
                num += 1
                name = product['title']
                cost = price.text.strip().replace('₾', '')
                domain = link.get('href')
                output = f'Zoomer | {num} | {name} | {cost} | https://zoommer.ge{domain}'
                writer.writerow(["Zoomer", name, cost,
                                f'https://zoommer.ge{domain}'])
                print(output)

        mores = soup.find_all('a', attrs={'class': 'show_more_btn'})
        for more in mores:
            page = more.get('href')
            if page is not None:
                r1 = requests.get(page)
                soup1 = BeautifulSoup(r1.content, 'html.parser')
                products1 = soup1.find_all('h4')
                prices1 = soup1.find_all(
                    'div', attrs={'class': 'product_new_price'})
                links1 = soup1.find_all(
                    'a', attrs={'class': 'carousel-inner product_link'})
            with open('output.csv', 'a', encoding='utf-8', newline='') as f1:
                writer1 = csv.writer(
                    f1, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for product1, price1, link1 in zip(products1, prices1, links1):
                    num += 1
                    name1 = product1['title']
                    cost1 = price1.text.strip().replace('₾', '')
                    domain1 = link1.get('href')
                    output1 = f'Zoomer | {num} | {name1} | {cost1} | https://zoommer.ge{domain1}'
                    writer1.writerow(
                        ["Zoomer", name1, cost1, f'https://zoommer.ge{domain1}'])
                    print(output1)

    def all(self):
        self.alta()
        self.ee()
        self.ada()
        self.zoomer()


def sort(decision: bool):
    if decision == True:
        df = pd.read_csv("output.csv")
        try:
            df['price'] = df['price'].astype(str).str.strip()
            df['price'] = df['price'].astype(str).str.replace(' ', '')
            df['price'] = df['price'].astype(int)
        except ValueError:
            df['price'] = df['price'].astype(float).astype(int)
        df = df.sort_values(by="price")
        df.to_csv("output.csv", index=False)
        print('\nsorted!')
    elif decision == False:
        return


choice = input('Search Term: ')
sortq = input('Do you want to sort output by price?(y/n): ')
Search(choice).all()

if sortq.lower() in ['y', 'yes']:
    sort(True)
elif sortq.lower() in ['n', 'no']:
    sort(False)
