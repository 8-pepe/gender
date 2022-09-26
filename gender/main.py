import pandas as pd
import os

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


###########
# Give result only with database
name = "Dieter"
country = None
continent = None


def share_male_female(result):
    male = 0
    female = 0
    # Make a list out of the grouped table results
    result_list = []
    try: result_list.append(["M", result["M"] ])
    except: pass
    try: result_list.append(["F", result["F"] ])
    except: pass
    print("result_list", result_list)

    # Calculate percentage results
    for res in result_list:
        if res[0] == "M":
            male = res[1]
        elif res[0] == "F":
            female = res[1]
        male_p = round(male*100/(male+female),2)
        femal_p = round(female*100/(female+male),2)

    return male_p, femal_p


def precit_from_data(name, country, continent):
    if name and country:
        print("name and country")
        df_name = data[(data["name"] == name.lower()) & (data["country"] == country)].groupby("gender")["wgt"].sum()
    elif name and continent:
        print("name and continent")
        df_name = data[(data["name"] == name.lower()) & (data["region"] == continent)].groupby("gender")["wgt"].sum()
    elif name:
        print("name")
        df_name = data[data["name"] == "andrea"].groupby("gender")["wgt"].sum()
    else:
        print("no data given")

    print(df_name)
    male_p, femal_p = share_male_female(df_name)
    return male_p, femal_p
