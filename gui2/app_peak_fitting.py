import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px


st.sidebar.image(Image.open("./gui2/assets/logo.png"))

st.header("Peak fitting")



################### FILE UPLOAD #####################


with st.sidebar.expander("Upload files"):

        parser = st.radio("Format of spectra", 
                                options=["Single .csv", "Single .txt (Bruker)", "Multiple .txt"], 
                                help="See documentation: what formats are accepted")
        
        multiple_files = True if parser == "Multiple .txt" else False

        uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=multiple_files)


################### PEAK FITTING SPECS #####################

st.selectbox(label="Peak lineshape", options=["Lorentizan", "Gaussian", "Pseudo-Voight"])

data_df = pd.DataFrame(
    {"Minimum":[],
    "Maximum":[],
     "Width":[],
    }
)

st.data_editor(data_df, hide_index=True, num_rows="dynamic")