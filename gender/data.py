import os
import pandas as pd
import streamlit as st


@st.cache(show_spinner=False)
def load_data():
    path = os.path.join("..","raw_data","wgnd_2_0_name-gender-code.csv")
    df = pd.read_csv(path)

    # Clean data
    # kick out where gender is not defined
    df = df[df["gender"] !="?"]

    # add country names and regions
    path_cc = os.path.join("..","raw_data","country-code","all-country-codes_continent_subregion.csv")
    cc_all = pd.read_csv(path_cc, sep=",")
    cc_short = cc_all[["alpha-2", "name", "region", "sub-region"]].copy()
    cc_short.rename(columns={"name":"country"}, inplace=True)
    df.rename(columns={"code":"alpha-2" }, inplace=True)

    # merge data and country info
    data = pd.merge(df, cc_short, how="left", on="alpha-2")
    continent_list = data["region"].unique()
    # clean merged data
    data = data[data["alpha-2"] != "??"] #filter out names where there is no country assigned

    return data

def clean_uploaded_data(df):
    # Convert to string
    df["name"] = df["name"].astype(str)
    df["country"] = df["country"].astype(str)
    df["continent"] = df["continent"].astype(str)
    # smal lettters
    df["name"] = df["name"].apply(lambda x: x.lower())
    df["country"] = df["country"].apply(lambda x: x.lower())
    df["continent"] = df["continent"].apply(lambda x: x.lower())

    return df

def shorten_dataframe(data,df):
    data_short = data[data['name'].isin(df["name"])]
    print(data.shape)
    return data_short

def save_result(df_new):
    import time
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    path_save = os.path.join("data","results",f"{timestamp}_genderized.csv")
    df_new.to_csv(path_save, index=False)
