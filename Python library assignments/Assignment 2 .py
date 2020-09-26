# Assignment 2 - Pandas Introduction
All questions are weighted the same in this assignment.
## Part 1
The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 

The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()

### Question 0 (Example)

What is the first country in df?

*This function should return a Series.*

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 

### Question 1
Which country has won the most gold medals in summer games?

*This function should return a single string value.*

def answer_one():
    a=max(df["Gold"])
    ans=df[df["Gold"]==a].index.tolist()
    return ans[0]

answer_one()

### Question 2
Which country had the biggest difference between their summer and winter gold medal counts?

*This function should return a single string value.*

def answer_two():
    a=max(df["Gold"]-df["Gold.1"])
    ans=df[df["Gold"]-df["Gold.1"]==a].index.tolist()
    return ans[0]
answer_two()

### Question 3
Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 

$$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$

Only include countries that have won at least 1 gold in both summer and winter.

*This function should return a single string value.*

def answer_three():
    a=df[df["Gold"]>0]
    b=df[df["Gold.1"]>0]
    c=df["Gold.2"]
    a=a["Gold"]
    b=b["Gold.1"]
    d=(a-b)/c
    ans=d[(a-b)/c==d.max()].index.tolist()
    return ans[0]
answer_three()

### Question 4
Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.

*This function should return a Series named `Points` of length 146*

def answer_four():
    a=df["Gold.2"]*3
    b=df["Silver.2"]*2
    c=df["Bronze.2"]
    c=a+b+c
    return c
answer_four()

## Part 2
For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf) for a description of the variable names.

The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.

### Question 5
Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)

*This function should return a single string value.*

census_df = pd.read_csv('census.csv')
census_df.head()

def answer_five():
    b=census_df.STNAME.map(census_df.STNAME.value_counts())
    c=census_df[census_df.CTYNAME.map(census_df.STNAME.value_counts())==b.max()]
    g=c["STNAME"].tolist()
    return g[0]
answer_five()

### Question 6
**Only looking at the three most populous counties for each state**, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.

*This function should return a list of string values.*

def answer_six():
    coun=census_df[census_df["SUMLEV"]==50]
    a=coun["CENSUS2010POP"].max()
    b=coun[coun["CENSUS2010POP"]==a]
    ans1=b["STNAME"].tolist()
    c=coun[coun["CENSUS2010POP"]!=a]
    d=c["CENSUS2010POP"].max()
    e=c[c["CENSUS2010POP"]==d]
    ans2=e["STNAME"].tolist()
    f=c[c["CENSUS2010POP"]!=d]
    g=f["CENSUS2010POP"].max()
    h=f[f["CENSUS2010POP"]==g]
    ans3=h["STNAME"].tolist()
    ans=ans1+ans3+ans2
    return ans
answer_six()

### Question 7
Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)

e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.

*This function should return a single string value.*

def answer_seven():
    coun=census_df[census_df["SUMLEV"]==50]
    a=coun["POPESTIMATE2010"]
    b=coun["POPESTIMATE2011"]
    c=coun["POPESTIMATE2012"]
    d=coun["POPESTIMATE2013"]
    e=coun["POPESTIMATE2014"]
    f=coun["POPESTIMATE2015"]
    ad=pd.DataFrame({"1":a,
                    "2":b,
                    "3":c,
                    "4":d,
                    "5":e,
                    "6":f})
    x=ad.T
    k=x[:].max()-x[:].min()
    y=k[x[:].max()-x[:].min()==k.max()].index
    ks=coun.loc[y,"CTYNAME"].tolist()
    return ks[0]
answer_seven()

### Question 8
In this datafile, the United States is broken up into four regions using the "REGION" column. 

Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.

*This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

def answer_eight():
    a=census_df[census_df["REGION"]<3]
    b=a[a["CTYNAME"]=="Washington County"]
    c=b[b["POPESTIMATE2015"]>b["POPESTIMATE2014"]]
    return c[['STNAME','CTYNAME']]
    
answer_eight()


