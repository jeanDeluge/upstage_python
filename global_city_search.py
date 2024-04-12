import time
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

# driver 설정
from selenium import webdriver 
from selenium.webdriver.common.by import By
        
# chrome driver
driver = webdriver.Chrome()

url='https://m.naver.com/'
driver.get(url)
time.sleep(1)

# 세계 도시 목록 
global_citys=['뉴욕','런던','파리','도쿄','베이징','홍콩','로스앤젤레스','시카고','싱가포르','워싱턴 D.C.']

# 사용자 응답 받아오기 (구현미완)
user_answers=[]

# 사용자의 응답 중 검색원하는 도시 추출
citys=[]
for user_answer in user_answers:
    if user_answer in global_citys:
        citys.append(user_answer)

# 일단은 첫번째 도시만 검색하게 구현 (구현미완)
# city=citys[0]
city='뉴욕'

# 사용자가 무엇을 원하는지? 1) 날씨 2) 현지시각 3)뉴스
selection=['날씨','현지시각']

driver.find_element(By.XPATH,'//*[@id="MM_SEARCH_FAKE"]').click()
driver.find_element(By.XPATH,'//*[@id="query"]').send_keys(f'{city} 날씨')
driver.find_element(By.XPATH,'//*[@id="sch_w"]/div/form/button').click()
time.sleep(1)

# 글로벌 도시 날씨
if '날씨' in selection:
    
    # csv저장을 위한 dataframe 생성
    df = pd.DataFrame(columns=['city','temperature','sky','feel_temperature']) 
    
    weather = driver.find_element(By.XPATH,'//*[@id="ct"]/section[1]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div[2]').text
    weather=weather.split('\n') 
    temperature=" ".join(weather[0:2])
    sky=weather[2]
    feel_temperature=weather[3]
    
    print(temperature, sky, feel_temperature)
    df.loc[0] = [city,temperature, sky, feel_temperature]
    
    # dataframe를 csv로 저장
    df.to_csv("output/city_weather.csv", encoding='utf-8-sig',index=False) # dataframe을 csv로

# 글로벌 도시 현지시각    
if '현지시각' in selection:
    
    # csv저장을 위한 dataframe 생성
    df = pd.DataFrame(columns=['city','city_time']) 
    
    city_time=driver.find_element(By.XPATH,'//*[@id="ct"]/section[1]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/dl[1]/dd[1]').text
    print(city_time)
    
    df.loc[0] = [city,city_time]

    # dataframe를 csv로 저장
    df.to_csv("output/city_time.csv", encoding='utf-8-sig',index=False) # dataframe을 csv로

# 글로벌 뉴스 (구현 미완)
if '뉴스' in selection :
  # csv 만들고 보내는 코드 추후 구현
  pass