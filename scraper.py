
# coding: utf-8

# In[17]:

import time
import requests
from BeautifulSoup import BeautifulSoup
import numpy as np
import pandas as pd
from __future__ import division


# In[2]:

def getSessionRequest(email, password):
    session_requests = requests.session()
    login_url = 'https://www.alexa.com/secure/login'
    credentials = {'email': email, 'password': password}
    logged_in = session_requests.post(login_url, data=credentials)
    return session_requests


# In[3]:

def getTableFromDomain(domain, session_requests):
    BASE_URL = 'http://www.alexa.com/siteinfo/'
    url = BASE_URL + domain
    response = session_requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    table = soup.find('div', attrs={'id': 'demographics-content'})
    return table


# In[4]:

def getPercentageFromTags(tag):
    words = tag.split()
    percentage = []
    for word in words:
        if "width" in word:
            percentage.append(word)
    return percentage


# In[5]:

def getPercentageFromTable(table):
    tag_gender_age_children = table.findAll("span")[0].prettify()
    tag_education_income = table.findAll("span")[148].prettify()
    tag_browsing_ethnicity = table.findAll("span")[263].prettify()
    gender_age_children_percentage = getPercentageFromTags(tag_gender_age_children)
    education_income_percentage = getPercentageFromTags(tag_education_income)
    browsing_ethnicity_percentage = getPercentageFromTags(tag_browsing_ethnicity)
    return gender_age_children_percentage, education_income_percentage, browsing_ethnicity_percentage


# In[6]:

def convertTextIntoInt(percentage):
    final_percentage = []
    for percent in percentage:
        final_percentage.append(percent[(percent.index(":")+1):percent.index("%")])
    final_percentage = map(int, final_percentage)
    return final_percentage


# In[7]:

def getRealDemoFromPercentage(gender_age_children_percentage, education_income_percentage, browsing_ethnicity_percentage):
    final_gender_age_children= convertTextIntoInt(gender_age_children_percentage)
    final_education_percentage= convertTextIntoInt(education_income_percentage)
    final_browsing_ethnicity= convertTextIntoInt(browsing_ethnicity_percentage)
    final_percentage = final_gender_age_children + final_education_percentage + final_browsing_ethnicity
    real_demo = [0]*28
    i = 0
    count = 0
    while i < 28:
        real_demo[i] = (final_percentage[count]+final_percentage[count+1])/200
        i = i + 1
        count = count + 2
    return real_demo


# In[11]:

def makeDfFromRealDemo(domain_name, real_demo):
    dict = {domain_name:real_demo}
    df=pd.DataFrame.from_dict(dict, orient='index', dtype=None)
    return df


# In[13]:

customer1["domain"][0:30]


# In[18]:

customer1 = pd.read_csv('domain_count.txt', sep='\t',header = None, names=["domain", "count"])
final_df = pd.DataFrame()
session_request = getSessionRequest('haha', 'hehe')
count=0
for single_domain in customer1["domain"][0:30]:
    table = getTableFromDomain(single_domain, session_request)
    triple_element = getPercentageFromTable(table)
    e_1 = triple_element[0]
    e_2 = triple_element[1]
    e_3 = triple_element[2]
    real_demo = getRealDemoFromPercentage(e_1, e_2, e_3)
    df = makeDfFromRealDemo(single_domain, real_demo)
    final_df=final_df.append(df)
    count+=1
    time.sleep(1)
    print count


# In[19]:

final_df


# In[20]:

final_df.columns = ["male", "female", "18-24", "25-34", "35-44", "45-54", "55-64", "65+", "Has Children", "No Children", 
"No_college", "Some_college", "Graduate_School", "College", "$0 - $30K", "$30K - $60K", "$60K - $100K", "$100K+", "Home", "School",
"Work", "African", "African American", "Asian", "Caucasian", "Hispanic", "Middle Eastern", "Other"]
final_df["Count"] = customer1["count"][0:30].values



# In[21]:

pd.set_option('display.max_columns', 29)
final_df


# In[ ]:




# In[ ]:



