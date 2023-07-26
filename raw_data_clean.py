#Author: Xiaoyun Geng (xiaoyung)
# Python file for cleaning the data scraped through ConcertScrapingTest1.py.

#!/usr/bin/env python
# coding: utf-8

# In[2]:


def cleaning_data():
    import pandas as pd
    df = pd.read_csv('overviewRaw.csv')
    
    to_drop = ['Unnamed: 0']
    df.drop(to_drop, inplace=True, axis=1)
    #df
    
    df_split_vd = df['Venue Details'].str.rsplit(",", expand=True)
    #df_split_vd.head()

    df['Zip'] = df_split_vd[2]
    df['Street'] = df_split_vd[1]
    df['City'] = df_split_vd[3]
    df['State'] = df_split_vd[4]
    df['Venue Name'] = df_split_vd[0]
    #df
    #df.dtypes
    
    df = df.convert_dtypes()
    #df.dtypes
    
    df = df.loc[~df['Zip'].str.contains('[a-zA-Z]')]
    # df
    
    to_drop = ['Venue Details']
    df.drop(to_drop, inplace=True, axis=1)
    # df
    
    to_drop = ['Locations']
    df.drop(to_drop, inplace=True, axis=1)
    # df
    
    
    df_time = df["Date"].str.split("T", n = 1, expand = True) 
    # df_time
    
    
    df['Date'] = df_time[0]
    # df
    
    df['Date'] = pd.to_datetime(df['Date'])
    # df
    
    df_genre = df["Artists Genres"].str.split(",", expand = True)
    # df_genre
    
    df = df[df['State'].str.contains('NY', na=False)]
    # df
    
    
    mask = (df['Zip'].str.len() == 5)
    df = df.loc[mask]
    #df
    
    
    result = pd.DataFrame(df)
    result.to_csv('ConcertDataCleaned.csv', header = True)
    
    return result


# In[ ]:




