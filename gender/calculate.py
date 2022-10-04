import streamlit as st

def share_male_female(result):
    male = 0
    female = 0
    male_p = 0
    female_p = 0
    # Make a list out of the grouped table results
    result_list = []
    try: result_list.append(["M", result["M"] ])
    except: pass
    try: result_list.append(["F", result["F"] ])
    except: pass

    # Calculate percentage results
    for res in result_list:
        if res[0] == "M":
            male = res[1]
        elif res[0] == "F":
            female = res[1]
        male_p = round(male*100/(male+female),2)
        female_p = round(female*100/(female+male),2)

    return male_p, female_p


def csv_share_male_female(result):
    """
    Takes a dataframe and calculates the probability of femal and male
    """
    male = 0
    female = 0
    male_p = 0
    female_p = 0
    # Make a list out of the grouped table results
    result_list = []
    try: result_list.append(["M", result["M"] ])
    except: pass
    try: result_list.append(["F", result["F"] ])
    except: pass

    # Calculate percentage results
    for res in result_list:
        if res[0] == "M":
            male = res[1]
        elif res[0] == "F":
            female = res[1]
        male_p = round(male*100/(male+female),2)
        female_p = round(female*100/(female+male),2)

    if male_p > female_p:
        gender = "m"
        return gender, male_p
    else:
        gender = "f"
        return gender, female_p


def precit_from_data(data, name, country, continent):
    if name and country:
        st.write("name and country")
        df_name = data[(data["name"] == name.lower()) & (data["country"] == country)].groupby("gender")["wgt"].sum()
    elif name and continent:
        st.write("name and continent")
        df_name = data[(data["name"] == name.lower()) & (data["region"] == continent)].groupby("gender")["wgt"].sum()
    elif name:
        st.write("name")
        df_name = data[data["name"] == name.lower()].groupby("gender")["wgt"].sum()
    else:
        print("no data given")

    male_p, female_p = share_male_female(df_name)
    return male_p, female_p


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
        gender, perc = share_male_female(df_name)
        return gender, perc

def extend_result_and_shorten(df, result):

    for index, res in enumerate(result):
        df.loc[index, "gender"] = res[0]
        df.loc[index, "percentage"] = res[1]

        if df.loc[index, "check_all"] == [False, False]:
            df.loc[index, "check_all"] = "Name"
        elif (df.loc[index, "check_all"] == [True, False]) | (df.loc[index, "check_all"] == [True, True]):
            df.loc[index, "check_all"] = "Name and Country"
        elif (df.loc[index, "check_all"] == [False, True]) :
            df.loc[index, "check_all"] = "Name and Continent"

    df = df.rename(columns={"check_all": "method used"})
    return df[["name","country","continent", "method used","gender","percentage"]].copy()
