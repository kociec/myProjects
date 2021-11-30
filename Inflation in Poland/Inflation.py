#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import modułów
import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt


# In[2]:


# import danych pobranych z Banku Danych Lokalnych GUS
part1 = pd.read_excel('F:\DataScience\Data\Inflacja\data1.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part2 = pd.read_excel('F:\DataScience\Data\Inflacja\data2.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part3 = pd.read_excel('F:\DataScience\Data\Inflacja\data3.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part4 = pd.read_excel('F:\DataScience\Data\Inflacja\data4.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part5 = pd.read_excel('F:\DataScience\Data\Inflacja\data5.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part6 = pd.read_excel('F:\DataScience\Data\Inflacja\data6.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part7 = pd.read_excel('F:\DataScience\Data\Inflacja\data7.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part8 = pd.read_excel('F:\DataScience\Data\Inflacja\data8.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part9 = pd.read_excel('F:\DataScience\Data\Inflacja\data9.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part10 = pd.read_excel('F:\DataScience\Data\Inflacja\data10.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part11 = pd.read_excel('F:\DataScience\Data\Inflacja\data11.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part12 = pd.read_excel('F:\DataScience\Data\Inflacja\data12.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part13 = pd.read_excel('F:\DataScience\Data\Inflacja\data13.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])
part14 = pd.read_excel('F:\DataScience\Data\Inflacja\data14.xlsx', sheet_name = 'DANE', usecols = ['Rodzaje produktów','Rok','Wartosc'])


# In[3]:


#  połączenie danych, ustawienie indeksów oraz unstack kolumny "Rok" z wierszy do kolumn dla lepszej prezentacji danych
part1.set_index(['Rodzaje produktów','Rok'], inplace = True)
data = part1.unstack(level = 'Rok')

parts = [part2, part3, part4, part5, part6, part7, part8, part9, part10, part11, part12, part13, part14]
for part in parts:
    part.set_index(['Rodzaje produktów','Rok'], inplace = True)
    part = part.unstack(level = 'Rok')
    data = data.append(part)
data.head()


# In[4]:


# Usunięcie multiindeksu "Wartosc"
data = data.transpose()
data.reset_index(inplace = True)
data = data.drop(columns =['level_0'])
data.set_index('Rok',inplace = True)
data = data.transpose()
data.head()


# In[5]:


# Zmiana nazwy kolumn
data.reset_index(inplace = True)
data.rename(columns = {'Rodzaje produktów':'ProduktLubUsluga'}, inplace = True)
data.set_index('ProduktLubUsluga', inplace = True)
data.head()


# In[6]:


# Usunięcie duplikatów i sprawdzenie rozmiaru tablicy
data.reset_index(inplace = True)
data.drop_duplicates(subset = ['ProduktLubUsluga'], inplace = True)
data.set_index('ProduktLubUsluga', inplace = True)
data.shape


# In[7]:


# Usunięcie produktów i usług z brakującymi wartosciami w wierszach
data = data.replace('-', np.NaN)
data.dropna(how = 'any', inplace = True)
data.shape


# In[8]:


# Eksport danych do MS Excel w celu korekty nazw produktów i usług oraz usunięcie pozycji nietypowych
data.reset_index(inplace = True)
excelWriter = pd.ExcelWriter('F:\DataScience\Data\Inflacja\data_export.xlsx')
data.to_excel(excelWriter, index = False)
excelWriter.save()


# In[9]:


# Ponowny import poprawionych danych wraz z kolumną zawierierającą szacowane miesięczne spożycie(koszyk inflacyjny)
data = pd.read_excel('F:\DataScience\Data\Inflacja\data_import.xlsx')
data.set_index('ProduktLubUsluga', inplace = True)
data.head(10)


# In[10]:


# wygenerowanie kolumn z kosztami danych produktów w danym roku

for number in range(0,11):
    data['kwota_'+str(2010+number)] = data[2010+number]*data['rocznie']
data.head(10)


# In[11]:


# Usunięcie wierszy z produktami/usługami nieobcnymi w koszyku inflacyjnym
data = data.where(data['kwota_2020'] != 0).dropna()
data.head(10)


# In[12]:


# Wycięcie niezbędnych kolumn do dalszych obliczeń i transpoza

lista = []
for number in range(0,11):
    position = 'kwota_'+ str(2010+number)
    lista.append(position)
lista
koszyk = data[lista]
koszyk = koszyk.transpose()
koszyk


# In[13]:


# Dodanie kolumny z sumą za każdy rok

lista = []
for number in range(0,11):
    suma = koszyk.loc['kwota_' + str(2010+number)].sum()
    lista.append(round(suma,2))

suma_koszyk = pd.Series(lista) 
koszyk.reset_index(inplace = True)
koszyk['suma_koszyk'] = suma_koszyk
koszyk.rename(columns = {'index':'Rok'}, inplace = True)
koszyk.set_index('Rok', inplace = True)
koszyk


# In[14]:


# wyodrębnienie kolumny z sumą i obliczenie rok-rocznej inflacji oraz sumarycznej od roku 2010

koszyk.reset_index(inplace = True)
inflacja = koszyk[['Rok','suma_koszyk']]
inflacja.set_index('Rok', inplace = True)
lista = inflacja['suma_koszyk'].tolist()

#obliczenie iflacji rok-rocznej
infl_r_r = [0]
for number in range(0, len(lista)-1):
    value = round(((lista[number+1]/lista[number])*100)-100,2)
    infl_r_r.append(value)

# obliczenie inflacji sumarycznej
infl_sum = [0]
for number in range(0,len(lista)-1):
    value = round(((lista[number+1]/lista[0])*100)-100,2)
    infl_sum.append(value)

# utworzenie nowych kolumn
inflacja.reset_index(inplace = True)    
inflacja['inflacja_r_r'] = infl_r_r
inflacja['inflacja_od_2010'] = infl_sum
inflacja.set_index('Rok', inplace = True)


# In[15]:


# zmiana nazw w indeksie 'Rok': np.  kwota_2014 ---> 2014
inflacja.reset_index(inplace = True)
inflacja['Rok'] = inflacja['Rok'].str.replace('kwota_','')
inflacja.set_index('Rok', inplace = True)
inflacja


# In[17]:


# Prezentacja danych na wykresie
plt.figure( figsize = (15,9))
plt.title("Inflacja w Polsce dla wybranego koszyka dóbr i usług")
plt.ylabel("Inflacja %")
plt.xlabel("Rok")
plt.plot(inflacja['inflacja_r_r'], marker = 'o', linestyle = ':', color = 'r', label = 'Inflacja r/r')
plt.plot(inflacja['inflacja_od_2010'],linestyle = 'dashed', color = 'g', marker = 'o', label = 'Inflacja sumaryczna')
plt.grid(linestyle = '--')
plt.legend(loc = 'upper left', fontsize = 15)
plt.xticks(rotation = 45)
plt.show()

