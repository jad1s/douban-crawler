#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from lxml import etree
import numpy as np
import pandas as pd
import datetime


# In[2]:


def dbspider(url):

    data = requests.get(url).text
    s = etree.HTML(data)

    dburl = '//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[1]/a'
    dburl = s.xpath(dburl+'/@href')
    filmname = '//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[1]/a/em'
    filmname = s.xpath(filmname+'/text()')
    rating = '//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[3]/span[1]'
    rating = s.xpath(rating+'/@class')
    intro = '//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[2]'
    intro = s.xpath(intro+'/text()')
    date = '//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[3]/span[2]'
    date = s.xpath(date+'/text()')
    tags = '//*[@id="content"]/div[2]/div[1]/div[2]/div/div[2]/ul/li[3]/span[3]'
    tags = s.xpath(tags+'/text()')
    
    while not len(dburl) == 15:
        dburl.append('0')
    while not len(filmname) == 15:
        filmname.append('0')    
    while not len(rating) == 15:
        rating.append('0')        
    while not len(intro) == 15:
        intro.append('0')        
    while not len(date) == 15:
        date.append('0')
    while not len(tags) == 15:
        tags.append('0')
    
    return dburl, filmname, rating, intro, date, tags


# In[3]:


dburl_list = []
film_list = []
rate_list = []
intro_list = []
date_list = []
tag_list = []

for a in range(100):
    biourl = 'https://movie.douban.com/people/username/collect?sort=time&amp;start={}&amp;filter=all&amp;mode=grid&amp;tags_sort=count'.format(a*15)
    dburl, filmname, rating, intro, date, tags = dbspider(biourl)
    
    dburl_list.extend(dburl)
    film_list.extend(filmname)
    rate_list.extend(rating)
    intro_list.extend(intro)
    date_list.extend(date)
    tag_list.extend(tags)


# In[4]:


biodf = pd.DataFrame()
biodf['dburl'] = dburl_list
biodf['filmname'] = film_list
biodf['rating'] = rate_list
biodf['intro'] = intro_list
biodf['date'] = date_list
biodf['tags'] = tag_list
# ['dburl','filmname','rating','intro','date','tags']


# In[28]:


df_tags = biodf['tags'].str.split(pat=':', n=1, expand=True)
df_tags_tag = df_tags[1].str.split(n=1, expand=True)
biodf['tag1'] = df_tags_tag[0]
biodf['tag2'] = df_tags_tag[1]

df_rate = biodf['rating'].str.split(pat='g', n=1, expand=True)
df_rate_num = df_rate[1].str.split(pat='-', n=1, expand=True)
biodf['rate_num'] = df_rate_num[0]

df_intro = biodf['intro'].str.split(pat='/', n=10, expand=True)
biodf_split = pd.concat([biodf, df_intro], axis=1).drop(['rating', 'tags'], axis=1)
biodf_split.head()


# In[35]:


now = datetime.datetime.now()
biodf.to_csv(r'/Users/username/Documents/username{}.csv'.format(now.strftime("%Y-%m-%d %H-%M")))


# In[ ]:




