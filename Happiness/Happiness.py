#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd           # importing modules
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data2015 = pd.read_csv(r'F:\DataScience\Data\happiness\\2015.csv')    # importing data
data2016 = pd.read_csv(r'F:\DataScience\Data\happiness\\2016.csv')
data2017 = pd.read_csv(r'F:\DataScience\Data\happiness\\2017.csv')
data2018 = pd.read_csv(r'F:\DataScience\Data\happiness\\2018.csv')
data2019 = pd.read_csv(r'F:\DataScience\Data\happiness\\2019.csv')
data2020 = pd.read_csv(r'F:\DataScience\Data\happiness\\2020.csv',sep = ';')


# In[2]:


# 2015 - unification of column names, deletion of unnecessary columns and setting the index

dictionary = {'Happiness Rank':'Overall rank','Happiness Score':'Score','Economy (GDP per Capita)':'GDP per capita', 'Health (Life Expectancy)':'Healthy life expectancy','Freedom':'Freedom to make life choices','Trust (Government Corruption)':'Perceptions of corruption','Family':'Social support' }
data2015.rename(dictionary, axis = 1, inplace = True)
del data2015['Region']
del data2015['Standard Error']
del data2015['Dystopia Residual']
data2015.set_index('Country', inplace = True)
data2015.head()


# In[3]:


# 2016 -  unification of column names, deletion of unnecessary columns and setting the index

dictionary = {'Happiness Rank':'Overall rank','Happiness Score':'Score','Economy (GDP per Capita)':'GDP per capita', 'Health (Life Expectancy)':'Healthy life expectancy','Freedom':'Freedom to make life choices','Trust (Government Corruption)':'Perceptions of corruption','Family':'Social support' }
data2016.rename(dictionary, axis = 1, inplace = True)
del data2016['Region']
del data2016['Lower Confidence Interval']
del data2016['Upper Confidence Interval']
del data2016['Dystopia Residual']
data2016.set_index('Country', inplace = True)
data2016.head()


# In[4]:


# 2017 -  unification of column names, deletion of unnecessary columns and setting the index

dictionary = {'Happiness.Rank':'Overall rank','Happiness.Score':'Score','Economy..GDP.per.Capita.':'GDP per capita', 'Health..Life.Expectancy.':'Healthy life expectancy','Freedom':'Freedom to make life choices','Trust..Government.Corruption.':'Perceptions of corruption','Family':'Social support' }
data2017.rename(dictionary, axis = 1, inplace = True)
del data2017['Whisker.high']
del data2017['Whisker.low']
del data2017['Dystopia.Residual']
data2017.set_index('Country', inplace = True)
data2017.head()


# In[5]:


# 2018 -  unification of column names and setting the index

dictionary = {'Country or region':'Country'}
data2018.rename(dictionary, axis = 1, inplace = True)
data2018.set_index('Country', inplace = True)
data2018.head()


# In[6]:


# 2019 -  unification of column names and setting the index

dictionary = {'Country or region':'Country'}
data2019.rename(dictionary, axis = 1, inplace = True)
data2019.set_index('Country', inplace = True)
data2019.head()


# In[7]:


# 2020 -  unification of column names and setting the index

dictionary = {'Country or region':'Country'}
data2020.rename(dictionary, axis = 1, inplace = True)
data2020.set_index('Country', inplace = True)
data2020.head()


# In[8]:


# adding column with info about year

data2015.insert(loc = 8, column = 'Year', value = '2015')
data2016.insert(loc = 8, column = 'Year', value = '2016')
data2017.insert(loc = 8, column = 'Year', value = '2017')
data2018.insert(loc = 8, column = 'Year', value = '2018')
data2019.insert(loc = 8, column = 'Year', value = '2019')
data2020.insert(loc = 8, column = 'Year', value = '2020')


# In[9]:


# connecting DataFrames from all years to one Frame

data = data2015.append(data2016).append(data2017).append(data2018).append(data2019).append(data2020)
len(data)


# In[10]:


# setting multiindex as "Year" and "Country", sorting both indexes ascending, replacing 'NaN' ---> 0

data.reset_index(inplace = True)
data.set_index(['Country','Year'], inplace = True)
data.sort_index(inplace = True)
data.fillna(value = 0, inplace = True)


# In[11]:


# rounding numbers to 3 decimal places and checking a data

col_names = ['Overall rank', 'Score', 'GDP per capita', 'Social support','Healthy life expectancy', 
             'Freedom to make life choices','Perceptions of corruption', 'Generosity']
data[col_names] = round(data[col_names],3)
data.head(12)


# In[12]:


# Does money give happiness?

data.plot(kind = 'scatter', x = 'Score', y = 'GDP per capita',
          ylabel = 'GDP per capita', xlabel = 'Happiness', figsize = (10,5), color = 'r')

# World rather says...YES.


# In[13]:


# Can we buy health?

data.plot(kind = 'scatter', x = 'Healthy life expectancy', y = 'GDP per capita',
          ylabel = 'GDP per capita', xlabel = 'Healthy life expectancy', figsize = (10,5), color = 'b')

# World also suggest answer "YES".


# In[14]:


# OK, so lets find a place on Earth, where we can be happy without big money (GDP) influence :)

data['Happy/GDP Ratio'] = round(data['Score'] / data['GDP per capita'], 3)    # calculating "Happiness to GDP ratio"

hasGDP = data['GDP per capita'] > 0.2    # can be low GDP, but lets say must be at least 0.2

ScoreOver7 = data['Score'] > 7.0           # we are looking for really happy countries - level at least 7/10

data[hasGDP & ScoreOver7].sort_values(by = 'Happy/GDP Ratio', ascending = False).head() # Finding of results

# All top5 countries from Latin America!


# In[15]:


# Now, on the contrary, let's find some countries, where happinness is mainly based on money.

hasBigGDP = data['GDP per capita'] > data['GDP per capita'].mean()    # GDP above average

ScoreOver4 = data['Score'] > 4           # Happiness can be low, but lets say must be at least 4/10

data[hasBigGDP & ScoreOver4].sort_values(by = 'Happy/GDP Ratio', ascending = True).head()

# Top3 results comes from Arabian countries, 4/5 from Asia.


# In[16]:


#  removing column 'Happy/GDP Ratio' and reindex
   
del data['Happy/GDP Ratio']
data.reset_index(inplace = True)
data.set_index('Country', inplace = True)
data.head()


# In[17]:


# defining a function to represent the selected column for Poland its neighbours

def showCol(colname):
    plt.figure( figsize = (15,7))
    plt.plot(data.loc['Poland','Year'], data.loc['Poland',colname], color = 'red', label = 'Poland', marker = 'o', linestyle = 'dashed')
    plt.plot(data.loc['Germany','Year'],data.loc['Germany',colname], color = 'blue', label = 'Germany', marker = 'o', linestyle = 'dashed')
    plt.plot(data.loc['Czech Republic','Year'],data.loc['Czech Republic',colname], color = 'cyan', label = 'Czech Republic', marker = 'o', linestyle = 'dashed')
    plt.plot(data.loc['Slovakia','Year'],data.loc['Slovakia',colname], color = 'green', label = 'Slovakia', marker = 'o', linestyle = 'dashed')
    plt.plot(data.loc['Ukraine','Year'],data.loc['Ukraine',colname], color = 'orange', label = 'Ukraine', marker = 'o', linestyle = 'dashed')
    plt.plot(data.loc['Belarus','Year'],data.loc['Belarus',colname], color = 'yellow', label = 'Belarus', marker = 'o', linestyle = 'dashed')
    plt.plot(data.loc['Lithuania','Year'],data.loc['Lithuania',colname], color = 'black', label = 'Lithuania', marker = 'o', linestyle = 'dashed')
    plt.plot(data.loc['Russia','Year'],data.loc['Russia',colname], color = 'silver', label = 'Russia', marker = 'o', linestyle = 'dashed')
    
    font1 = {'family':'serif','color':'blue','size':12}
    font2 = {'family':'serif','color':'darkred','size':15}
    
    plt.xlabel('Year', fontdict = font1 )
    plt.ylabel(colname, fontdict = font1)
    plt.title(colname + ' in Poland and its neighbourhood', fontdict = font2)
    plt.legend(loc = 'lower right', fontsize = 12)
    plt.grid(linestyle = '--')
    plt.xticks(rotation = 45)
    plt.show()
    
# calling the function for "Score"

showCol('Score')


# In[18]:


# calling the function for "GDP per capita"

showCol('GDP per capita')


# In[19]:


# calling the function for "Healthy life expectancy"

showCol('Healthy life expectancy')


# In[20]:


# calling the function for "Freedom to make life choices"

showCol('Freedom to make life choices')


# In[21]:


# "Healthy life expectancy" and "GDP per capita" for Poland, Germany and Ukraine compared to the rest of the world.

ALL = data.plot(kind = 'scatter', x = 'Healthy life expectancy', y = 'GDP per capita',
          ylabel = 'GDP per capita', xlabel = 'Healthy life expectancy', color = 'gray')

PL = data.loc['Poland'].plot(kind = 'scatter', x = 'Healthy life expectancy', y = 'GDP per capita',
          ylabel = 'GDP per capita', xlabel = 'Healthy life expectancy', color = '#ff0000', ax = ALL, label = 'Poland', marker = 'H', s = 100)

UKR = data.loc['Ukraine'].plot(kind = 'scatter', x = 'Healthy life expectancy', y = 'GDP per capita',
          ylabel = 'GDP per capita', xlabel = 'Healthy life expectancy', color = '#00ffff', ax = PL, label = 'Ukraine', marker = 'H', s = 100)

DEU = data.loc['Germany'].plot(kind = 'scatter', x = 'Healthy life expectancy', y = 'GDP per capita',
          ylabel = 'GDP per capita', xlabel = 'Healthy life expectancy', figsize = (15,8), color = '#00ff00', ax = UKR, label = 'Germany', marker = 'H', s = 100)


# In[22]:


data


# In[23]:


# preparing data for Machine Learning - removing unnecessary columns

data_ML = data.copy()

data_ML.reset_index(inplace = True)

del data_ML['Country']
del data_ML['Overall rank']
del data_ML['Year']
data_ML.head(10)


# In[24]:


#  Creating a Heat Map

fig, ax = plt.subplots(figsize = (7,7))
sns.set(font_scale = 1.5)
corr = data_ML.corr()
sns.heatmap(data = corr, square= True, annot = True, cbar = True, fmt = '.2f',
            annot_kws={'size': 15}, xticklabels = data_ML.columns, yticklabels = data_ML.columns)


# ## SOME MACHINE LEARNING ... :)

# In[25]:


# importing modules for Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


# In[26]:


#  Preparing data and creating model based on most corelated columns, where abs(corelation) > 0.5

mostCorelatedCols = ['GDP per capita', 'Social support', 'Healthy life expectancy','Freedom to make life choices', 'Score']
data_ML = data_ML[mostCorelatedCols]

# Eliminating outliers by IQR method
Q1 = data_ML.quantile(0.25) 
Q3 = data_ML.quantile(0.75)
IQR = Q3 - Q1
outlier_condition = (data_ML < Q1 - 1.5 * IQR) | (data_ML > Q3 + 1.5 * IQR)
data_ML_iqr = data_ML[~outlier_condition].dropna()

# spliting data into X - features and y - target
X = data_ML_iqr.drop('Score', axis  = 1)
y = data_ML_iqr['Score'].values

# split the data into learning 80% and testing 20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

linear = LinearRegression()
linear.fit(X_train, y_train)

# R2 score for training and testing
r2_train = r2_score(y_train, linear.predict(X_train))
r2_test =  r2_score(y_test, linear.predict(X_test))

#printing results
print('R2 TRAIN ', round(r2_train,3), '\tR2 TEST:', round(r2_test,3))


# In[27]:


# Quick look to data

data[mostCorelatedCols].sample(5)


# In[28]:


#  checking coefficients for trained model:
# "GDP per capita", "Social support", "Healthy life expectancy", "Freedom to make life choices"
linear.coef_


# In[29]:


#  checking the "heat map" for data taken for machine learning

fig, ax = plt.subplots(figsize = (5,5))
sns.set(font_scale = 1)
corr = data_ML_iqr.corr()
sns.heatmap(data = corr, square= True, annot = True, cbar = True, fmt = '.2f',
            annot_kws={'size': 15}, xticklabels = data_ML_iqr.columns, yticklabels = data_ML_iqr.columns)


# ### Conclusion: The correlation coefficients between data features (heat map) are moderately related to the resulting model coefficients (model.coef_)

# In[30]:


# Making a prediction for sample countries (from 2020, becouse data was sorted ascending, and we use tail method)

sampleCountries = ['Poland', 'Germany', 'Russia', 'Mexico', 'Australia', 'Lesotho', 'Brazil', 'Norway', 'Ukraine']
predictedValues = []
for country in sampleCountries:
    
    value_1 = float(data[mostCorelatedCols].loc[country,'GDP per capita'].tail(1))
    value_2 = float(data[mostCorelatedCols].loc[country,'Social support'].tail(1))
    value_3 = float(data[mostCorelatedCols].loc[country,'Healthy life expectancy'].tail(1))
    value_4 = float(data[mostCorelatedCols].loc[country,'Freedom to make life choices'].tail(1))

    prediction = linear.predict([[value_1, value_2, value_3, value_4]])
    prediction = round(prediction[0], 3)
    predictedValues.append(prediction)
predictedValues


# In[31]:


# Checking real "Score" values for sample countries

realValues = []
for country in sampleCountries:
    real_value = float(data[mostCorelatedCols].loc[country, 'Score'].tail(1))
    realValues.append(real_value)
realValues


# In[32]:


# comparing predictions with real "Score" Values

for predict, real, country in zip(predictedValues, realValues, sampleCountries):
    print('For {0:^12s} real "Score" value was: {1:^8.2f}| model predicts: {2:^8.2f}| absolute error is {3:^8.2f}'.format(country, real, predict, real - predict))
    print('-' * 100)


# In[33]:


# Making a prediction for luxury "Wonderland" with very high factors

GBP = 2.0
socialSupport = 1.6
lifeExpectancy = 1.6
freedom = 1.5

prediction = linear.predict([[GBP, socialSupport, lifeExpectancy, freedom]])
prediction = round(prediction[0], 3)

print('Happyness factor for "Wonderland" is equal to', prediction)

