#Imports
import requests
from bs4 import BeautifulSoup
import time

url = "https://www.amazon.com.br/s?k=pen+drive+Kingston"
session = requests.Session()

headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language":"pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1"
    }

#Entering the site (pagination + attempts)
def enter_site(page_url):
    for trin in range(1, 6):
        try:
            time.sleep(2)
            code = session.get(page_url, headers=headers, timeout=20)

            if code.status_code == 200:
                print(f"Here we go! {page_url}")
                return code

            print(f"Try {trin}/5: HTTP {code.status_code}")

        except requests.exceptions.RequestException as error:
            print(f"Try {trin}/5: {error}")

        if trin < 5:
            time.sleep(5)

    print("Site cannot be accessed in 5 tries.")
    return None

#Main function
def scraper():
    list_products = []

    #Pagination loop (multiple pages)
    for page in range(1, 6):
        page_url = f"{url}&page={page}"
        print(f"\n--- Page {page} ---")
        code = enter_site(page_url)
        
        #Attempt
        if code is None:
            print(f"Error accessing page {page}.")
            continue

        soup = BeautifulSoup(code.text, "html.parser")
        offers_products = soup.find_all("div", attrs={"class": "sg-col-inner"})

        print(f"Ads found: {len(offers_products)}")

        for b in offers_products:
            try:
                #Title
                title_element = b.find("h2", attrs={"class": ("a-size-base-plus a-spacing-none a-color-base a-text-normal")})
                #Price_int
                price_element = b.find(
                    "span", attrs={"class": "a-price-whole"})
                #Price_fraction
                fraction_element = b.find("span", attrs={"class": "a-price-fraction"})

                if not title_element or not price_element:
                    continue

                #Formatting stuff
                title = title_element.get_text(strip=True)
                title_lower = title.lower()
                #Filtering stuff
                if "kingston" not in title_lower:
                    continue

                if "sandisk" in title_lower or "multi" in title_lower:
                    continue

                price_int = price_element.get_text(strip=True).replace(",", "")
                price_fraction = (fraction_element.get_text(strip=True) if fraction_element else "00")
                price = f"R$ {price_int},{price_fraction}"

                #More formating...
                list_products.append({"Product": title, "Price": price})
                print(f"Product: {title} | Price: {price}")

            except Exception as error:
                print(f"Error at processing ad: {error}")
                continue

        time.sleep(2)
    return list_products

if __name__ == "__main__":
    products = scraper()
    print(f"\nTotal: {len(products)} products found.")