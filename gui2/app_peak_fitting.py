import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px


st.sidebar.image(Image.open("./gui2/assets/logo.png"))

st.header("Peak fitting")



################### FILE UPLOAD #####################
with st.expander("Upload files"):

        chosen_format = st.radio("File format", 
                                options=["Single CSV file", "Multiple CSV files"], 
                                help="See documentation: what formats are accepted")

        uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True)

file_namnes = [uploaded_file.name for uploaded_file in uploaded_files]