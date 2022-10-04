import pandas as pd
import os
import streamlit as st
from calculate import precit_from_data
from data import load_data


st.set_page_config(
            page_title="Gender",
            page_icon="🖼",
            layout="wide",
            initial_sidebar_state="auto") # collapsed



###########
# Give result only with database
country = None
continent = None
male_p = False
female_p = False


data = load_data()
country_list = sorted(data["country"].unique())
country_list.insert(0, "No Selection")




# streamlit
name = st.text_input('Put the name here', 'Name')

with st.container():
    country = st.selectbox(
        'Country of origin',
        (country_list))
    st.write('You selected:', country)
    if country == "No Selection":
        country = False


#country = st.text_input('Country of origin', '')


# continent
with st.container():

    continent = st.radio('Chose a continent:', ('No Selcetion','Oceania', 'Americas', 'Europe', 'Asia', 'Africa'))
if continent == "No selcetion":
    continent = None


if st.button('Generate'):
    print("name:",name)
    print("country:", country)
    print("continent:", continent)
    'Your results will be generated:'
    male_p, female_p = precit_from_data(data, name, country, continent)

    if male_p or female_p:
        st.markdown("-------------------------------")
        st.markdown(f"The results for the name {name}:")
        st.markdown(f"Male: {male_p} %")
        st.markdown(f"Female: {female_p} %")
