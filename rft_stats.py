#import stuff
import sys
import os
import pandas as pd
import re
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#usage: <prog name> <path> <num pie chart>
args = sys.argv[1:]
path = os.path.dirname(args[0])

if not os.path.exists(path):
        os.makedirs(path)

#set up data
lines = [line.strip() for line in open(args[0])]
date_ptn = '(\d+/\d+/\d+,\s\d+:\d+\s(am|pm))\s-\s(\w+):(.*)'
data  = []
re.DOTALL
top_n = int(args[1])

if len(args) > 2:
    sys.exit('invalid arguments')


for l in lines:
    m = re.search(date_ptn, l)
    if(m):
        date = dt.datetime.strptime(m.group(1),'%d/%m/%Y, %I:%M %p')
        name = m.group(3)
        msg = m.group(4)
        data.append([date, name, msg])
        
df = pd.DataFrame(data,columns = ['date', 'name', 'msg'])
df_memes = df[df['msg'].str.contains("<Media omitted>")]


df_avg_txt = df[~df['msg'].str.contains("<Media omitted>")]
df_avg_txt = (df_avg_txt.groupby('name')['msg']
                            .apply(lambda x: np.mean(x.str.len()))
                            .reset_index(name='mean_msg_len'))


#visualize all

#bar
fig1 = plt.figure(figsize=(15, 10))
s= df.groupby('name').count()
s = s.reset_index().sort_values(by=['msg'], ascending=False)
ax = sns.barplot(x="name", y="msg", data=s)
ax.set_title('All contribution')
#pie
s2 = s[:top_n].copy()
#change labels for 'others'
new_row = pd.DataFrame(data = {
    'name' : ['Others'],
    'date' : s['msg'][top_n:].sum(),
    'msg' : [s['msg'][top_n:].sum()]
})


#combining top n with others
s2 = pd.concat([s2, new_row])
fig2, ax1 = plt.subplots(figsize = (20,15))
s2.plot(kind = 'pie', y = 'msg', labels = s2['name'], ax = ax1, autopct='%.2f')
ax1.set_title('All content')
fig1.savefig(path+'/bar_all.png', bbox_inches = 'tight')
fig2.savefig(path+'/pie_all.png', bbox_inches = 'tight')


#visualize memes/ media content

#bar
fig1 = plt.figure(figsize=(15, 10))
s= df_memes.groupby('name').count()
s = s.reset_index().sort_values(by=['msg'], ascending=False)
ax = sns.barplot(x="name", y="msg", data=s)
ax.set_title('Memes contribution')
#pie
s2 = s[:7].copy()
#change labels for 'others'
new_row = pd.DataFrame(data = {
    'name' : ['Others'],
    'date' : s['msg'][7:].sum(),
    'msg' : [s['msg'][7:].sum()]
})


#combining top n with others
s2 = pd.concat([s2, new_row])
fig2, ax1 = plt.subplots(figsize = (20,15))
s2.plot(kind = 'pie', y = 'msg', labels = s2['name'], ax = ax1, autopct='%.2f')

ax1.set_title('Media content')
fig1.savefig(path+'/bar_media.png', bbox_inches = 'tight')
fig2.savefig(path+'/pie_media.png', bbox_inches = 'tight')

#visualize avg len

#bar
fig1 = plt.figure(figsize=(15, 10))
s = df_avg_txt.reset_index().sort_values(by=['mean_msg_len'], ascending=False)
ax = sns.barplot(x="name", y="mean_msg_len", data=s)
ax.set_title('Average Message length by user')
fig1.savefig(path+'/bar_avg_msg.png', bbox_inches = 'tight')