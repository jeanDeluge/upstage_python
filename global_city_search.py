import time
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

# driver 설정
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
        
class GetGlobalCity:
  def __init__(self, city, command):
    self.city = city
    self.selection = command
    self.result = {}
    self.url='https://m.naver.com/'
    self.driver=None

  def __enter__(self):
    self.result= self.select_function()
    return self.result

  def __exit__(self, type, value, trackback):
    pass
  
  def select_function(self):
    self.result=self.get_news()
    if self.result==0:
      self.get_city()
      if '날씨' in self.selection:
        self.result=self.get_weather()
      if '현지시각' in self.selection:
        self.result=self.get_time()
      self.driver.quit()
    return self.result 
        
  def get_news(self):
    if '뉴스' in self.selection :
      if '요약' in self.selection :
        # 뉴스 상단 3개 요약(text) & wordcloud(img)
        df=pd.read_csv('output/news.csv')
        df='\n\n---------------------------------\n\n'.join(df.ai_summary[0:3].to_list())
        return {'text':df,'command_type':'news_summary'}
      # 뉴스 csv 파일로 보내기
      return {'command_type':'only_news'}
    return 0  

  def get_city(self):
    self.driver = webdriver.Chrome(options=chrome_options)
    self.driver.get(self.url)
    self.driver.implicitly_wait(time_to_wait=3)

    self.driver.find_element(By.XPATH,'//*[@id="MM_SEARCH_FAKE"]').click()
    self.driver.find_element(By.XPATH,'//*[@id="query"]').send_keys(f'{self.city} 날씨')
    self.driver.find_element(By.XPATH,'//*[@id="sch_w"]/div/form/button').click()
    time.sleep(1)

  def get_weather(self):
    weather = self.driver.find_element(By.XPATH,'//*[@id="ct"]/section[1]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div[2]').text
    weather=weather.split('\n') 
    temperature=" ".join(weather[0:2])
    sky=weather[2]
    feel_temperature=weather[3]
    
    return {'text':f"{self.city}의 기온은 {temperature}이며 하늘은 {sky}입니다. {feel_temperature}입니다."}

  def get_time(self):
    city_time=self.driver.find_element(By.XPATH,'//*[@id="ct"]/section[1]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/dl[1]/dd[1]').text
    
    return {'text': f"{self.city}의 현지 시각은 {city_time}입니다."}
    
with GetGlobalCity(["뉴욕"],["날씨"]) as globals:
  print(globals)
