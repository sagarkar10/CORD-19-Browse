import streamlit as st
import pandas as pd
import json
from utils import get_most_similar_title
from data_io import DataIO


@st.cache()
def get_result(query, df, top_n):
    return get_most_similar_title(query, df, top_n)

@st.cache()
def get_data():
    dataio=DataIO()
    df = dataio.get_data()
    return df

def main():
    st.title("CORD-19 Data Analysis")
    st.header("Please Enter Query/Title to Search Similar Research Titles")
    query = st.text_input("Plain Text Only")
    top_n = st.slider('Show Top n Predicted docs?', min_value=5, max_value=30, value=5)
    st.header("Prediction")
    
    if st.button("Run"):
        res = get_result(query, get_data(), top_n)
        st.json(json.dumps(res))

if __name__=="__main__":
    main()

