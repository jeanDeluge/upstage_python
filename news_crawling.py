import time
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from textrankr import TextRank
from typing import List
from konlpy.tag import Okt

# driver 설정
from selenium import webdriver 
from selenium.webdriver.common.by import By

# chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

      
class NewsCrawling:
    def __init__(self):
        self.mytokenizer: OktTokenizer=OktTokenizer()
        self.textrank: TextRank = TextRank(self.mytokenizer)
        self.n_text=3
        self.url='https://news.naver.com/section/105'
        self.drive=None
        self.df = pd.DataFrame(columns=['title','company','url','summarize_content','content','ai_summary'])
        self.news_list=[]

    def __enter__(self):
        print('start')
        self.get_news()
        self.news_crawling()
        self.news_summary()
        self.save()

    def __exit__(self, type, value, trackback):
        pass

    def get_news(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        time.sleep(0.3)
    
        self.driver.find_element(By.XPATH,'//*[@id="newsct"]/div[1]/div[2]/a').click()
        time.sleep(0.3)

        # 뉴스 기사가 몇개 잇는지
        self.news_list=self.driver.find_elements(By.CLASS_NAME,'sa_item._SECTION_HEADLINE')

    def news_crawling(self):
        self.title_list=[]
        self.company_list=[]
        self.summarize_content_list=[]
        self.url_list=[]

        for news in self.news_list:
            title = news.find_element(By.CLASS_NAME, 'sa_text_strong').text #뉴스제목
            company = news.find_element(By.CLASS_NAME, 'sa_text_press').text #언론사
            summarize_content = news.find_element(By.CLASS_NAME, 'sa_text_lede').text #내용
            url = news.find_element(By.CLASS_NAME, 'sa_text_title').get_attribute('href') #작성일

            self.title_list.append(title)
            self.company_list.append(company)
            self.summarize_content_list.append(summarize_content)
            self.url_list.append(url)

    def news_summary(self):
        self.content_list=[]
        self.ai_summary_content_list=[]

        for url in self.url_list:
            self.driver.get(url)
            content=self.driver.find_element(By.CLASS_NAME, 'go_trans._article_content').text #내용
            # print(content)
            ai_summary: str = self.textrank.summarize(content,self.n_text)
            # print(ai_summary) 
            
            time.sleep(1)
            self.content_list.append(content)
            self.ai_summary_content_list.append(ai_summary)

    def save(self):
        self.df['title']=self.title_list
        self.df['company']=self.company_list
        self.df['url']=self.url_list
        self.df['summarize_content']=self.summarize_content_list
        self.df['content']=self.content_list
        self.df['ai_summary']=self.ai_summary_content_list
        
        # dataframe를 csv로 저장
        self.df.to_csv("output/news.csv", encoding='utf-8-sig',index=False)
                

# 리스트 형식으로 저장하기 위한 클래스 선언
class ListTokenizer:
    def __call__(self,text:str)->List[str]:
        tokens: List[str]=text.split()
        return tokens

# okt를 사용한 MyTokenizer
class OktTokenizer:
    okt: Okt = Okt()
    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = self.okt.phrases(text)
        return tokens 

