import pandas as pd
import os
import streamlit as st
import time
from datetime import datetime as dt
from datetime import timedelta as td
from calculate import  csv_predict_from_data, extend_result_and_shorten, csv_share_male_female
from data import load_data, clean_uploaded_data, shorten_dataframe, save_result


st.set_page_config(
            page_title="Gender-CSV",
            page_icon="🖼",
            layout="wide",
            initial_sidebar_state="auto") # collapsed



###########
st.write("# Welcome to - AI Genderizer")
st.write("### Genderize your data within minutes!")



with st.container():
    st.set_option('deprecation.showfileUploaderEncoding', False)


    st.write("#### Important: Please upload your data in this following format:")
    st.write("1. A headline with column-names is not needed")
    st.write("2. Order of columns: ")
    st.markdown("- 1st: name / 2nd: country / 3rd: continent")
    st.markdown('- Please upload your file as ".csv" with ";" as separator')
    st.markdown('- Only column "name" is necessary, but results are more accurate with additional "country" or "continent" column.')
    st.markdown("3. Detailled instructions:")
    link = '[For detailled instructions click here](/instructions_csv_upload)'
    st.markdown(link, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("###")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        list-style-position: inside;
    }
    </style>
    ''', unsafe_allow_html=True)

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file,sep=";",names=["name","country","continent"], encoding='latin-1')
        st.write(df.head(8))
        st.markdown(f"The file has {df.shape[0] :,} rows.")
        st.write("Please check if your data is shown and separated correctly.")
        st.write("If not please read the instruction for uploading data above and reupload your data.")



        if st.button('Generate'):
            'Your data will be genderized...'

            st.markdown("""---""")

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
            df = df.reset_index(level=0)

            ### Run the classification
            def csv_predict_from_data(row):
                """
                Create a temporary dataframe with name and gender in differnt countries
                Adds rows with gender and percentage to the input dataframe
                """
                n_row = row["index"]
                if n_row%100 == 0:
                    print(n_row)


                if row["check_all"][0]:
                    df_name = data[(data["name"] == row["name"] ) & (data["country"] == row["country"])].groupby("gender")["wgt"].sum()
                elif row["check_all"][1]:
                    df_name = data[(data["name"] == row["name"] ) & (data["region"] == row["continent"])].groupby("gender")["wgt"].sum()
                else:
                    df_name = data[data["name"] == row["name"].lower() ].groupby("gender")["wgt"].sum()


                if df_name.empty:
                    return "No Data", 0
                else:
                    gender, perc = csv_share_male_female(df_name)
                    return gender, perc



            def run_apply(df):
                start_time = dt.now()
                result = df.apply(csv_predict_from_data, axis=1)
                end_time = dt.now()
                run_time = end_time - start_time
                run_time =  str(run_time).split(".")[0]
                return result , run_time
            result, run_time = run_apply(df)
            print(run_time)
            df_new = extend_result_and_shorten(df, result)

            # Save result
            save_result(df_new)

            st.markdown("### Your results are ready")
            st.markdown(f'Runtime: {run_time} (h/min/sec)')
            st.markdown("###")
            st.write(df_new.head(8))

            def convert_df(df_new):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df_new.to_csv(sep=";").encode('utf-8')

            csv = convert_df(df_new)

            with st.container():
                st.write("Download your results")

                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name='result_data.csv',
                    mime='text/csv')
