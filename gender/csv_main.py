import pandas as pd
import os
import streamlit as st
from calculate import  csv_predict_from_data, extend_df_with_result, csv_share_male_female
from data import load_data, clean_uploaded_data, shorten_dataframe, save_result


st.set_page_config(
            page_title="Gender-CSV",
            page_icon="🖼",
            layout="wide",
            initial_sidebar_state="auto") # collapsed



###########


with st.container():
    st.set_option('deprecation.showfileUploaderEncoding', False)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file,sep=";",names=["name","country","continent"])
        st.write(df.head())



if st.button('Generate'):
    'Your data will be genderized'

    # clean uploaded data
    df = clean_uploaded_data(df)
    # prepare stored database
    data = load_data()
    data = shorten_dataframe(data,df)

    # Enrich uploaded dataframe
    country_list = data["country"].unique()
    continents_list = data["region"].unique()

    def check_country(country):
        return country.lower() in country_list
    df["c_country"] = df["country"].apply(check_country)

    def check_continent(continent):
        return continent.lower() in continents_list
    df["c_continent"] = df["continent"].apply(check_continent)

    def check_all(row):
        res_list = []
        res_list.append(row['c_country'])
        res_list.append(row["c_continent"])
        return res_list

    df["check_all"] = df.apply(check_all, axis=1)

    ### Run the classification
    def csv_predict_from_data(row):
        """
        Create a temporary dataframe with name and gender in differnt countries
        Adds rows with gender and percentage to the input dataframe
        """

        if row["check_all"][0]:
            print("name and country")
            df_name = data[(data["name"] == row["name"] ) & (data["country"] == row["country"])].groupby("gender")["wgt"].sum()
        elif row["check_all"][1]:
            print("name and continent")
            df_name = data[(data["name"] == row["name"] ) & (data["region"] == row["continent"])].groupby("gender")["wgt"].sum()
        else:
            print("just name or nothing")
            df_name = data[data["name"] == row["name"].lower() ].groupby("gender")["wgt"].sum()

        if df_name.empty:
            return "No Data", "No Data"
        else:
            gender, perc = csv_share_male_female(df_name)
            return gender, perc




    result = df.apply(csv_predict_from_data, axis=1)
    df_new = extend_df_with_result(df, result)

    # Save result
    save_result(df_new)

    st.markdown("Here are the results")
    st.write(df_new.head())

    def convert_df(df_new):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df_new.to_csv().encode('utf-8')

    csv = convert_df(df_new)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )
