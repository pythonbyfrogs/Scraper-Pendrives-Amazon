#Imports
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

#Acess to web
url = "https://www.amazon.com.br/s?k=pendrive"
session = requests.Session()

headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language":"pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1"
    }

#Entering the site
def enter_site():
    for trin in range(1, 6):
        try:
            time.sleep(2)
            code = session.get(url, headers=headers, timeout=20)

            if code.status_code == 200:
                print("Just pythonic!")
                return code

            print(
                f"Try {trin}/5: "
                f"HTTP {code.status_code}"
            )

        except requests.exceptions.RequestException as error:
            print(f"Try {trin}/5: {error}")

        if trin < 5:
            time.sleep(5)

    print("Site cannot be acessed in 5 trys.")
    return None

#Acessing
code = enter_site()
if code is None:
    print ("Error at scraping")
else:
    soup = BeautifulSoup(code.text, 'html.parser')



    #Pick offers
    time.sleep(2)
    offers_products = soup.find_all("div", attrs={"data-component-type":"s-search-result"})

    list_products = []

    for b in offers_products:
        try:
            #Title
            tag_title = b.find("h2", attrs={"class":"a-size-base-plus a-spacing-none a-color-base a-text-normal"})
            Product = tag_title.text.strip() if tag_title else "Unavailable"

            #Search for price
            tag_price = b.find("span", attrs={"class":"a-price"})
            dirt_price = tag_price.text.strip() if tag_price else "Unavailable"
            if "R$" in dirt_price:
                price = "R$" + dirt_price.split("R$")[1].strip()
            else:
                price = dirt_price
            
            #Validate
            if (
                not Product.strip()
                or Product == "Unavailable"
                or not price.startswith("R$")
            ):
                continue

            list_products.append({"Product": Product, "Price": price})
            print(f"Product: {Product} | Price: {price}")

        except Exception:
            continue

    #Create DataFrame
    if list_products:
        df = pd.DataFrame(list_products)
        df = df.drop_duplicates(subset=["Product", "Price"])
        df.to_csv("Pendrives_amazon.csv", index= False, encoding="utf-8")
        print("\n DataFrame generated!")
    else:
        print("\n Error at generating DataFrame")
