import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib notebook
df=pd.read_csv('netflix_titles.csv')
df=df[['title','type','release_year']]
df1=df[df['type']=='TV Show']
df1=df1.reset_index()
df1=df1.drop(['index'],axis=1)
df2=df[df['type']=='Movie']
df2=df2.reset_index()
df2=df2.drop(['index'],axis=1)
df1=df1.groupby('release_year')['type'].agg({'no':np.size})
df2=df2.groupby('release_year')['type'].agg({'no':np.size})
df1=df1[24:]
df2=df2[49:]
df3=pd.read_csv('Movie-Data.csv')
df=df[df['type']=='Movie']
df=df.rename(columns={'title':'Title'})
df3=df3[['Title','Rating']]
df4=df.merge(df3, on='Title')
df4=df4.reset_index()
df0=df4.drop(['index','Title','type'],axis=1)
df4=df0.groupby('release_year').max()
df5=df0.groupby('release_year').min()
df4=df4[6:]
df5=df5[6:]


plt.figure()
plt.subplot(1,2,1)
plt.plot(df1,label='Tv Show')
plt.xticks(df1.index)
plt.plot(df2,label='Movies')
plt.legend()
x = plt.gca().xaxis
for item in x.get_ticklabels():
    item.set_rotation(45)
ax=plt.gca()
ax.set_xlabel('YEARS')
ax.set_ylabel('NO OF CONTENTS')
ax.set_title('MOVIES VS TV SHOWS ON NETFLIX OVER 20 YEARS')
plt.subplots_adjust(bottom=0.25)

plt.subplot(1,2,2)
bars=plt.bar(df4.index,df5['Rating'].values,width=0.8)
plt.xticks(df4.index)
x = plt.gca().xaxis
for item in x.get_ticklabels():
    item.set_rotation(45)
ax=plt.gca()
ax.set_xlabel('YEARS')
ax.set_ylabel('IMDB RATING')
ax.set_title('IMDB RATINGS OF NETFLIX MOVIES FOR LAST 14 YEARS')
plt.subplots_adjust(bottom=0.25)

for bar in bars:
    plt.gca().text(bar.get_x() + bar.get_width()/2, bar.get_height() - 1, str(bar.get_height()), 
                 ha='center', color='w', fontsize=10)
bars=plt.bar(df4.index,df4['Rating'].values,width=0.8,bottom=df5['Rating'].values,color='r',alpha=0.5)
for bar in bars:
    plt.gca().text(bar.get_x() + bar.get_width()/2, bar.get_height() +2, str(bar.get_height()), 
                 ha='center', color='w', fontsize=10)
plt.tick_params(top='off', bottom='on', left='off', right='off', labelleft='off', labelbottom='on')
for spine in plt.gca().spines.values():
    spine.set_visible(False)
fig=plt.gcf()
fig.set_size_inches(16,8)
plt.legend(['min','max'])

plt.savefig('project.png')