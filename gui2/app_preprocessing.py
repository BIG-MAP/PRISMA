import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import os



st.sidebar.image(Image.open("./gui2/assets/logo.png"))

st.header("Preprocessing")


################### FILE UPLOAD #####################
with st.expander("Upload files"):

        chosen_format = st.radio("File format", 
                                options=["Single CSV file", "Multiple CSV files"], 
                                help="See documentation: what formats are accepted")

        uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True)

file_namnes = [uploaded_file.name for uploaded_file in uploaded_files]


st.sidebar.selectbox("Spectra", file_namnes)
close_app = st.sidebar.button("Close app")


################## CONTROLS ###########################

tab_trim, tab_downsample, tab_outliers, tab_smoothing, tab_baseline = st.tabs(["Trimming", "Downsampling", "Outliers", "Smoothing"," Baseline correction"])

with tab_trim:
    st.markdown("Keeps only a subset of a spectrum for further processing")
    trimm_range:tuple[int] = st.slider("Trimming range",400, 4000, [400, 4000])

with tab_downsample:
    st.markdown("How many points are kept from original signal. Ex. 2: singal reduced by half.")
    donwsampling_factor:int = st.slider('Downsampling factor', 1, 10, 1)

with tab_outliers:
    st.markdown("Removes points outside 1.5 IQR from the median difference value.")
    remove_outliers:bool = st.toggle('Remove outliers')

with tab_smoothing:
    st.markdown("Applies the Eilers smoorther to a spectrum.")
    smooth_threshold:int = st.slider('Smoothing window', 3, 100, 5)

with tab_baseline:
    st.markdown("Applies Eiler's ALS algorithm to fit a baseline to spectra")
    baseline_p:tuple[int] = st.slider("P-parameter",3, 14, 7)
    baseline_alpha:tuple[int] = st.slider("Alpha-parameter",3, 14, 7)



################## PLOT ###########################

example_csv_path = "./gui2/ExxonMobil_CaCO3_LLDPE.txt"
df = pd.read_csv(example_csv_path, sep="\t", names= ["x","y"])
fig = px.scatter(df, x="x", y="y")
st.plotly_chart(fig, use_container_width=True)

if close_app:
     os._exit(0)