import streamlit as st
import pandas as pd
import plotly.express as px




st.subheader("Preprocessing")


donwsamp_col1, donwsamp_col2, donwsamp_col3, donwsamp_col4 = st.columns([1,1, 1, 1])
donwsamp_col1.markdown('Downsampling', 
                       help= "How many points are kept from original signal. Ex. 2: singal reduced by half.")
donwsampling_threshold = donwsamp_col2.slider('', 1, 10, 1, label_visibility="collapsed")


donwsamp_col3.markdown('Remove Outliers', 
                     help="Removes points outside 1.5 IQR from the median difference value." )
tog_param = donwsamp_col4.toggle('', label_visibility="collapsed")



smooth_col1, smooth_col2, smooth_col3 = st.columns([1,1,2])
smooth_col1.markdown('Smoothing', 
                       help= "Applies the XX algorithm to smooth a spectrum.")
smooth_threshold = smooth_col2.slider('', 3, 100, 5, label_visibility="collapsed")






df = pd.read_csv("ExxonMobil_CaCO3_LLDPE.txt", sep="\t", names= ["x","y"])
fig = px.scatter(df, x="x", y="y")
st.plotly_chart(fig, use_container_width=True)