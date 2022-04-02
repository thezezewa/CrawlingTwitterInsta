import re
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

insta_url = "https://www.instagram.com/explore/tags/"


def get_driver():
    driver_option = webdriver.ChromeOptions()
    driver_option.add_argument('--headless')
    driver_option.add_argument('--lang=ko_KR')
    driver_option.add_argument('--no-sandbox')
    driver_option.add_argument("--disable-dev-shm-usage")
    driver_option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    #driver = webdriver.Chrome('D:\JSU\crawler\chromedriver.exe.exe.exe')
    #driver = webdriver.Chrome('/mnt/d/JSU/crawler/chromedriver.exe.exe.exe', chrome_options=driver_option)
    driver = webdriver.Chrome('./chromedriver.exe.exe', chrome_options=driver_option)
    #driver = webdriver.Chrome('/mnt/d/JSU/crawler/chromedriver.exe.exe.exe')

    #driver.implicitly_wait(3)

    return driver


def make_link_list(driver):
    link = []
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for line in soup.find_all(name='div', attrs={'class': 'Nnq7C weEfm'}):
            title = line.select('a')[0]
            textlink = title.attrs['href']
            if textlink in link:
                pass
            else:
                link.append(textlink)
            title = line.select('a')[1]
            textlink = title.attrs['href']
            if textlink in link:
                pass
            else:
                link.append(textlink)
            title = line.select('a')[2]
            textlink = title.attrs['href']
            if textlink in link:
                pass
            else:
                link.append(textlink)


        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue

    return link


def link_crawl(driver, link_list):
    result_file = open('instagram_곰취_1.txt', 'w', encoding="utf-8")
    for link in link_list:
        crawl_url = 'https://www.instagram.com' + link
        driver.get(crawl_url)
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "C4VMK")))
        html = driver.page_source
        time.sleep(0.5)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            text = soup.find_all('div', {'class': 'C4VMK'})[0].find_all('span')[0].text
            #p = re.compile("산마늘|곰취")
            #if p.search(text):
                #pass
            #else:
                #continue
        except Exception as e:
            text = ""
            print(str(e))
            print(crawl_url)

        try:
            text_time = soup.find_all('time', {'class': '_1o9PC Nzb55'})[0].get('title')
            #text_time = datetime.datetime.strptime(text_time, "%b %d, %Y").date()
            #text_time = text_time.strftime("%Y년 %m월 %d일".encode('unicode-escape').decode()).encode().decode('unicode-escape')
        except Exception as e:
            text_time = ""
            print(str(e))
            print(crawl_url)

        result_file.write(str(crawl_url) + "\t" + str(text) + "\t" + str(text_time) + "\n")

    result_file.close()


def main(text):
    driver = get_driver()
    driver.get(insta_url + text)
    time.sleep(2)

    link_list = make_link_list(driver)
    link_crawl(driver, link_list)


if __name__ == "__main__":
    text = "외식배달"
    main(text)
