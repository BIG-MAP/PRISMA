import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from PIL import Image
import requests



st.title("Prototype for views")

response = requests.get("https://raw.githubusercontent.com/BIG-MAP/PRISMA/main/docs/figures/logo.png",
                        stream=True)
if response.status_code == 200:
        logo = BytesIO(response.content)
        logo = Image.open(logo).convert('RGB')

st.sidebar.image(image=logo)
st.sidebar.button("PRISMA", use_container_width= True)
st.sidebar.button("Smoothing", use_container_width= True)
st.sidebar.button("Baseline Correction", use_container_width= True)
st.sidebar.button("Peak Fitting", use_container_width= True)
st.sidebar.button("Process and Save", use_container_width= True)

donwsamp_col1, donwsamp_col2, donwsamp_col3 = st.columns(3)

donwsamp_col1.write('Downsampling threshhold')
donwsampling_threshold = donwsamp_col2.slider('', 0.0, 1.0, 0.2, label_visibility="collapsed")
if donwsamp_col3.button('*i*', key="downsampling"):
    st.toast("""Applies the XX algorithm to downsample a spectrum. See [Documentation](https://www.google.com/)  

    * 0: no downsampling  
    * 1: maximum 
    """)


smooth_col1, smooth_col2, smooth_col3 = st.columns(3)

smooth_col1.write('Smoothing window')
smooth_param = smooth_col2.slider('', 3, 100, 2, label_visibility="collapsed")
if smooth_col3.button('*i*', key="smoothing"):
    st.toast("Applies the XX algorithm to smooth a spectrum. See [Documentation](https://www.google.com/)")


df = pd.read_csv("ExxonMobil_CaCO3_LLDPE.txt", sep="\t", names= ["x","y"])
fig = px.scatter(df, x="x", y="y")
st.plotly_chart(fig, use_container_width=True)