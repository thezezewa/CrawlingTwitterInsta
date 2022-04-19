import pandas as pd
from selenium import webdriver
import time
import warnings
warnings.filterwarnings('ignore')

# url, account, body, time, hashtag를 담을 리스트
url_lists = []
account_lists = []
body_lists = []
time_lists = []
hashtag_lists = []



URL =  'https://www.instagram.com'
driver = webdriver.Chrome(executable_path='./chromedriver')
html = driver.get(url = URL)
time.sleep(3)

# 아이디, 비밀번호 전송 후 로그인
input_id = driver.find_element_by_name('username')
input_id.send_keys('user_id')
time.sleep(5)

input_pw = driver.find_element_by_name('password')
input_pw.send_keys('user_pw')
time.sleep(7)

login_btn = driver.find_element_by_css_selector('.sqdOP.L3NKy.y3zKF     ')
login_btn.click()
time.sleep(3)

# 로그인 정보를 저장하시겠어요? 나중에 하기 클릭
later_btn = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/div/div/div/button')
later_btn.click()
time.sleep(3)

# 알림 설정 나중에 하기 클릭
later_btn2 = driver.find_element_by_css_selector('.aOOlW.HoLwm ')
later_btn2.click()
time.sleep(3)

# 검색창 input 태그에 키워드 전달
input_search = driver.find_element_by_css_selector('.XTCLo.d_djL.DljaH')
input_search.send_keys('외식배달')
time.sleep(3)

# 검색창 input에 '외식배ㅇ달'이라고 검색하였을 때 나오는 첫번째 결과 조희 및 클릭
a_tag = driver.find_element_by_css_selector('.-qQT3')
a_tag.click()
time.sleep(7)

# 첫번째 게시물 클릭
first_post = driver.find_element_by_css_selector('._9AhH0')
first_post.click()
time.sleep(5)


count = 0
while True:
    idx = []
    # 게시물의 계정명 및 내용
    account = driver.find_element_by_css_selector('.C4VMK')
    post_time = driver.find_element_by_css_selector('._1o9PC')

    print(driver.current_url)
    url_lists.append(driver.current_url.strip())
    print(account.text.split('\n')[0])
    account_lists.append(account.text.split('\n')[0].strip())
    #   \n 단위로 나눈 body 값들 정제
    new_line = ''
    for index, line in enumerate(account.text.split('\n')):
        # 계정명
        if (index == 0) | (index == len(account.text.split('\n'))-1):
            continue
        if line == '':
            continue
        else:
            new_line = new_line + ' ' +line
    print(new_line.strip())
    body_lists.append(new_line.strip())
    print(post_time.text.strip())
    time_lists.append(post_time.text.strip())

    hashtags = ''
    temp = []
    for j in range(len(account.text.split('\n'))):
        for k in range(len(account.text.split('\n')[j].split(' '))):
            print(account.text.split('\n')[j].split(' ')[k])
            if '#' in account.text.split('\n')[j].split(' ')[k]:
                temp.append(account.text.split('\n')[j].split(' ')[k])

    for ht in temp:
        hashtags = hashtags + ' ' + ht

    hashtag_lists.append(hashtags)
    time.sleep(5)

    # 다음 게시글 넘기기
    try:
        if count == 0:
            next_btn = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/button')
        else:
            next_btn = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[2]/button')
        next_btn.click()
        count += 1
        time.sleep(7)

    # 다음 게시글 버튼이 존재하지 않을 경우
    except:
        break

# 데이터프레임 생성
df_insta = pd.DataFrame({'url':url_lists, 'account':account_lists, 'body':body_lists, 'time':time_lists, 'hashtag':hashtag_lists})
df_insta.to_csv('./instagram_result_외식배달.csv', encoding='utf-8', index=False)