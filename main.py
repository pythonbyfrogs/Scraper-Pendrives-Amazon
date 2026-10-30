import pandas as pd
import time
from datetime import datetime
from pathlib import Path
from Scrapers import Amazon_Kingston
from Scrapers import Amazon_SanDisk

def run_scraper(scraper_function):
    for attempt in range(1, 6):
        try:
            products = run_scraper(scraper_function)

            if products:
                return products

            print(f"Attempt {attempt}/5: nothing found.")

        except Exception as error:
            print(f"Attempt {attempt}/5: {error}")

        if attempt < 5:
            time.sleep(5)

    print("Fail after 5 attempts.")
    return []

#Saving in "Dataframes" folder
data_folder = Path("Dataframes")
data_folder.mkdir(exist_ok=True)
date = datetime.now().strftime("%Y-%m-%d")

def main():
    all_products = []

    scrapers = [
        ("Amazon_Kingston", Amazon_Kingston.scraper),
        ("Amazon_SanDisk", Amazon_SanDisk.scraper)
    ]

    for store_name, scraper_function in scrapers:
        print(f"\nScraping {store_name}...")

        try:
            products = scraper_function()

            for product in products:
                all_products.append({
                    "Store": store_name,
                    "Product": product["Product"],
                    "Price": product["Price"],
                })

            print(f"Products collected: {len(products)}")

        except Exception as error:
            print(f"Error scraping {store_name}: {error}")

    if not all_products:
        print("\nNo products were collected.")
        return

    dataframe = pd.DataFrame(all_products)
    print("\nChoose the export format:")
    print("1 - CSV")
    print("2 - Excel (.xlsx)")
    choice = input("Your choice (1/2): ").strip()

    if choice == "1":
        dataframe.to_csv(
            data_folder / f"pendrives_{date}.csv",
            index=False,
            sep=";",
            encoding="utf-8-sig"
        )
        print(f"pendrives_{date}.csv")

    elif choice == "2":
        dataframe.to_excel(
            "isopodes.xlsx",
            index=False
        )
        print(f"pendrives_{date}.xlsx")

    else:
        print("\nInvalid option. No file was exported.")


if __name__ == "__main__":
    main()