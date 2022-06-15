from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

DATABASE_FILE = "database.csv"

class Product:

    def __init__(self, element):
        self.element = element
        self.full_info = self.element.text

    def get_url(self):
        return self.element.get_attribute('href')

    def get_title(self):
        self.title = str(self.full_info).splitlines()[0]
        return self.title

    def get_price(self):
        self.price = str(self.full_info).splitlines()[1]
        return self.price

    def get_rating(self):
        raw_info = str(self.full_info).splitlines()
        for line in raw_info:
            if 'sold' in line:
                info = str(line).split(' ')
                rating_raw = info[-1]
                self.rating = str(rating_raw).replace('sold', '')
                return self.rating
        return None

    def get_total_sale(self):
        raw_info = str(self.full_info).splitlines()
        for line in raw_info:
            if 'sold' in line:
                info = str(line).split(' ')
                self.total_sale = info[0]
                return self.total_sale
        return None


    def get_seller_info(self):
        return self.element.find_element(By.CLASS_NAME,'_7CHGi').get_attribute('href')

    def is_limited_offer(self):
        self.is_limited_offer = False
        if 'Limited Offer' in str(self.full_info):
            self.is_limited_offer = True
        return self.is_limited_offer

    def is_new_user_deal(self):
        self.is_new_user_deal = False
        if 'New User Deal' in str(self.full_info):
            self.is_new_user_deal = True
        return self.is_new_user_deal

    def is_free_shipping(self):
        self.is_free_shipping = False
        if 'Free Shipping' in str(self.full_info):
            self.is_free_shipping = True
        return self.is_free_shipping

    def is_free_return(self):
        self.is_free_return = False
        if 'Free Return' in str(self.full_info):
            self.is_free_return = True
        return self.is_free_return

    def is_10_day_delivery(self):
        self.is_10_day_delivery = False
        if '10-Day Delivery' in str(self.full_info):
            self.is_10_day_delivery = True
        return self.is_10_day_delivery

    def is_combined_delivery(self):
        self.is_combined_delivery = False
        if 'Combined Delivery' in str(self.full_info):
            self.is_combined_delivery = True
        return self.is_combined_delivery


def loadDatabase():
    df = pd.read_csv(DATABASE_FILE)
    return df

def saveDatabase(df):
    df.to_csv(DATABASE_FILE, index=False)

def addProduct(Title, Price, Total_Sale, Rating, Is_New_User_Deal,
               Is_Limited_Offer, Is_10_Day_Delivery, Is_Combined_Delivery,
               Is_Free_Shipping, Is_free_Return, URL):
    df = loadDatabase()
    df.loc[-1] = [Title, Price, Total_Sale, Rating, Is_New_User_Deal,
                  Is_Limited_Offer, Is_10_Day_Delivery, Is_Combined_Delivery,
                  Is_Free_Shipping, Is_free_Return, URL]
    df.index = df.index + 1  # shifting index
    #df = df.sort_index()  # sorting by index
    saveDatabase(df)

def initiate_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('start-maximized')
    # options.add_argument('disable-infobars')
    # options.add_argument('--disable-extensions')
    prefs = {
        "translate_whitelists": {"": "en"},
        "translate": {"enabled": "True"}
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome('/Users/chalexander/Desktop/chromedriver', options=options)
    return driver

def scroll_down_the_page(driver, page ,speed=5):
    y = 10000
    for timer in range(0, speed):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 5000
        time.sleep(1)
    #print(f'Page {page} scrolled')

def main():
    driver = initiate_driver()
    for page in range(1,60):
        print(f'Fetching page {page}')
        website = driver.get(f'https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText=humidifier&ltype=wholesale&SortType=default&g=y&page={page}')
        scroll_down_the_page(driver=driver, page=page ,speed=5)
        product = driver.find_elements(By.XPATH, '//a[@class="_3t7zg _2f4Ho"]')

        try:
            for item in product:
                product = Product(element=item)
                if not product.get_title() == 'AD':
                    addProduct(
                    Title=product.get_title(),
                    Price=product.get_price(),
                    Total_Sale=product.get_total_sale(),
                    Rating=product.get_rating(),
                    Is_New_User_Deal=product.is_new_user_deal(),
                    Is_Limited_Offer=product.is_limited_offer(),
                    Is_10_Day_Delivery=product.is_10_day_delivery(),
                    Is_Combined_Delivery=product.is_combined_delivery(),
                    Is_Free_Shipping=product.is_free_shipping(),
                    Is_free_Return=product.is_free_return(),
                    URL=product.get_url()
                    )
                else:
                    pass

        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    main()



