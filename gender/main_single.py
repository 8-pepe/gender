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




# streamlit
name = st.text_input('Put the name here', 'Name')
country = st.text_input('Country of origin', '')

# country
with st.container():

    continent = st.radio('Chose a continent:', ('No selcetion','Oceania', 'Americas', 'Europe', 'Asia', 'Africa'))
if continent == "No selcetion":
    continent = None


if st.button('Generate'):
    print("name:",name)
    print("country:", country)
    print("continent:", continent)
    'Your individual artwork will be painted...'
    male_p, female_p = precit_from_data(data, name, country, continent)

    if male_p or female_p:
        st.markdown("The results for the name:")
        st.markdown(f"Male: {male_p} %")
        st.markdown(f"Female: {female_p} %")
