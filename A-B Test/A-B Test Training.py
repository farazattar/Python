#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


# In[3]:


df = pd.read_csv('bank.csv', sep=";")
df.head()


# In[20]:


df.describe()


# In[21]:


df.info()


# In[10]:


df.query('loan == "yes"')


# In[11]:


df.query('loan == "no"')


# In[14]:


df.query('loan == "yes" and y=="yes"')


# In[15]:


len(df.query('loan == "yes" and y=="yes"'))


# In[16]:


df.query('loan == "no" and y=="yes"')


# In[17]:


len(df.query('loan == "no" and y=="yes"'))


# In[18]:


len(df.query('loan == "yes" and y=="no"'))


# In[19]:


len(df.query('loan == "no" and y=="no"'))


# In[22]:


a = len(df.query('loan == "yes" and y=="yes"'))
b = len(df.query('loan == "no" and y=="yes"'))
c = len(df.query('loan == "yes" and y=="no"'))
d = len(df.query('loan == "no" and y=="no"'))
a+b+c+d


# In[23]:


len(df["loan"])


# In[82]:


loan_and_y = a/(a+c)*100
noloan_and_y = b/(b+d)*100
loan_and_n = c/(a+c)*100
noloan_and_n = d/(b+d)*100


# In[83]:


loan_and_y


# In[84]:


noloan_and_y


# In[85]:


loan_and_n


# In[86]:


noloan_and_n


# In[88]:


new_loan_and_y = np.random.choice([1, 0], size = (a+c), p=[(loan_and_y/100), (1 - (loan_and_y/100))])


# In[89]:


new_loan_and_y


# In[90]:


plt.hist(new_loan_and_y)


# In[91]:


new_noloan_and_y = np.random.choice([1,0], size= (b+d), p = [(noloan_and_y/100), (1 - (noloan_and_y/100))])


# In[92]:


new_noloan_and_y


# In[93]:


plt.hist(new_noloan_and_y)


# In[94]:


new2_loan_and_y = np.random.binomial((a+c), loan_and_y/100, 10000) / (a+c)


# In[95]:


new2_noloan_and_y = np.random.binomial((b+d), noloan_and_y/100, 10000) / (b+d)


# In[96]:


new2_loan_and_y


# In[97]:


new2_noloan_and_y


# In[98]:


len(new2_loan_and_y)


# In[99]:


len(new2_noloan_and_y)


# In[100]:


p_diffs = new2_loan_and_y - new2_noloan_and_y


# In[101]:


p_diffs


# In[102]:


p_diffs.mean()


# In[103]:


ab_data_diff = (loan_and_y - noloan_and_y) / 100 


# In[104]:


ab_data_diff


# In[105]:


(p_diffs > ab_data_diff).mean() * 100


# In[106]:


(p_diffs < ab_data_diff).mean() * 100


# In[107]:


plt.hist(p_diffs, bins=100)
low = ab_data_diff
high = p_diffs.mean()
plt.axvline(x=low, color='g')
plt.axvline(x=high, color='r')


# In[108]:


import statsmodels.api as sm


# In[109]:


sm.stats.proportions_ztest([b, a], [(b+d), (a+c)], alternative='larger')


# In[ ]:




