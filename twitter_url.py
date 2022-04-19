import pandas as pd
from selenium import webdriver
from urllib import parse
import time
import warnings
from tqdm import tqdm
from selenium.webdriver import Keys
warnings.filterwarnings('ignore')

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
    url_list = []
    URL = 'https://twitter.com/search?q='+parse.quote(str)+'&src=typed_query'

    # URL 접속
    driver.get(url=URL)
    time.sleep(3)

    # 텍스트들을 담을 리스트
    text_list = []

    # 처음 페이지의 스크롤 높이를 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 모든 게시글을 불러오는 while 반복문
    while True:
        # 해당 페이지의 게시글 모두 가져오기
        ss = driver.find_elements_by_css_selector('.css-1dbjc4n.r-1loqt21.r-18u37iz.r-1ny4l3l.r-1udh08x.r-1qhn6m8.r-i023vh.r-o7ynqc.r-6416eg')

        # 부적절한 게시물일 경우 크롤링할 때 해당 문구가 나오는데 이를 필터링
        for s in ss:
            if 'account is temporarily unavailable because it violates the Twitter Media Policy.' in s.text:
                continue
            else:
                text_list.append(s.text)
                s.click()
                time.sleep(5)
                url_list.append(driver.current_url)
                driver.back()
                time.sleep(5)


        # pageDown 버튼 클릭
        page_down(4)
        time.sleep(7)

        # 페이지 다운 후 스크롤 높이 다시 가져오기
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 페이지의 끝과 스크롤의 끝이 일치할 경우 반복문 나오기
        if new_height == last_height:
            break
        last_height = new_height

    return text_list, url_list

'''
기능 : page down 키를 누르는 동작을 하며, 스크롤을 내리듯이 페이지를 내려준다.
파라미터 : t [몇 번을 누를 것인지를 설정하는 변수]
'''
def page_down(t):
    body = driver.find_element_by_css_selector('body')

    for i in range(t):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)

'''
기능 : 문자열을 숫자로 변환할 수 있는지를 True, False로 반환하는 함수
 - 크롤링한 내용 중 뒤에 좋아요, 리트윗 수 등을 제외시키기 위해 만든 함수
파라미터 : s [숫자로 변환할 문자열]
'''
def isNumberStr(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

'''
기능 : 
'''
def make_df(li, url_lists):
    li_lists = li
    id_list = []
    account_list = []
    date_list = []
    content_list = []
    url_list = url_lists

    # 리스트의 내용 모두 나열
    for li in tqdm(li_lists):
        new_word = ''
        # 한 게시글을 줄바꿈 단위로 나열
        for index, word in enumerate(li.split('\n')):
            # 한 게시글에서의 생략할 표현들 제거
            if index == 0:
                id_list.append(word.strip())
            elif index == 1:
                account_list.append(word.strip())
            elif index == 3:
                if '년' not in word.strip():
                    date_list.append('2022년 ' + word.strip())
                else:
                    date_list.append(word.strip())
            else:
                if (word.strip() == '·') | (word.strip() == '') | (word.strip() == '님에게 보내는 답글') | (word.strip() == '이 스레드 보기') | (word.strip() == '님, 다른 사람 2명에게 보내는 답글') | (word.strip() == '님이 공유') \
                            | ('· ' in word.strip()):
                    continue
                if isNumberStr(word.strip()):
                    continue
                else:
                    new_word = new_word + ' ' + word.strip()

        content_list.append(new_word.strip())


    df = pd.DataFrame({'id':id_list,'account':account_list, 'date':date_list, 'content':content_list, 'url':url_list})
    df.to_csv('./csv/twitter_result_외식포장.csv', encoding='utf-8',  index=False)




if __name__ == "__main__":
    driver = getDriver()
    ts = twitter_serach(driver, '외식포장')
    make_df(ts)
