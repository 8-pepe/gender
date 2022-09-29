import pandas as pd
import os
import streamlit as st
from calculate import precit_from_data
from data import load_data


st.set_page_config(
            page_title="Gender-CSV",
            page_icon="🖼",
            layout="wide",
            initial_sidebar_state="auto") # collapsed



###########
# Give result only with database
country = None
continent = None
male_p = False
female_p = False


with st.container():
    st.set_option('deprecation.showfileUploaderEncoding', False)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        data_uploaded = pd.read_csv(uploaded_file)
        st.write(data_uploaded)








if st.button('Generate'):
    print("country:", country)
    print("continent:", continent)
    'Your individual artwork will be painted...'
    male_p, female_p = precit_from_data(data, name, country, continent)

    if male_p or female_p:
        st.markdown("The results for the name:")
        st.markdown(f"Male: {male_p} %")
        st.markdown(f"Female: {female_p} %")
