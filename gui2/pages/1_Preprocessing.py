import streamlit as st
import pandas as pd
import plotly.express as px




st.subheader("Preprocessing")


tab_trim, tab_downsample, tab_outliers, tab_smoothing = st.tabs(["Trimming", "Downsampling", "Outliers", "Smoothing"])

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





df = pd.read_csv("ExxonMobil_CaCO3_LLDPE.txt", sep="\t", names= ["x","y"])
fig = px.scatter(df, x="x", y="y")
st.plotly_chart(fig, use_container_width=True)