import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import warnings
warnings.filterwarnings('ignore')

URL =  'https://www.instagram.com'
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
html = driver.get(URL)
time.sleep(3)

# 아이디, 비밀번호 전송 후 로그인
input_id = driver.find_element_by_name('username')
input_id.send_keys('aoakdnf_c')
time.sleep(5)

input_pw = driver.find_element_by_name('password')
input_pw.send_keys('Joonyeong.1')
time.sleep(7)

login_btn = driver.find_element_by_css_selector('.sqdOP.L3NKy.y3zKF     ')
login_btn.click()
time.sleep(3)

# 로그인 정보를 저장하시겠어요? 나중에 하기 클릭
later_btn = driver.find_element_by_css_selector('.sqdOP.yWX7d.y3zKF     ')
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

# 검색창 input에 '외식배달'이라고 검색하였을 때 나오는 첫번째 결과 조희 및 클릭
a_tag = driver.find_element_by_css_selector('.-qQT3')
a_tag.click()
time.sleep(7)

# 첫번째 게시물 클릭
first_post = driver.find_element_by_css_selector('._9AhH0')
first_post.click()
time.sleep(5)

# 게시물의 계정명 및 내용
account = driver.find_element_by_css_selector('.C4VMK')
post_time = driver.find_element_by_css_selector('._1o9PC')
print(account.text.strip())
print(post_time.text.strip())
time.sleep(5)

# 다음 게시글 넘기기
next_btn = driver.find_element_by_css_selector('.QBdPU ')
next_btn.click()
time.sleep(5)


