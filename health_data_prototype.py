#Author: Zixu Lin (zixulin)
#Python file for fetching COVID-related data in real time

#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
from sodapy import Socrata
import matplotlib.pyplot as plt
def getdataframe():
    client = Socrata("data.cdc.gov", None)
    results = client.get("8396-v7yb", limit=1450000)
    results_df = pd.DataFrame.from_records(results)
    zip_map_county=pd.read_csv("New_York_State_ZIP_Codes-County_FIPS_Cross-Reference.csv")

    zipcode=zip_map_county["ZIP Code"]
    countycode=zip_map_county["County FIPS"]
    map_dict=dict(zip(zipcode, countycode))

    results_df=results_df[results_df["state_name"]=='New York']
    results_df['report_date']=pd.to_datetime(results_df['report_date'],format='%Y-%m-%d')
    results_df=results_df.reset_index()
    results_df=results_df.replace("suppressed", 0)
    return results_df,map_dict

# In[39]:


def getdata(df,zipcode,map_dict):
    fips_code=map_dict[zipcode]
    ans=df[df['fips_code'] == str(fips_code)][-6:-1]
    y1=ans['percent_test_results_reported'].astype(float)
    y2=ans['cases_per_100k_7_day_count'].astype(float)
    x=[x for x in range(1,6)]
    plt.plot(x,y1)
    plt.xlabel('date') 
    plt.ylabel('percent_test_results_reported') 
    plt.show()
    plt.plot(x,y2)
    plt.xlabel('date') 
    plt.ylabel('cases_per_100k_7_day_count') 
    plt.show()
    print(ans.iloc[:,1:])
    return ans.iloc[:,1:]


# In[40]:

# results_df,mapping=getdataframe()
# getdata(results_df,14805,mapping)

