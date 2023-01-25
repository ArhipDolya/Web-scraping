from bs4 import BeautifulSoup
import requests
import re


# Scraping https://www.newegg.com
product = input('Type a link to the products you want to parse: \n')
url = product


def scraping():
    try:

        pages = 1
        how_many_pages = int(input('How many pages do you want to parse:\n')) + 1

        while pages < how_many_pages:

            print(f"------------------------PAGE-{pages}------------------------")

            responce = requests.get(f'{url}&page={pages}')
            soup = BeautifulSoup(responce.content, 'html.parser')
            items = soup.find_all('div', class_='item-container')

            # Contain variables
            items_table = {}
            lowest_price = 999999
            lowest_price_item = ''
            lowest_price_link = ''
            highest_price = 0
            highest_price_item = ''
            highest_price_link = ''

            for item in items:

                item_title = item.find('a', class_='item-title')
                item_price = item.find('ul', class_='price')
                current_price = item_price.find('li', class_='price-current')
                title = item_title.get_text(strip=True)

                if current_price.strong is None:
                    continue

                else:
                    cur = current_price.strong.text

                    if ',' in cur:
                        cur = cur[0] + cur[2:]

                    if int(cur) < lowest_price:
                        lowest_price = int(cur)
                        lowest_price_item = title
                        lowest_price_link = item_title['href']

                        if int(cur) > highest_price:
                            highest_price = int(cur)
                            highest_price_item = title
                            highest_price_link = item_title['href']

                    items_table[title] = f"Price: {current_price.strong.text + '$'} \nLink: {item_title['href']}"


            for item, price in items_table.items():
                print(item)
                print(price)
                print()


            print(f"Lowest price: {lowest_price}$\nLowest price item: {lowest_price_item}\nLowest price item link: {lowest_price_link}\n")
            print(f"Highest price: {highest_price}$\nHighest price item: {highest_price_item}\nHighest price item link: {highest_price_link}")
            pages += 1

    except:
        print("Something went wrong!")


if __name__ == '__main__':
    scraping()

