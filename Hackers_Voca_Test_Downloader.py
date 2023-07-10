# 라이브러리 선언
from urllib import request
import time

# 프로그램에 실행에 필요한 변수 선언 (사용자 설정 값)
start_day = 1 # 시험생성 시작 일
end_day = 31 # 시험생성 종료 일
q_num = 50 # 문항 수
q_type = 2 # 문제 유형
q_range = 3 # 출제 범위
answer_sheet = 'Y' # 문제지 출력 여부 (Y/N)

# 접속하여 원하는 시험지를 가져옴
# 접속하여 원하는 시험지를 얻어옴
for day in range(start_day,end_day):
    url = f'https://www.gohackers.com/modules/contents/lang.korean/pages/voca_program/pdf_paper.php?m=contents&front=voca_program&mode=pdf&iframe=Y&day1={day}&day2={day}&question={q_num}&type={q_type}&cate={q_range}&answer={answer_sheet}'
    with urllib.request.urlopen(url) as url_data:
        with open(f"./Day{day}_test.pdf", "wb") as pdf:
            pdf.write(url_data.read())
            time.sleep(0.5)
