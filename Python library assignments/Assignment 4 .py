import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Assignment 4 - Hypothesis Testing
This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

Definitions:
* A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
* A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
* A _recession bottom_ is the quarter within a recession which had the lowest GDP.
* A _university town_ is a city which has a high percentage of university students compared to the total population of the city.

**Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)

The following data files are available for this assignment:
* From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
* From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
* From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.

Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 
          'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    df = pd.read_fwf('university_towns.txt',names=["RegionName"])
    car=df["RegionName"].str.lower().str.endswith("[edit]").tolist()
    lent=len(car)
    scp=list(df["RegionName"])
    length=len(scp)
    g=0
    i=0
    e=[]
    d=[]
    while g<length and i<lent:
        s=car[i]
        if(s==False):
            d.append(cb)
        if(s==True):
            cb=scp[g]
            d.append(cb)
            e.append(i)
        i=i+1
        g=g+1
        
    df["State"]=d
    df=df.drop(e)
    df=df.reset_index()
    df=df.drop(["index"],axis=1)
    df["RegionName"]=df["RegionName"].str.replace(r"\[.*\]","")
    df["State"]=df["State"].str.replace(r"\[.*\]","")
    df=df[["State","RegionName"]]
    rn=df["RegionName"].str.split("(", n = 1, expand = True)
    df["RegionName"]=rn[0].str.rstrip()
    return df
get_list_of_university_towns()      

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    df=pd.read_excel('gdplev.xls',skiprows=220,header=None)
    df=df[[4,5]].rename(columns={4:"year",5:"GDP"})
    df["dif"]=df["GDP"].diff()
    sc=list(df["dif"])
    l=len(sc)
    i=0
    c=0
    d=0
    while(i<l):
        if(sc[i]<0):
            c=c+1
        if(c>=2):
            val=i-1
            while(i<l):
                if(sc[c]>0):
                    d=d+1
                if(d>=2):
                    k=val
                    break;
                i=i+1
            break
        i=i+1
    k=df.iloc[k].tolist()     
    return k[0]
get_recession_start()

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    df=pd.read_excel('gdplev.xls',skiprows=220,header=None)
    df=df[[4,5]].rename(columns={4:"year",5:"GDP"})
    df["dif"]=df["GDP"].diff()
    sc=list(df["dif"])
    l=len(sc)
    i=0
    c=0
    d=0
    while(i<l):
        if(sc[i]<0):
            c=c+1
        if(c>=2):
            val=i-1
            while(i<l):
                if(sc[c]>0):
                    d=d+3
                if(d>=2):
                    k=i+4
                    break;
                i=i+1
            break
        i=i+1
    k=df.iloc[k].tolist()     
    return k[0]
get_recession_end()

def get_recession_bottom():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    df=pd.read_excel('gdplev.xls',skiprows=220,header=None)
    df=df[[4,5]].rename(columns={4:"year",5:"GDP"})
    df["dif"]=df["GDP"].diff()
    sc=list(df["dif"])
    l=len(sc)
    i=0
    c=0
    d=0
    while(i<l):
        if(sc[i]<0):
            c=c+1
        if(c>=2):
            val=i-1
            while(i<l):
                if(sc[c]>0):
                    d=d+1
                if(d>=2):
                    k=i+1
                    break;
                i=i+1
            break
        i=i+1
    k=df.iloc[k].tolist()     
    return k[0]
get_recession_bottom()

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df=pd.read_csv('City_Zhvi_AllHomes.csv')
    df1=df[["State","RegionName"]]
    df=df[df.columns[51:]] 
    columns=list(df)
    i=0
    j=3
    k=0
    df3=pd.DataFrame()
    while(i<len(columns)):
        if((i+3)%4!=0):
            var=columns[i]
            var=var.split("-")
            d=str(var[0])
            e=str(((i+3)//3)%4)
            var=d+"q"+e
        else:
            var=columns[i]
            var=var.split("-")
            var=var[0]+"q"+"4"

            
    
        df2=df[df.columns[i:j]]
        df1[var]=df2.mean(axis=1)
        i=j
        j=j+3
    df1["State"]=df1.replace({"State":states})
    df1=df1.set_index(["State","RegionName"])
    df1=df1.sort_index()
    
    return df1
convert_housing_data_to_quarters()

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    

    df = convert_housing_data_to_quarters()[['2008q2','2009q2']].dropna()
    df['ratio'] = df['2008q2']/df['2009q2']
    df.drop(['2008q2','2009q2'],axis=1,inplace=True)
    df1 = get_list_of_university_towns()
    df1 = df1.set_index(['State','RegionName'])
    univ = pd.merge(df,df1,how="inner",left_index=True,right_index=True)
    aluniv=df.drop(univ.index)
    p=ttest_ind(univ["ratio"],aluniv["ratio"]).pvalue
    return p
run_ttest()





