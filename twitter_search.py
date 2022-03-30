import re
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver


def get_driver():
    driver_option = webdriver.ChromeOptions()
    driver_option.add_argument('--headless')
    driver_option.add_argument('--lang=ko_KR')
    driver_option.add_argument('--no-sandbox')
    driver_option.add_argument("--disable-dev-shm-usage")
    driver_option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('./chromedriver.exe')

    driver.implicitly_wait(3)

    return driver


def page_scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def remove_link(text):
    link1 = re.compile('(( )?(https|http):[a-zA-Z0-9._/?&@=]+)|( )?(pic.twitter.com[a-zA-Z0-9/]+)')
    link2 = re.compile('( )?https://youtu.be/\w+')

    if link1.search(text):
        text = link1.sub("", text)

    if link2.search(text):
        text = link2.sub("", text)

    return text


def twit_search(driver):
    p = re.compile('산.{1,2}마늘|산\n마늘')
    openline = re.compile("\n{1,}")

    textfile = open("twitter_2_headless.txt", "w", encoding="utf-8")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    twit_url = "https://www.twitter.com"
    tweet = soup.find_all(attrs={'class': 'content'})
    for t in tweet:
        nickname = t.find_all(attrs={'class': 'FullNameGroup'})[0].text.strip()
        text = t.find_all(attrs={'class': 'TweetTextSize js-tweet-text tweet-text'})[0].text.strip()
        if p.search(str(text)):
            continue
        text = openline.sub(" ", remove_link(text))

        link = twit_url + t.find_all(attrs={'class': 'tweet-timestamp js-permalink js-nav js-tooltip'})[0].get('href')
        twit_time = t.find_all(attrs={'class': 'tweet-timestamp js-permalink js-nav js-tooltip'})[0].text

        write_text = (link + "\t" + nickname + "\t" + text + "\t" + twit_time).replace("‏", "")
        textfile.write(write_text + "\n")
    textfile.close()


def main(text):
    twitter_url = "https://twitter.com/search?q=" + str(quote_plus(text)) + "%20since%3A2018-01-01%20until%3A2018-12-31&src=typd"

    driver = get_driver()
    driver.get(twitter_url)
    page_scroll_down(driver)

    twit_search(driver)


if __name__ == "__main__":
    text = ""
    main(text)