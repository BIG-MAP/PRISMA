import streamlit as st




st.title("Prototype for views")

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