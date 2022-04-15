from selenium import webdriver
from urllib import parse
import time
import warnings
from bs4 import BeautifulSoup
from selenium.webdriver import Keys

warnings.filterwarnings('ignore')

driver = webdriver.Chrome(executable_path='./chromedriver')

def getDriver():
    # driver_option = webdriver.ChromeOptions()
    # driver_option.add_argument('--headless')
    # driver_option.add_argument('--lang=ko_KR')
    # driver_option.add_argument('--no-sandbox')
    # driver_option.add_argument("--disable-dev-shm-usage")
    # driver_option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('./chromedriver')

    return driver


def twitter_serach(driver, str):
    URL = 'https://twitter.com/search?q='+parse.quote(str)+'&src=typed_query'

    # URL 접속
    driver.get(url=URL)
    time.sleep(7)

    # 텍스트들을 담을 리스트
    text_list = []

    while True:
        ss = driver.find_elements_by_css_selector('.css-1dbjc4n.r-j5o65s.r-qklmqi.r-1adg3ll.r-1ny4l3l')
        for s in ss:
            if 'account is temporarily unavailable because it violates the Twitter Media Policy. https://Learn more.' in s.text:
                continue
            else:
                text_list.append(s.text)
                print(s.text)
                print('------------------')

        page_down(4)
        time.sleep(7)

        if ss[-1].text == text_list[-1]:
            break

def page_down(t):
    body = driver.find_element_by_css_selector('body')

    for i in range(t):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)


if __name__ == "__main__":
    driver = getDriver()
    twitter_serach(driver, '외식배달')

