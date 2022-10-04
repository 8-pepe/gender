import streamlit as st
import os
import pandas as pd

st.write("# Instructions for csv upload")

st.write("### Your file should look like this:")
sample_path = os.path.join("data","sample", "sample-20.csv")
df = pd.read_csv(sample_path,sep=";",names=["name","country","continent"], encoding='latin-1')
st.write(df.head(10))
with st.container():
    st.write('#### You can download this sample file here:')
    df_download = df.to_csv(sep=";", index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=df_download,
        file_name='sample_file.csv',
        mime='text/csv')

st.write("### Columns:")
st.markdown('**We can process 3 colums: name, country and continent** ')
st.markdown('**"name"**: Name of the person.')
st.markdown("- This column is obligatory")
st.markdown(' **"country"**: Country of origin of the person.')
st.markdown('- The same name can have a different genders in different countries')
st.markdown(' **"continent"**: Continent of origin of the person')
st.markdown('- If you dont know the country it helps to put a general contint to use for genderization')

st.write("### Best Results:")
st.markdown('- You get the **best results** if you upload **"names" and "country"** since our AI has data for each country.')
st.markdown('- If you dont know the country you can improve your results by **providing a continent**')
