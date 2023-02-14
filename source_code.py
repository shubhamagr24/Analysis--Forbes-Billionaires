#!/usr/bin/env python
# coding: utf-8

# # Analysis -Forbes Billionaires 2021(Feb) 
# 
# It is my first ever data analysis using python, exploring varrious features and functions I have learnt through the course by-Jovian on zerotopandas.I Used Forbes Billionaires 2021(FEB) data and Country wise population Data(2020)** which I downloaded through Kaagle Open Data Sets and then merged both of them and did all the cleaning, type casting , merging and filltering of the releavant data.
# First did a global Macro Review  and then magnified it further to top 200 and top 20 aggregates, groups that has majority of representation on Data being used and a huge impact on whlole of my analysis.
# ### At last I also did a India Specific Analysis for Knowning Billionaires of My country.
# 
# **The population data of 2021 was not avaiable and since there is'nt much change in population figures(1-2%).I have used data for 2020 and it wont distort our main theme of anlyzing Billionaires In The World 2021(Feb).

# # Downloading and Reading of Data

# In[1]:


get_ipython().system('pip install jovian opendatasets --upgrade --quiet')


# In[169]:


jovian.commit()


# Let's begin by downloading the data, and listing the files within the dataset.

# In[2]:


dataset_url = 'https://www.kaggle.com/roysouravcu/forbes-billionaires-of-2021' 


# In[191]:


import opendatasets as od
od.download(dataset_url)


# The dataset has been downloaded and extracted.

# In[3]:



data_dir = './forbes-billionaires-of-2021'


# In[4]:


import os
os.listdir(data_dir)


# In[5]:


project_name = "Billionaires-2021-Analysis" 


# Lets save the file using jovian onto jovian profile

# In[8]:


get_ipython().system('pip install jovian --upgrade -quiet')


# In[9]:


import jovian


# In[10]:


jovian.commit(project=project_name)


# ## Data Preparation and Cleaning
# 
# 
# 
# 

# In[11]:


import pandas as pd
import numpy as np
data_raw=pd.read_csv('./forbes-billionaires-of-2021/Billionaire.csv')


# In[12]:


data_raw


# In[13]:


data_raw.columns


# In[14]:


print(data_raw.info())


# As we see that we hvae NetWorth column which is having datatype object but for our analysis we need to convert it into float type.

# In[15]:


data_raw.NetWorth


# In[20]:


data_raw['NetWorth_Billion_Dollars'] = data_raw['NetWorth'].replace({'\$': '', 'B': ''}, regex=True).astype(float)


# regex = True helps in substacting each string from the series of string passed and perform the instructions given

# Above is a function used to remove character in values and extract numeric data and convert them in float.
# Now we have clean data

# In[22]:


data_raw


# In[24]:


data_raw=data_raw.drop(columns='NetWorth')


# In[25]:


data_raw.info()


# In[26]:


data_raw.describe()


# We see that we some entries where ranks are repeated.
# so we need to investigate and solve the issue.

# In[27]:


data_raw.Rank.value_counts()


# In[21]:


data_raw[data_raw.Rank==2035]


# So we have entries where people have same net worth which means they share common rank.

# We can have a an absolute unique rank for each person

# In[29]:


data_raw['Abs_rank']=data_raw.index+1


# In[30]:


data_raw


# # We can now add population for each country on our billionaries list so as to get more data on demographics of each billionares country

# we are downloading another file with population data of different countires
# Note: The updated data for 2021 is not available so we are taking data for 2020 since there is very negligibe change in population for most of the counties and it wont effect out analysis much.

# In[24]:


import opendatasets as od
od.download('https://www.kaggle.com/tanuprabhu/population-by-country-2020')


# In[31]:


os.listdir('./population-by-country-2020')


# In[32]:


population_data=pd.read_csv('./population-by-country-2020/population_by_country_2020.csv')


# In[33]:


population_data


# In[34]:


population_data.columns


# We need to rename key column to Coutry before merging

# In[35]:


population_data.rename(columns = {'Country (or dependency)':'Country'}, inplace = True)


# In[36]:


population_data


# In[37]:


mergerd_raw=data_raw.merge(population_data,how='left', on='Country')


# In[38]:


mergerd_raw.rename(columns = {'Population (2020)':'Population'}, inplace = True)


# In[39]:


mergerd_raw


# In[40]:


mergerd_raw.info()


# Now we select all the coulms which we need for our analysis

# In[41]:


selected_columns = ['Name','Country','Source','Rank','NetWorth_Billion_Dollars','Abs_rank','Population']


# In[42]:


df=mergerd_raw[selected_columns].copy()


# In[43]:


df


# In[44]:


df.info()


# Having a list of countrywise data

# In[39]:


df


# # Now we have a clean Data For Analysis
# lets save our File and proceed further

# In[40]:


import jovian


# In[45]:


jovian.commit()


# ## Exploratory Analysis and Visualization
# 
# 
# 
# 

# Let's begin by importing`matplotlib.pyplot` and `seaborn`.

# In[77]:


import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'


# In[43]:


df


# In[173]:


print("there are total '{}' Billionaires in The World(FEB-2021)".format(len(df)))


# In[44]:


df.describe()


# ## Exploring Net Worth Vs Ranks(top 200)

# In[45]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(14,7))

plt.plot(df.Rank[:200],df.NetWorth_Billion_Dollars[:200],c='orange',lw=4)

plt.xlabel('Ranks')
plt.ylabel('Net Worth(Billion-$)')
plt.title('Wealth Distrbution')

sns.set_style('whitegrid')


# # We see that there is large change in net worth as we move up the ranks so to confirm it we look at same chart for Top 200 Countries
# 

# # Lets have a look at Frequency of Top 200 Billionaires Across Range of NetWorth

# In[57]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.hist(df.NetWorth_Billion_Dollars[df.Rank<=200],bins=10)
plt.xlabel('Range')
plt.ylabel('Frequency')


plt.title('Frequency of Top 200 Billionaires Acc. to Net Worth');


# ## As expected Count of the Billonaires are highly concentrated at lower range of Net Worth

# ## we see that most of the bilionaires Net Worth lie between 1-50.

# In[58]:


plt.hist(df.Rank,bins=20)
plt.xlabel('Range')
plt.ylabel('Frequency')

plt.title('Frequency of Billionaires Acc to Ranks')


# ## We can see that most billionaires have same Ranks when we move down the ranks.

# # Have a look at all the countries involved

# In[60]:


df['Country'].unique()


# We can identify the countries with the highest number of Billionaires using the value_counts method.

# In[61]:


top_countries_count = df.Country.value_counts()
top_countries_count.head(20)


# In[75]:


count_conc_top_countries=top_countries_count[:20].sum()/top_countries_count[:].sum()
print('Top 20 Country Accounts for {} % of Billionaires out of {} Present in the list.'.format((count_conc_top_countries*100).round(2)
                                                                                               
                                                                                               ,top_countries_count[:].sum()))


# ## Since out of 2755 Billionares only Top 20 Countries  Accounts for ~88.8 .So we can magnify our analysis to Top 20 Countries and rest of the World.

# In[86]:


d1=top_countries_count[:20]
oth=pd.Series([top_countries_count[20:].sum()], index=['Rest of the Countries'])
country_count_oth_inc=d1.append(oth)

plt.figure(figsize=(12,6))
plt.xticks(rotation=75)
plt.title('Where Do Those Riches Live')
sns.barplot(x=country_count_oth_inc.index, y=country_count_oth_inc);


plt.ylabel('Count');
plt.xlabel('Countries');


# ## Above graph tells about Billionaires count amoung Top 20 and rest of the world
# ## We need a another Plot for Comparative Analysis.

# In[84]:



d1=top_countries_count[:7]
oth=pd.Series([top_countries_count[7:].sum()], index=['Rest of the Countries'])
country_count_oth_inc=d1.append(oth)

myexplode = [0.2, 0, 0.4, 0,0,0,0,0]

plt.pie(country_count_oth_inc, labels=country_count_oth_inc.index, autopct='%1.1f%%', startangle=180,pctdistance=.9,explode = myexplode, shadow = True);
plt.title('CountryWise Billionaires Concentration ')


#this increases Size of plot
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(25,12)
fig.savefig('test2png.png', dpi=100)


# In[87]:


top_countries_wealth_contri = df.groupby('Country').NetWorth_Billion_Dollars.sum().sort_values(ascending=False)
top_countries_wealth_contri.head(20)


# In[92]:


d1=top_countries_wealth_contri[:20]
oth=pd.Series([top_countries_wealth_contri[20:].sum()], index=['Rest of the Countries'])
top_countries_wealth_contri_oth_inc=d1.append(oth)

plt.figure(figsize=(12,8))
plt.xticks(rotation=0)
plt.title('How Much Do they Contribute')
sns.barplot(y=top_countries_wealth_contri_oth_inc.index, x=top_countries_wealth_contri_oth_inc);




plt.xticks(top_countries_wealth_contri_oth_inc[:3])

plt.ylabel('Countries');
plt.xlabel('Net Wealth Contribution(B$)');


# In[93]:


jovian.commit()


# In[95]:


top_countries_wealth_mean = df.groupby('Country').NetWorth_Billion_Dollars.mean().sort_values(ascending=False)
top_countries_wealth_mean.head(20)


# In[97]:


d1=top_countries_wealth_mean[:20]
oth=pd.Series([top_countries_wealth_mean[20:].mean()], index=['Rest of the Countries'])
top_countries_wealth_mean_inc_oth=d1.append(oth)



plt.figure(figsize=(10,6))
plt.xticks(rotation=75)
plt.title('CountryWise Mean Net Worth of Billionaires')
sns.barplot(x=top_countries_wealth_mean_inc_oth.index, y=top_countries_wealth_mean_inc_oth,alpha=.5);
plt.plot(top_countries_wealth_mean_inc_oth.index,top_countries_wealth_mean_inc_oth,'o-g',lw=3)

plt.ylabel('Value(B$)');
plt.xlabel('Mean Net Worth');


# ## It shows that on an Average a Billionaire in France is Wealthier than other Billionares in the world

# In[68]:


import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'


# 
# # Questions?
# 

# ## Q1: Which Country Has highest Concentration of  Billionaires.

# ### Lets have a look at Concentration Level of Billionaires in each Country
# ### conc = Billionaires Count / Population

# In[56]:


a=df[df.Population > 10e6].groupby('Country').Name.count()
b=df[df.Population > 10e6].groupby('Country').Population.mean()
z=a*(10e6)/b
z=z.sort_values(ascending=False)


# In[73]:



sns.barplot(x=z[:20], y=z.index[:20]);


# Though U.S tops in Billionaires Count and net Billionaires wealth but It ranks second in Conc wise.Sweden has most Billionaires per million Population.

# In[174]:


df


# #### Q2: Which Catagories have highest Count of Billionaires?

# In[167]:


cata_df=df.groupby('Source')['NetWorth_Billion_Dollars'].agg(["sum", "min", "max",'count','mean'])
cata_df=cata_df.sort_values(by='sum',ascending=False)
cata_df=cata_df[cata_df['count']>5]

''''Here we Considered only catogories which have Billionaires Count more greator than 5, Just neglect billonares
with a single company fortune'''

cata_df


# In[162]:



z=cata_df
plt.figure(figsize=(10,6))
plt.xticks(rotation=75)
sns.barplot(y=z['count'][:20], x=z.index[:20],alpha=.7);
plt.plot(z.index[:20],z['count'][:20]);


# In[103]:


SD_Source_world=z['count'].std(skipna = True)
SD_Source_world


# We can conclude that Real State in the Field where we have most of Our Billionaires. SD for Count of Billionaires for individual Sources = ~9

# In[110]:


jovian.commit()


# #### Q3:Which country has most Billionares in Realestate?

# # ## It shows that on an Average a Billionaire in Hungray is Poorer than other Billionares in the world

# In[106]:


countries_realestate=df[df.Source=='real estate'].groupby('Country').Name.count()
countries_realestate.sort_values(ascending=False)


# In[111]:


z=countries_realestate
plt.figure(figsize=(10,6))
plt.xticks(rotation=75)
sns.barplot(y=z[:20], x=z.index[:20]);
plt.title("Count of Billionaires from RealEstate Source ");


# ## It seams that China has maximum representation of Billionaires  in RealeState.

# #### Q4: Billionaires List of India?

# In[129]:


india_df=df[df.Country=='India']
india_df=india_df.sort_values(by='Rank')
india_df


# In[153]:


plt.figure(figsize=(10,6))
plt.xticks(rotation=0)
plt.title('Billionaires Of India')
sns.barplot(y=india_df.Name[:20],x=india_df.NetWorth_Billion_Dollars[:20],alpha=.7);
plt.plot(india_df.NetWorth_Billion_Dollars[:20],india_df.Name[:20],'s-g',lw=3)
plt.xticks(india_df.NetWorth_Billion_Dollars[:4]);


# In[132]:


print('Top 10 richest Persons in India (acc to forbes-2021-Feb) are: ','\n')
india_df[["Name",'NetWorth_Billion_Dollars','Rank']].head(10)


# #### Q5: Which Sector in India has more Billionaires?
# 

# In[133]:


india_df.Source.nunique()


# In[142]:


india_Source=india_df.groupby('Source')["Name"].count().sort_values(ascending=False)
SD_Sources_india=india_Source.std(skipna = True)
SD_Sources_india


# In[154]:


plt.figure(figsize=(10,6))
plt.xticks(rotation=0)
plt.ylabel('Count')
plt.title('Count Of Billionaires')
sns.barplot(x=india_Source[:20],y=india_Source.index[:20]);


# ## Clearly Pharmaceuticals is the winner here.No doubt that India is world leader in the field of Pharmaceuticals.
# ## SD for India Billionaires Count for individual Souces  ~3.

# # Inferences and Conclusion
# 
# ### 1.there are total '2755' Billionaires in The World(FEB-2021).
# ### 2.We see that there is large change in net worth as we move up the ranks .
# ### 3.On an Average a Billionaire in France is Welthier than other Billionares in the rest of world.
# ### 4.Though U.S tops in Billionaires Count and net Billionaires wealth but It ranks second in c Conc .(Billionaires/Population)wise.Sweden has most Billionaires per million Population.
# ### 5.We can conclude that Real State major source of Our Billionaires.China have most Billionairesl in Working in RealeState. 
# ### 6.Pharmaceuticals in India has Most No. of Billionaires.
# 
# 
# 
# # Conclusion
# 
# ### 1. US tops on almost all parameters.
# ### 2.India Features in Most of the Top(20) list But is is very Far Behind in Billionaires Concentrtion which tells that India people as of whole has lot to improve and a huge scope for growth.
# ### 3.Realestate  houses most of our worlds Billionaires has nigligiblle rep amoung Indian Billionaires.
# ### 4.Indian Billionaires Soucres Count Has SD~3 and World Billionaires Sources SD ~ 9 which shows that there is much more Diversified Sources of Wealth available in India as Compared with rest of the world. Which is inline with Many Developing Countries.

# ## References and Future Work
# 
# We can compare Data of previous 2020 billionaires list and map for new entrants and se the effect of Covid 19 on wealth of Billionaires.
# We can also see country, source wise effect of Covid-19.
# ### Most IMP: It will also be helpful in Finding  the sources of wealth which has recorded most inc in Count of Billionaires. 

# In[62]:


import jovian


# In[168]:


jovian.commit()


# In[ ]:




