import time
import pandas as pd
import schedule

import warnings
warnings.filterwarnings('ignore')

from textrankr import TextRank
from typing import List

# driver 설정
from selenium import webdriver 
from selenium.webdriver.common.by import By
        
# chrome driver
driver = webdriver.Chrome()

def crawling_news():
    
    # 리스트 형식으로 저장하기 위한 클래스 선언
    class MyTokenizer:
        def __call__(self,text:str)->List[str]:
            tokens: List[str]=text.split()
            return tokens
    # 리스트 형식으로 저장하는 공간만들고 그 공간에 데이터 요약
    mytokenizer: MyTokenizer=MyTokenizer()
    textrank: TextRank = TextRank(mytokenizer)
    k=3 # 요약 데이터 3줄까지 설정
    
    
    url='https://news.naver.com/section/105'
    driver.get(url)
    time.sleep(0.3)
    
    driver.find_element(By.XPATH,'//*[@id="newsct"]/div[1]/div[2]/a').click()
    time.sleep(0.3)
    
    # 뉴스 기사가 몇개 잇는지
    news_list=driver.find_elements(By.CLASS_NAME,'sa_item._SECTION_HEADLINE')

    # csv저장을 위한 dataframe 생성
    df = pd.DataFrame(columns=['title','company','url','summarize_content','content','ai_summary'])

    title_list=[]
    company_list=[]
    summarize_content_list=[]
    url_list=[]
    content_list=[]
    ai_summary_content_list=[]

    for news in news_list:
        print('-----------')
        title = news.find_element(By.CLASS_NAME, 'sa_text_strong').text #뉴스제목
        company = news.find_element(By.CLASS_NAME, 'sa_text_press').text #언론사
        summarize_content = news.find_element(By.CLASS_NAME, 'sa_text_lede').text #내용
        url = news.find_element(By.CLASS_NAME, 'sa_text_title').get_attribute('href') #작성일

        title_list.append(title)
        company_list.append(company)
        summarize_content_list.append(summarize_content)
        url_list.append(url)

    for url in url_list:
        driver.get(url)
        content=driver.find_element(By.CLASS_NAME, 'go_trans._article_content').text #내용
        print(content)
        ai_summary: str = textrank.summarize(content,k)
        print(ai_summary) 
        
        time.sleep(1)
        content_list.append(content)
        ai_summary_content_list.append(ai_summary)
    
    df['title']=title_list
    df['company']=company_list
    df['url']=url_list
    df['summarize_content']=summarize_content_list
    df['content']=content_list
    df['ai_summary']=ai_summary_content_list
    
    # dataframe를 csv로 저장
    df.to_csv("output/news.csv", encoding='utf-8-sig',index=False)



### 스케쥴 매일 아침 9:30 에 크롤링 시작 
# schedule.every().day.at("09:30").do(crawling_news)
schedule.every(14).seconds.do(crawling_news)
while True:
    schedule.run_pending()
    time.sleep(1)    