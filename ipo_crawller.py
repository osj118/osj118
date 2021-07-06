'''IPO web crawller.py'''
'''IPO공모일정을 불러오는 크롤러'''
from urllib.request import urlopen
from bs4 import BeautifulSoup as bfs

html=urlopen('http://www.ipo38.co.kr/ipo/index.htm?key=6')
bsobj=bfs(html,'html.parser')

# 회사 이름 청약날짜 등을 얻기
contents=[]
for link in bsobj.find_all('td'):
    contents.append(link.text.strip().split())

# 회사 이름, 청약날짜 있는 지점 뽑기
import numpy as np
k=0
keywords=np.array(['대신증권','KB증권','삼성증권','미래에셋증권','NH투자증권','한국투자증권','하나금융투자','현대차증권','한화투자증권','키움증권','하이투자증권','신한금융투자'])
#print(contents[39])
for i in contents:
    i=np.asarray(i)
    if np.isin(keywords,i).any():
        break
    else:
        k=k+1
contents2=contents[k]
k=0;wh=[]
for i in contents2:
   if i=='종목명' or i=='[2][3][4][5][6][7][8][9][10]':
       wh.append(k)
   else:
       k+=1

mat=contents2[wh[0]:wh[1]]
mat.remove('분석')
mat.remove('청약경쟁률')

# 아직 청약공모가 안된 것들 고르기
from datetime import datetime
current_time=datetime.now()
month=str(current_time.month)
if len(month)==1:
    month='0'+month
year_month='.'.join([month])
days=[]
day=current_time.day
for i in range(day,32):
    i1=str(i)
    if len(i1)==1:
        i1='0'+i1
    days.append('.'.join([year_month,i1]))

import re
tmp='_'.join(mat)
start_day=0
for i in days:
    #re.search(i)
    if i in tmp:
        #print(i in tmp,i)
        start_day=i
        break

#if True:
if start_day==days[0]:
    # 테이블 만들기
    for i in range(len(mat)):
        mat[i]=mat[i].replace(',',';')

    mat2 = np.array(mat)
    k=0
    while k < len(mat2):
       if start_day in mat2[k]:
           break
       else:
           k+=1
    mat3=mat2[:(k+4)]
    nrow=mat3.shape[0]
    mat4=mat3.reshape(int(nrow/5),5)
    import pandas as pd # Converting pandas pd to export it in a excel sheet
    df=pd.DataFrame(mat4[6:],columns=mat4[0,:6])
    df.to_csv('ipo_calendar.csv',index=False,encoding='utf-8-sig')

    # Print out
    nrow=mat4.shape[0]
    for i in [0,1,3,4]: #i=1
        print(df.columns[i]+': '+mat4[(nrow-1),i])
