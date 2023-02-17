# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 03:03:35 2023

@author: Administrator
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
file = r'C:/Users/Administrator/Downloads/athlete_events.csv'
df = pd.read_csv(file)
df_1 = pd.read_csv(r'C:/Users/Administrator/Desktop/Python/noc_regions.csv')
df_merged = df.merge(df_1)
# Data Cleaning
# Checking null values
df_merged.isna().any()
# filling null values with mean
df_age = df_merged['Age'].fillna(df['Age'].mean())
df_height = df_merged['Height'].fillna(df['Height'].mean())
df_weight = df_merged['Weight'].fillna(df['Weight'].mean())
df_medal = df_merged['Medal'].fillna('Nan')
#df_region = df_merged['region'].fillna('Nan')
# updating null values with mean
df_merged['Age'].update(df_age)
df_merged['Height'].update(df_height)
df_merged['Weight'].update(df_weight)
df_merged['Medal'].update(df_medal)
#df_merged['region'].update(df_region)
# Changing data type of age 
#df['Age'] = df['Age'].astype('int')
st.title('Olympic History Dashboard')
st.subheader('Made by Tanzila')
all_year = sorted(df['Year'].unique())
year = st.selectbox('Select year',all_year)
df_merged['Gold_medal'] = df_merged['Medal'] == 'Gold'
df_merged['Silver_medal'] = df_merged['Medal'] == 'Silver'
df_merged['Bronze_medal'] = df_merged['Medal'] == 'Bronze'
df_country_gold = df_merged.groupby('region')['Gold_medal'].sum()
df_country_silver = df_merged.groupby('region')['Silver_medal'].sum()
df_country_bronze = df_merged.groupby('region')['Bronze_medal'].sum()
#curr_count = df_merged.groupby('region')['Medal'].count()
inc_count = 1000

curr_gold_medal = 13372
inc_gold_medal = -1000

curr_silver_medal = 13116
inc_silver_medal = -1000

curr_bronze_medal = 13295
inc_bronze_medal = -1000

st.header('Olympics - {}'.format(year))
col1, col2, col3,  = st.columns(3)
#col1.metric('Number of Olympians', curr_count)
col1.metric('Gold Medals', df_country_gold)
col2.metric('Silver Medals', df_country_silver)
col3.metric('Bronze Medals', df_country_bronze)

with st.container():
    left,middle,right = st.columns(3)
    chart_data = df
    