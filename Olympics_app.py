# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 22:36:13 2023

@author: Administrator
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file = r'C:/Users/Administrator/Desktop/Python/athlete_events.csv'
df = pd.read_csv(file)
file_1 = r'C:/Users/Administrator/Desktop/Python/noc_regions.csv'
df_1 = pd.read_csv(file_1)
df_merged = df.merge(df_1)
# Data cleaning
df_age = df_merged['Age'].fillna(0)
df_height = df_merged['Height'].fillna(0)
df_weight = df_merged['Weight'].fillna(0)
df_medal = df_merged['Medal'].fillna('None')
df_region = df_merged['region'].fillna('None')

# Updating nan values
df_merged['Age'].update(df_age)
df_merged['Height'].update(df_height)
df_merged['Weight'].update(df_weight)
df_merged['Medal'].update(df_medal)
df_merged['region'].update(df_region)
 
# Creating Gold,Silver,Bronze columns from Medal column
Medals_df = pd.get_dummies(df_merged.Medal)
df_2 = pd.concat([df_merged,Medals_df],axis = 1)

#Changing Gold,Silver,Bronze column type float to int
df_2 = df_2.astype({"Gold":'int', "Silver":'int' , "Bronze" : 'int'})

all_countries = sorted(df_2['region'].unique())
Select_country = st.selectbox('Select Country',all_countries)
# Subset on selected countries
subset = df_2[df_2['region'] == Select_country]
medal = df_2[df_2['Medal'] != 'None']

Total_participants = subset['ID'].nunique()
Total_gold_medal = (subset['Medal'] == 'Gold').sum()
Total_silver_medal = (subset['Medal'] == 'Silver').sum()
Total_bronze_medal = (subset['Medal'] == 'Bronze').sum()

st.header('Olympics Data set - {}'.format(Select_country))
st.subheader('Made by Tanzila')
col1, col2, col3, col4 = st.columns(4)
with col1:
         col1.metric('Number of Olympians', Total_participants)
with col2:
         col2.metric('Number of Gold Medal',Total_gold_medal)
with col3:
         col3.metric('Number of Silver Medal',Total_silver_medal)
with col4:
         col4.metric('Number of Bronze Medal',Total_bronze_medal)
         
with st.container():
    left,middle,right = st.columns(3)
    
    left.header('Medal over the year')
    data_chart = subset.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False)
    plt.plot(data_chart)
    plt.legend(data_chart)
    plt.xlabel('Year')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.ylabel('Number of Medals')
    
    left.pyplot()
    middle.header('Medal over the athelete')
    arr = subset.groupby('ID').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).head(5)
    fig,ax = plt.subplots()
    arr.plot.barh()
    middle.pyplot()
    
    right.header('Medal over sport')
    table_data = subset.groupby('Sport').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).head(5)
    right.table(table_data)
    
with st.container():
    b_left,b_middle,b_right = st.columns(3)
    b_left.header('Medals over age')
    hist_data = subset.groupby('Age').count()['Medal'].sort_values(ascending = False)
    sns.histplot(hist_data , x = subset['Age'])
    b_left.pyplot()
    
    b_middle.header('Medal over Gender')
    subset_medal = subset[subset['Medal'] != 'None']
    pie_data = subset_medal.groupby(['Sex','Medal'])['Medal'].count().sort_values(ascending = False)
    plt.pie(pie_data , labels= pie_data.index)
    b_middle.pyplot()
    
    b_right.header('Season over Medal')
    bar_data = subset.groupby('Season')['Medal'].count().sort_values(ascending = False)
    fig,ax = plt.subplots()
    bar_data.plot.bar()
    b_right.pyplot()
    
    
    
    
    