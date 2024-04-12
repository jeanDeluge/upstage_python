from wordcloud import WordCloud

from konlpy.tag import Okt
import pandas as pd
import numpy as np

from collections import Counter

# from PIL import Image
# import matplotlib.pyplot as plt

okt = Okt()
stop_words="또 의 과 개 회 옆 이번 익스 기반 등 수 및 것 통해 를 고 더 위해 한스 이 각종 용 센터 코 며 언스 비롯 은 위 가장 강조 부사 부문 결과 제시 최근 라며 총 대응 현안 시 비 해 산 민 때 새 애 에 학"
stop_words=set(stop_words.split(' '))

df=pd.read_csv('output/news.csv',encoding='utf-8-sig')
df['content_token'] = df['content'].apply(lambda x: ','.join([word for word, pos in okt.pos(x) if pos in ['Noun'] and not word in stop_words])) #'Adjective','Verb'

news_words=np.concatenate(df['content_token'].str.split(',').apply(np.array).tolist())
print(news_words)

counts = Counter(news_words)
# print(counts)

# cloud image 로 wordcloud 만들고 싶을때
# icon = PIL.Image.open('cloud.png')

# img = PIL.Image.new('RGB', icon.size, (255,255,255))
# img.paste(icon, icon)
# img = np.array(img)

wc = WordCloud(random_state = 123, font_path = 'rss/Typo_SsangmunDongB.ttf', width = 400,
               height = 400, background_color = 'white')

img_wordcloud = wc.generate_from_frequencies(counts)
wc.to_file('output/wordcloud_new.png')