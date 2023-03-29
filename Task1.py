#!/usr/bin/env python
# coding: utf-8

# ### Step 0
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.

# In[24]:


pip install xlrd


# In[25]:


import pandas as pd
import numpy as np


energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38)


energy = energy.drop(energy.columns[0:2], axis=1)


energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']


energy['Energy Supply'] *= 1000000


energy.replace('...', np.NaN, inplace=True)


energy['Country'].replace({"Republic of Korea": "South Korea",
                           "United States of America": "United States",
                           "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                           "China, Hong Kong Special Administrative Region": "Hong Kong"}, inplace=True)

# Remove numbers and/or parenthesis from the country names
energy['Country'] = energy['Country'].str.replace(r" \(.*\)","",regex=True)
energy['Country'] = energy['Country'].str.replace(r"([0-9]+)$","",regex=True)


print(energy)


# In[26]:


pip install pandas


# ### Step 1
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>

# In[27]:


import pandas as pd

GDP = pd.read_csv("world_bank.csv", skiprows=4)


GDP = GDP.rename(index={"Korea, Rep.": "South Korea", 
                       "Iran, Islamic Rep.": "Iran",
                       "Hong Kong SAR, China": "Hong Kong"})


print(GDP.head())


# ### Step 2
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.

# In[28]:


pip install openpyxl


# In[29]:


import pandas as pd

ScimEn = pd.read_excel("scimagojr-3.xlsx")
print (ScimEn)


# ### Step 3
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This step should yeild a DataFrame with 20 columns and 15 entries.*

# In[30]:


GDP.rename(columns={"Country Name": "Country"}, inplace=True)

print(GDP)
 
 


# In[31]:





GDP = GDP[['Country','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]


ScimEn = ScimEn[ScimEn['Rank'] <= 15]


df = pd.merge(GDP, energy, on='Country')
merged_df = pd.merge(df, ScimEn, on='Country')


merged_df.set_index('Country', inplace=True)


merged_df = merged_df[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
merged_df


# ### Step 4
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This step should yield a single number.*

# In[32]:




total_scimen = ScimEn.size


total_merged = merged_df.size


entries_lost = total_merged - total_scimen

print(entries_lost)



# ### Step 5
# 
# #### Answer the following questions in the context of only the top 15 countries by Scimagojr Rank 
# 
# 
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This step should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[33]:



avgGDP = merged_df[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].mean(axis=1).sort_values(ascending=False)

print(avgGDP)


# ### Step  6
# What is the mean `Energy Supply per Capita`?
# 
# *This step should return a single number.*

# In[34]:


avg = merged_df ['Energy Supply per Capita'].mean()
avg


# ### Step 7
# What country has the maximum % Renewable and what is the percentage?
# 
# *This step should return a tuple with the name of the country and the percentage.*

# In[35]:


max_renewable = merged_df['% Renewable'].idxmax()
max_renewable_percent = merged_df.loc[max_renewable]['% Renewable']
result = (max_renewable, max_renewable_percent)
result


# ### Step 8
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This step should return a tuple with the name of the country and the ratio.*

# In[36]:



merged_df['Citation Ratio'] = merged_df['Self-citations'] / merged_df['Citations']


max_ratio = merged_df['Citation Ratio'].idxmax()
max_ratio_value = merged_df.loc[max_ratio, 'Citation Ratio']

result = (max_ratio, max_ratio_value)
print(result)


# ### Step 9
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This step should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*







median_renewable = merged_df['% Renewable'].median()


merged_df['HighRenew'] = (merged_df['% Renewable'] >= median_renewable).astype(int)


result = merged_df.sort_values(by='Rank')['HighRenew']
merged_df


# ### Step 10
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[46]:


import pandas as pd
import numpy as np
df = pd.DataFrame({'Country': ['China', 'United States', 'Japan', 'United Kingdom', 'Russian Federation', 'Canada', 'Germany', 'India', 'France', 'South Korea', 'Italy', 'Spain', 'Iran', 'Australia', 'Brazil']})
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

df['Continent'] = df['Country'].map(ContinentDict)
df['popu']=energy['Energy Supply']/energy['Energy Supply per Capita']
result = df.groupby('Continent')['popu'].agg(size=np.size, total=np.sum, average=np.mean, deviation=np.std)
result







