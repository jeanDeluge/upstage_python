from wordcloud import WordCloud
from konlpy.tag import Okt
import pandas as pd
import numpy as np
from collections import Counter


class MakeWordCloud:
    def __init__(self):
        self.okt=Okt()
        self.stop_words=""
        self.df=pd.read_csv('output/news.csv',encoding='utf-8-sig') # load crawling news to dataframe 

    def __enter__(self):
        self.stopword()
        self.wordcloud()

    def __exit__(self, type, value, trackback):
        pass

    def wordcloud(self):
        # making wordcloud image
        news_words=self.tokenizer()
        counts = Counter(news_words)
        wc = WordCloud(random_state = 123, font_path = 'rss/Typo_SsangmunDongB.ttf', width = 400,
               height = 400, background_color = 'white')
        wc.generate_from_frequencies(counts)
        wc.to_file('output/wordcloud_new.png')

    def stopword(self):
        # Define stopwords
        self.stop_words="사 또 의 과 개 회 옆 이번 익스 기반 등 수 및 것 통해 를 고 더 위해 한스 이 각종 용 센터 코 며 언스 비롯 은 위 가장 강조 부사 부문 결과 제시 최근 라며 총 대응 현안 시 비 해 산 민 때 새 애 에 학"
        self.stop_words=set(self.stop_words.split(' '))
    
    def tokenizer(self):
        # Using okt, tokenizing the news words
        self.df['content_token'] = self.df['content'].apply(lambda x: ','.join([word for word, pos in self.okt.pos(x) if pos in ['Noun'] and not word in self.stop_words])) #'Adjective','Verb'
        self.news_words=np.concatenate(self.df['content_token'].str.split(',').apply(np.array).tolist())
        return self.news_words
    


