
import os
import pandas as pd

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
