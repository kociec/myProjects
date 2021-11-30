# importing modules
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# selecting columns for analysis
cols = ['CRIM','ZN','INDUS','CHAS','NOX','RM','AGE','DIS',
        'RAD','TAX','PTRATIO','B','LSTAT','MEDV']

# importing data
data = pd.read_csv(r"F:\DataScience\Data\housing\housing.data",
                   sep=' +', engine='python', header = None, 
                   names = cols)
 
# spliting data into X - features and y - target
X = data.drop('MEDV', axis=1)
y = data['MEDV'].values

# data standardization and scaling
scaler = StandardScaler()
scaler.fit(X,y)
X = scaler.transform(X)

# split the data into learning 80% and testing 20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

############# Create models for a constant alpha value (alph) equal to 1 #############

alph = 1.0

# Linear Model
linear = LinearRegression()
linear.fit(X_train, y_train)

# Lasso Model
lasso = Lasso(alpha = alph)
lasso.fit(X_train, y_train)

# Ridge Model
ridge = Ridge(alpha = alph)
ridge.fit(X_train, y_train)

# Elastic Net Model with L1 ratio = 0.5
elastic = ElasticNet(alpha = alph, l1_ratio = 0.5)
elastic.fit(X_train, y_train)

# Summary result weights (coef_) for all models
cols.remove('MEDV')
coef = pd.DataFrame(data = [linear.coef_, lasso.coef_, ridge.coef_, elastic.coef_]).transpose()
coef.index = cols
coef.columns = ['Linear', 'Lasso', 'Ridge', 'ElasticNet']
coef

#######################################################################
# LASSO model for variable value of parameter Alpha in the range < 0 ; 5 >

alpha_max = 5
alpha_list = np.arange(0.01, alpha_max, 0.01)
hz_line = np.zeros(alpha_max + 1)

lasso_coef = pd.DataFrame(columns= cols)
lasso_r2_train = []
lasso_r2_test = []

for a in alpha_list:
     lasso = Lasso(alpha = a)
     lasso.fit(X_train, y_train)
     lasso_coef.loc[a] = lasso.coef_
     lasso_r2_train.append(r2_score(y_train, lasso.predict(X_train)))
     lasso_r2_test.append(r2_score(y_test, lasso.predict(X_test)))
    
     
f = plt.figure( figsize = (15,10))
plt.title('Lasso coeficient changes for Alpha in range < 0 ; 5 >')
lasso_coef.plot(kind = 'line', ax = f.gca(), linewidth = 5)
plt.plot(hz_line, ls =':', linewidth = 5, color = 'black')
plt.xlabel("Alpha")
plt.ylabel("Coeficient")
plt.legend(loc = 'lower right')
plt.show()

plt.plot(alpha_list, lasso_r2_train, color = 'red', label = 'Train')
plt.plot(alpha_list, lasso_r2_test, color = 'green', label = 'Test')
plt.xlabel("Alpha")
plt.ylabel("R2 Score")
plt.title('Lasso R2 score changes for Alpha in range < 0 ; 5 >')
plt.legend(loc = 'upper right')
plt.show()

####################################################################################
# RIDGE model for variable value of parameter Alpha in the range < 0 ; 5 >

ridge_coef = pd.DataFrame(columns= cols)
ridge_r2_train = []
ridge_r2_test = []

for a in alpha_list:
     ridge = Ridge(alpha = a)
     ridge.fit(X_train, y_train)
     ridge_coef.loc[a] = ridge.coef_
     ridge_r2_train.append(r2_score(y_train, ridge.predict(X_train)))
     ridge_r2_test.append(r2_score(y_test, ridge.predict(X_test)))
    
     
f = plt.figure( figsize = (15,10))
plt.title('Ridge coeficient changes for Alpha in range < 0 ; 5 >')
ridge_coef.plot(kind = 'line', ax = f.gca(), linewidth = 5)
plt.plot(hz_line, ls =':', linewidth = 5, color = 'black')
plt.xlabel("Alpha")
plt.ylabel("Coeficient")
plt.legend(loc = 'lower right')
plt.show()

plt.plot(alpha_list, ridge_r2_train, color = 'red', label = 'Train')
plt.plot(alpha_list, ridge_r2_test, color = 'green', label = 'Test')
plt.xlabel("Alpha")
plt.ylabel("R2 Score")
plt.title('Ridge R2 score changes for Alpha in range < 0 ; 5 >')
plt.legend(loc = 'upper right')
plt.show()

####################################################################################
# ELASTIC NET model for variable value of parameter Alpha in the range < 0 ; 5 > with l1_ratio  = 0.5


elastic_coef = pd.DataFrame(columns = cols)
elastic_r2_train = []
elastic_r2_test = []

for a in alpha_list:
     elastic = ElasticNet(alpha = a, l1_ratio = 0.5)
     elastic.fit(X_train, y_train)
     elastic_coef.loc[a] = elastic.coef_
     elastic_r2_train.append(r2_score(y_train, elastic.predict(X_train)))
     elastic_r2_test.append(r2_score(y_test, elastic.predict(X_test)))
    
     
f = plt.figure( figsize = (15,10))
plt.title('ElasticNet coeficient changes for Alpha in range < 0 ; 5 >')
elastic_coef.plot(kind = 'line', ax = f.gca(), linewidth = 5)
plt.plot(hz_line, ls =':', linewidth = 5, color = 'black')
plt.xlabel("Alpha")
plt.ylabel("Coeficient")
plt.legend(loc = 'lower right')
plt.show()

plt.plot(alpha_list, elastic_r2_train, color = 'red', label = 'Train')
plt.plot(alpha_list, elastic_r2_test, color = 'green', label = 'Test')
plt.xlabel("Alpha")
plt.ylabel("R2 Score")
plt.title('Elastic Net R2 score changes for Alpha in range < 0 ; 5 >')
plt.legend(loc = 'upper right')
plt.show()

########################################################################
#  Creating a Heat Map

fig, ax = plt.subplots(figsize = (15,15))
sns.set(font_scale = 1.5)
corr = data.corr()
sns.heatmap(data = corr, square= True, annot = True, cbar = True, fmt = '.2f',
            annot_kws={'size': 15}, xticklabels = data.columns, yticklabels = data.columns)

########################################################################
#  Creating a pair plot with most corelated data to target column 'MEDV' with abs(corelation) > 0.45
cols = ['LSTAT', 'PTRATIO', 'TAX', 'RM', 'INDUS', 'MEDV']
chosen_data = data[cols]
sns. pairplot(chosen_data)

#######################################################################
# Eliminating outliers by IQR method from chosen data

Q1 = chosen_data.quantile(0.25) 
Q3 = chosen_data.quantile(0.75)
IQR = Q3 - Q1

outlier_condition = (chosen_data < Q1 - 1.5 * IQR) | (chosen_data > Q3 + 1.5 * IQR)

chosen_data_iqr = chosen_data[~outlier_condition].dropna()

########################################################################
#  Creating a pair plot with cleaned data
sns. pairplot(chosen_data_iqr)

########################################################################
# Creating a LinearRegression model with cleaned data and checking the score


X = chosen_data_iqr.drop('MEDV', axis=1)
y = chosen_data_iqr['MEDV'].values

scaler = StandardScaler()
scaler.fit(X,y)
X = scaler.transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

linear_chosen_iqr = LinearRegression()
linear_chosen_iqr.fit(X_train, y_train)

####################### SCORES #############################################

# MAE
mae_train = mean_absolute_error(y_train, linear_chosen_iqr.predict(X_train))
mae_test = mean_absolute_error(y_test, linear_chosen_iqr.predict(X_test))

# MSE
mse_train = mean_squared_error(y_train, linear_chosen_iqr.predict(X_train))
mse_test =  mean_squared_error(y_test, linear_chosen_iqr.predict(X_test))

# R2
r2_train = r2_score(y_train, linear_chosen_iqr.predict(X_train))
r2_test =  r2_score(y_test, linear_chosen_iqr.predict(X_test))































