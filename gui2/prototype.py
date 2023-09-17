import streamlit as st
from io import BytesIO
from PIL import Image
import requests



response = requests.get("https://raw.githubusercontent.com/BIG-MAP/PRISMA/main/docs/figures/logo.png",
                        stream=True)
if response.status_code == 200:
        logo = BytesIO(response.content)
        logo = Image.open(logo).convert('RGB')

col1, col2 = st.columns([1,3])

col1.image(logo)
col2.title("PRISMA")
col2.markdown("An app for high-throughput processing of spectra.")
col2.markdown("Eibar Flores | [The BIG-MAP Project](https://www.big-map.eu/) | [Cite](https://doi.org/10.1002/cmtd.202100094).")



uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)