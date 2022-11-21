import streamlit as st
from calculate import precit_from_data
from gender.data import load_data


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
    if continent == "No Selcetion":
        continent = None


if st.button('Generate'):
    print("name:",name)
    print("country:", country)
    print("continent:", continent)
    'Your results will be generated:'
    male_p, female_p, df_name_all = precit_from_data(data, name, country, continent)
    print(male_p)
    print(female_p)

    #  Change how the dataframe is displayed - restructure it in tow dataframes maybe woman and men or by country
    df_show = df_name_all.drop(columns=["alpha-2", "name", "region", "sub-region"])
    df_show = df_show[["country", "gender", "wgt"]]
    df_show.rename(columns={"wgt":"percentage"}, inplace=True)
    df_show["percentage"] = df_show["percentage"].apply(lambda x: str(round(x*100))) + "%"

    if male_p or female_p:
        st.markdown("-------------------------------")
        st.markdown(f"The results for the name {name}:")
        st.markdown(f"Male: {male_p} %")
        st.markdown(f"Female: {female_p} %")
        st.markdown("-------------------------------")
        st.markdown(f"Details by countries for name: {name}")

        st.dataframe(df_show)
