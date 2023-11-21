import requests
from bs4 import BeautifulSoup
from typing import List
from fake_useragent import UserAgent
from pydantic import BaseModel
import sqlite3
import datetime

HEADERS = {
    "User-Agent": UserAgent().random,
    "Referer": "https://www.amazon.com/"
}

class Product(BaseModel):
    title: str = ''
    price: str = ''
    rating: str = ''
    url: str = ''
    image: str = ''

class ProductPrice(BaseModel):
    price: str = ''
    date: str = ''

def get_page(url: str, headers: dict) -> BeautifulSoup:
    """
    Gets the search page for a given url and 
    return the page as a BeautifulSoup object
    """

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        page = BeautifulSoup(response.content, 'html.parser')
        return page
    else:
        raise Exception(f'Failed to load page: {url}')
    
def get_products_from_search(query: str) -> List[Product]:
    """
    Gets the product information from the search page
    """

    # Get the search page
    url = f"https://www.amazon.com/s?k={query}"
    page = get_page(url, HEADERS)
    
    # Get the product results
    products = []
    product_results = page.find_all('div', {'data-component-type': 's-search-result'})
    for product_result in product_results:
        # Create a product object
        product = Product()

        # Get the product title
        title = product_result.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
        if title:
            product.title = title.text

        # Get the product price
        price = product_result.find('span', {'class': 'a-offscreen'})
        if price:
            product.price = price.text

        # Get the product rating
        rating = product_result.find('span', {'class': 'a-icon-alt'})
        if rating:
            product.rating = rating.text

        # Get the product url
        url = page.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        if url:
            product.url = 'https://www.amazon.com' + url['href']

        # Get the product image
        image = product_result.find('img', {'class': 's-image'})
        if image:
            product.image = image['src']

        # Append the product to the list of products
        products.append(product)

    return products

def get_product_from_url(url: str) -> Product:
    """
    Gets the product details from the product page
    """
    
    # Get the product page
    page = get_page(url, HEADERS)
    
    # Create a product object
    product = Product()

    # Get the product title
    title = page.find('span', {'id': 'productTitle'})
    if title:
        product.title = title.text.strip()

    # Get the product price
    price_symbol = page.find('span', {'class': 'a-price-symbol'})
    price_whole = page.find('span', {'class': 'a-price-whole'})
    price_fraction = page.find('span', {'class': 'a-price-fraction'})
    if price_symbol and price_whole and price_fraction:
        product.price = price_symbol.text + price_whole.text + price_fraction.text

    # Get the product rating
    rating = page.find('span', {'id': 'acrPopover'})
    if rating:
        product.rating = rating['title'].split()[0]

    # Get the product url
    product.url = url

    # Get the product image
    image = page.find('img', {'id': 'landingImage'})
    if image:
        product.image = image['src']

    return product

def save_product(product: Product):
    """
    Saves the product to a database
    """
    
    # Save the product to a SQLite database
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS products (
              id INTEGER PRIMARY KEY, 
              title TEXT NOT NULL, 
              rating TEXT NOT NULL, 
              url TEXT NOT NULL, 
              image TEXT NOT NULL)'''
    )
    
    # Insert the product into the table
    c.execute("INSERT INTO products (title, rating, url, image) VALUES (?, ?, ?, ?)", (product.title, product.rating, product.url, product.image))
    conn.commit()

    # # Get the product id
    # product_id = c.lastrowid

    # Close the connection
    conn.close()

    # Save the product price
    save_product_price(product)

    print(f"Saved product: {product.title}")

def save_product_price(product: Product):
    """
    Saves the product price to a database
    """
    
    # Save the product to a SQLite database
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS product_prices (
                id INTEGER PRIMARY KEY, 
                product_id INTEGER NOT NULL,
                price TEXT NOT NULL, 
                date TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id))'''
    )
    
    # Get the product from the database
    c.execute("SELECT * FROM products WHERE url=?", (product.url,))
    product_id = c.fetchone()[0]
    
    # Insert the product into the table
    c.execute("INSERT INTO product_prices (product_id, price, date) VALUES (?, ?, ?)", (product_id, product.price, datetime.datetime.now()))

    # Close the connection
    conn.close()

if __name__ == '__main__':
    product = get_product_from_url('https://www.amazon.com/Portable-Mechanical-Keyboard-MageGee-Backlit/dp/B098LG3N6R/ref=sr_1_3?_encoding=UTF8&content-id=amzn1.sym.12129333-2117-4490-9c17-6d31baf0582a&keywords=gaming%2Bkeyboard&pd_rd_r=ff5def34-54e3-42be-aeef-24ea37bb0caa&pd_rd_w=tw2v4&pd_rd_wg=PTZml&pf_rd_p=12129333-2117-4490-9c17-6d31baf0582a&pf_rd_r=6BMNT3NB1RDBNZW2D6RT&qid=1700064035&sr=8-3&th=1')
    print(product)

    save_product(product)
