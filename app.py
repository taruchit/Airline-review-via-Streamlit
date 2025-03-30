# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 23:05:46 2025

@author: pc
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#Title of the web page
st.title("Sentiment analysis based on passenger reviews for Qatar Airways")

#Title of the sidebar
st.sidebar.title("Sentiment analysis of reviews about Qatar Airways")

#Adding a markdown
st.markdown("Analyzing sentiments of customers based on their review.")

DATA_URL="qatar_airways_reviews.csv"

@st.cache_data
def load_data():
    data=pd.read_csv(DATA_URL)
    data['Date Published']=pd.to_datetime(data['Date Published'])
    return data

data=load_data()


#Asking the user to tell the rating against which the 
#respective random review must be fetched
st.sidebar.subheader("Sample reviews based on rating")
random_rating=st.sidebar.slider("Select the rating for which review is to be fetched",1,10)
st.sidebar.markdown(data.query('Rating == @random_rating')["Review Body"].sample(n=1))

st.sidebar.markdown("###Number of reviews per rating")
review_count=data['Rating'].value_counts()
review_count=pd.DataFrame({'Rating':review_count.index,'Frequency':review_count.values})
fig=px.bar(review_count,x='Rating', y='Frequency',height=500, title='Number of Reviews per Rating')
st.plotly_chart(fig)

st.sidebar.subheader("Breakdown of Airline review based on seat type")
seat_type=st.sidebar.multiselect('Pick seat type',('Economy Class','Business Class','First Class','Premium Economy'),key='0')

if len(seat_type)>0:
    seat_type_data=data[data["Seat Type"].isin(seat_type)]
    fig_seat_type=px.histogram(seat_type_data, x='Seat Type', y='Rating', histfunc='count', facet_col='Rating', labels={'Review Body':'Reviews'}, height=600, width=800)
    st.plotly_chart(fig_seat_type)