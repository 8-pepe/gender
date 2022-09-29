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
