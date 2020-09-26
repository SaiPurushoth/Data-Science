# Assignment 2

Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.

An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.

Each row in the assignment datafile corresponds to a single observation.

The following variables are provided to you:

* **id** : station identification code
* **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
* **element** : indicator of element type
    * TMAX : Maximum temperature (tenths of degrees C)
    * TMIN : Minimum temperature (tenths of degrees C)
* **value** : data value for element (tenths of degrees C)

For this assignment, you must:

1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.

The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.



import matplotlib.pyplot as plt
import numpy as np
import mplleaflet
import pandas as pd
import matplotlib.dates as mdates

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')



%matplotlib notebook
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df=df.drop('ID',axis=1)
df['Data_Value']=df['Data_Value']*0.1
df['Date']=pd.to_datetime(df['Date']).dt.strftime('%m-%d')
df['Date']='2015-'+df['Date']
df=df.set_index('Date')
df=df.groupby(level=0)['Data_Value'].agg({'minc':np.min,'maxc':np.max})
df=df.drop('2015-02-29')

df2= pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df2=df2.drop('ID',axis=1)
df2['Data_Value']=df2['Data_Value']*0.1
df2['Date']=pd.to_datetime(df2['Date'])
df2=df2[df2['Date'].dt.year!=2015]
df2['Date']=pd.to_datetime(df2['Date']).dt.strftime('%m-%d')
df2['Date']='2015-'+df2['Date']
df2=df2.set_index('Date')
df2=df2.groupby(level=0)['Data_Value'].agg({'minc':np.min,'maxc':np.max})
df2=df2.drop('2015-02-29')


df1= pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df1=df1.drop('ID',axis=1)
df1['Date']=pd.to_datetime(df1['Date'])
df1['Data_Value']=df1['Data_Value']*0.1
df1=df1[df1['Date'].dt.year==2015]
df1=df1.groupby('Date')['Data_Value'].agg({'maxl':np.max,"minl":np.min})
k=df1[df['minc']-df1['minl']==0]
l=df1[df['maxc']-df1['maxl']==0]
k=k["minl"]
l=l["maxl"]




df2.index=pd.to_datetime(df2.index)
days=df2.index
ax=plt.gca().xaxis
plt.plot(days,df2['maxc'],label="Record high(2005-2014)")
plt.plot(days,df2['minc'],label="Record low (2005-2014)")
plt.scatter(k.index,k,s=25,c='g',label="Record breaking low in 2015")
plt.scatter(l.index,l,s=25,c='r',label="Record breaking high in 2015")
fmt=mdates.DateFormatter('%b')
locator=mdates.MonthLocator()
ax.set_major_locator(locator)
ax.set_major_formatter(fmt)
plt.gca().fill_between(days, 
                       df2['maxc'],df2['minc'], 
                       facecolor='blue', 
                       alpha=0.25)
ax1=plt.gca()
ax1.set_xlabel('MONTHS')
ax1.set_ylabel('TEMPERATURE IN CELSIUS')
ax1.set_title('TEMPERATURE IN Ann Arbor, Michigan, United States OVER THE YEARS OF 2005-2014')
plt.legend(loc=4, frameon=False, title='Legend')
fig=plt.gcf()
fig.set_size_inches(14,8)
plt.savefig('temperature.png')
plt.show()


