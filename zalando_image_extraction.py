import theMain
import pandas as pd
from selenium.webdriver.common.by import By

DATABASE_FILE = "zalando_database.csv"
MAX_PAGES = 100
CATEGORIES = ['Jacket', 'Pants', 'Jeans', 'Shorts', 'T-shirt',
              'Pullover', 'Bag', 'Cap', 'Sandal', 'Skirt']

def loadDatabase():
    df = pd.read_csv(DATABASE_FILE)
    return df
def saveDatabase(df):
    df.to_csv(DATABASE_FILE, index=False)


def main_func():
    driver = theMain.initiate_driver()
    for category in CATEGORIES:
        for page in range(1,MAX_PAGES):
            try:
                df = loadDatabase()
                website = driver.get(f'https://www.zalando.nl/alle/?q={category}&p={page}')
                theMain.scroll_down_the_page(driver, website, 5)
                images = driver.find_elements(By.TAG_NAME, 'img')
                # images = driver.find_elements_by_tag_name('img')

                for image in images:
                    # print(image.get_attribute('src'))
                    try:
                        Image_URL = image.get_attribute('src')
                        df.loc[-1] = [category, Image_URL]
                        df.index = df.index + 1  # shifting index
                    except:
                        pass
                saveDatabase(df)
                print(f'Completing {round((page / MAX_PAGES) * 100, 2)}% of {category} category')
            except:
                pass
if __name__ == '__main__':
    main_func()