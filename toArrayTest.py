import requests, io, cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

DATABASE_FILE = 'zalando_database.csv'
NEW_DATABASE_FILE = 'feature_label.csv'
df = pd.read_csv(DATABASE_FILE)
IMAGE_SIZE = 32


def saveDatabase(df):
    df.to_csv(NEW_DATABASE_FILE, index=False)


def image_to_array(img_url):
    response = requests.get(img_url)
    img = Image.open(io.BytesIO(response.content))
    image = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
    # inverted = np.invert(image)
    imgArray = np.asarray(image)
    cv_im = cv2.cvtColor(imgArray, cv2.COLOR_BGR2GRAY)
    return cv_im / IMAGE_SIZE

def plot_image(img):
    #cv_im = image_to_array(img)
    cv_im = img
    plt.figure()
    plt.imshow(cv_im)
    plt.colorbar()
    plt.grid(False)
    plt.show()

def demonstrate():
    plt.figure(figsize=(10, 10))
    index = [112, 6268, 7546, 11446, 14612, 21659, 30192, 39202, 46990, 50816]
    for i in index:
        plt.subplot(5, 5, index.index(i) + 1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(plot_image(df.iloc[i][1]), cmap=plt.cm.binary)
        plt.xlabel(df.iloc[i][0])
        plt.colorbar()
        plt.grid(False)
    plt.show()

def initiate_dfMain():
    COLUMNS_SIZE = IMAGE_SIZE*IMAGE_SIZE
    columns = ['label']
    for i in range(COLUMNS_SIZE):
        columns.append(f'pixel{i}')

    dfMain = pd.DataFrame(columns=columns)
    saveDatabase(dfMain)
    return dfMain



def main_func():
    print('Initializing dfMain...')
    dfMain = initiate_dfMain()

    print('dfMain Initialized!')

    CATEGORIES = {'Jacket':0, 'Pants':1, 'Jeans':2, 'Shorts':3, 'T-shirt':4,
                  'Pullover':5, 'Bag':6, 'Cap':7, 'Sandal':8, 'Skirt':9}

    for row in range(1, len(df)):
        try:

            category_string = df.iloc[row][0]
            category_value = int(CATEGORIES[category_string])

            image_url = df.iloc[row][1]
            image_array = image_to_array(image_url)

            reshaped_image_array = image_array.reshape(IMAGE_SIZE*IMAGE_SIZE)
            reshaped_image_array = np.insert(reshaped_image_array,0,category_value)

            dfMain = dfMain.append(pd.DataFrame(reshaped_image_array.reshape(1, -1), columns=dfMain.columns), ignore_index=True)
            print(f'Completing => {round((row / len(df)) * 100, 2)}%. Category => {category_string}')

            if row % 50:
                saveDatabase(dfMain)
                print('Saved database!')

        except Exception as e:
            print(f'----EXCEPTION {e}----')


main_func()
