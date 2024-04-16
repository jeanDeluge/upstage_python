import time
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

# driver 설정
from selenium import webdriver 
from selenium.webdriver.common.by import By
        
async def get_global_city(city, command): #"뉴욕"
  # chrome driver
  
  selection=command
  print(command)
  
  if '뉴스' in selection :
    
    if '요약' in selection :
      # 뉴스 상단 3개 요약(text) & wordcloud(img)
      df=pd.read_csv('output/news.csv')
      df='\n\n---------------------------------\n\n'.join(df.ai_summary[0:3].to_list())
      return {'text':df,'command_type':'news_summary'}
    
    # 뉴스 csv 파일로 보내기
    return {'command_type':'only_news'}

  driver = webdriver.Chrome()

  url='https://m.naver.com/'
  driver.get(url)
  time.sleep(1)

  # # 세계 도시 목록 
  # global_citys=['뉴욕','런던','파리','도쿄','베이징','홍콩','로스앤젤레스','시카고','싱가포르','워싱턴 D.C.']

  # # 사용자 응답 받아오기 (구현미완)
  # user_answers=[]

  # # 사용자의 응답 중 검색원하는 도시 추출
  # citys=[]
  # for user_answer in user_answers:
  #     if user_answer in global_citys:
  #         citys.append(user_answer)

  # 일단은 첫번째 도시만 검색하게 구현 (구현미완)

  # 사용자가 무엇을 원하는지? 1) 날씨 2) 현지시각 3)뉴스


  driver.find_element(By.XPATH,'//*[@id="MM_SEARCH_FAKE"]').click()
  driver.find_element(By.XPATH,'//*[@id="query"]').send_keys(f'{city} 날씨')
  driver.find_element(By.XPATH,'//*[@id="sch_w"]/div/form/button').click()
  time.sleep(1)
  
  result={}

  # 글로벌 도시 날씨
  if '날씨' in selection:
      
      # csv저장을 위한 dataframe 생성
      # df = pd.DataFrame(columns=['city','temperature','sky','feel_temperature']) 
      
      weather = driver.find_element(By.XPATH,'//*[@id="ct"]/section[1]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div[2]').text
      weather=weather.split('\n') 
      temperature=" ".join(weather[0:2])
      sky=weather[2]
      feel_temperature=weather[3]
      
      # print(temperature, sky, feel_temperature)
      # df.loc[0] = [city,temperature, sky, feel_temperature]
      return {'text':f"{city}의 기온은 {temperature}이며 하늘은 {sky}입니다. 체감온도는 {feel_temperature}입니다"}
      # dataframe를 csv로 저장
      # df.to_csv("output/city_weather.csv", encoding='utf-8-sig',index=False) # dataframe을 csv로

  # 글로벌 도시 현지시각    
  if '현지시각' in selection:
      
    # csv저장을 위한 dataframe 생성
    # df = pd.DataFrame(columns=['city','city_time']) 
    
    city_time=driver.find_element(By.XPATH,'//*[@id="ct"]/section[1]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/dl[1]/dd[1]').text
    # print(city_time)
    
    # df.loc[0] = [city, city_time]
    return {'text': f"{city}의 현지 시각은 {city_time}입니다"}

    # dataframe를 csv로 저장
    #df.to_csv("output/city_time.csv", encoding='utf-8-sig',index=False) # dataframe을 csv로

  
    