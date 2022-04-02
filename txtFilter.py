import pandas as pd
import re

week = re.compile('\d+주|수정됨 · \d+주|수정됨·\d+주')
special = re.compile('_|/|\-|・・・|\.')

# 각각의 컬럼에 담을 리스트 생성
url_lists = []
account = []
body = []
time = []

# txt 파일을 읽어서 정해진 정규표현식에 맞추어 정제
with open('./txt/instagram_외식배달.txt', 'r') as f:
    for index, text in enumerate(f):
        line = text.strip('\n').strip()

        # line이 빈칸일 경우 넘기기
        if line == '':
            continue

        # 주, 수정됨 주가 담긴 line
        if week.match(line):
            continue
        # 주, 수정됨 주가 담기지 않는 line
        else:
            # .만 존제하는 line
            if special.match(line):
                continue
            else:
                if 'URL : ' in line:
                    url_lists.append(line[6:])
                print(index, line)




