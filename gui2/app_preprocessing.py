
import streamlit as st
import sys
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import os




@st.cache_data
def set_wdir():
    # Add the root directory of your repository to the Python path
    current_directory = os.path.dirname(os.path.abspath(__file__))
    repository_root = os.path.join(current_directory, '..')
    sys.path.append(repository_root)

set_wdir()

from prisma import parsers, preprocessing, baselines
from prisma.spectrum import Spectrum



################## FUNCTIONS #####################



@st.cache_data
def payload_to_spectra(payload, parser:str):
    """ Load spectra from the FileUpload streamlit widget, using prisma parsers"""

    if parser == 'Single .csv':
        spectra, spectra_metadata = parsers.single_csv(payload.getvalue())
    elif parser == 'Single .txt (Bruker)':
        spectra, spectra_metadata = parsers.single_txt_bruker(payload.getvalue())
    elif parser == 'Multiple .txt':
        spectra, spectra_metadata = parsers.multiple_txt({spectrum_bits.name : spectrum_bits.getvalue() for spectrum_bits in payload})
    else:
        raise KeyError('The parser is not defined')
    
    return spectra, list(spectra.keys()), spectra_metadata



@st.cache_data
def update_preprocessing_parameters(spectra_metadata:dict = None):
    """ Keeps track of pre-processing parameters that are updated from metadata values form the spectra"""

    if not spectra_metadata: #use default preprocessing params
        preprocs_params = {
            "trimming": {
                "min_value":400,
                "max_value": 4000,
                "value": [500, 3500]
            }}
    else:
        min_index, max_index = spectra_metadata["energy_limits"]
        preprocs_params = {
                "trimming": {
                    "min_value":int(min_index),
                    "max_value": int(max_index),
                    "value": [int(0.25*(max_index - min_index)+min_index), int(0.75*(max_index - min_index)+min_index)]
                }}
        
    return preprocs_params



def process_spectrum(spectrum:Spectrum,
                    trim_range:tuple[int],
                    donwsampling_factor:int,
                    remove_outliers:bool,
                    baseline_p:tuple[int],
                    baseline_lambda:tuple[int]):
    """Takes preprocessing parameters from the widgets to apply all pre-processing functions"""
    
    processed_spectrum = preprocessing.trimming(spectrum, trim_range)
    processed_spectrum = preprocessing.downsample(processed_spectrum, donwsampling_factor)
    processed_spectrum = preprocessing.reject_outliers(processed_spectrum, remove_outliers)
    processed_spectrum = baselines.asymmetric_least_squares(processed_spectrum, log_p=baseline_p, log_lambda=baseline_lambda)

    return processed_spectrum





######################################### MAIN APP LOOP  ###############################################



############## BOILERPLATE 

st.sidebar.image(Image.open("./gui2/assets/logo.png"))
st.header("Preprocessing")


############## RAW SPECTRUM
raw_spectrum_container = st.container()


########## FILE UPLOAD 

with st.sidebar.expander("Upload files"):

        parser = st.radio("Format of spectra", 
                                options=["Single .csv", "Single .txt (Bruker)", "Multiple .txt"], 
                                help="See documentation: what formats are accepted")
        
        multiple_files = True if parser == "Multiple .txt" else False

        uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=multiple_files)



if uploaded_files:

    spectra, spectra_names, spectra_metadata = payload_to_spectra(uploaded_files, parser = parser)

    with st.sidebar.expander("Spectra metadata"):
        st.json(spectra_metadata)

    selected_spectrum_name:str = st.sidebar.selectbox("Select spectrum", spectra_names)

    current_spectrum = spectra[selected_spectrum_name]

    preprocs_params = update_preprocessing_parameters(spectra_metadata) 

else:
    current_spectrum = None
    spectra_metadata = None


########## PROCESSING PARAMETERS


preprocs_params = update_preprocessing_parameters(spectra_metadata)


tab_trim, tab_downsample, tab_outliers, tab_baseline = st.tabs(["Trimming", "Downsampling", "Outliers"," Baseline correction"])


with tab_trim:
    st.markdown("Keeps only a subset of a spectrum for further processing")
    trimm_range:tuple[int] = st.slider("Trimming range",
                                       min_value = preprocs_params["trimming"]["min_value"],
                                       max_value = preprocs_params["trimming"]["max_value"],
                                       value = preprocs_params["trimming"]["value"])

with tab_downsample:
    st.markdown("How many points are kept from original signal. Ex. 2: singal reduced by half.")
    donwsampling_factor:int = st.slider('Downsampling factor', 1, 10, 1)

with tab_outliers:
    st.markdown("Removes points outside 1.5 IQR from the median difference value.")
    remove_outliers:bool = st.toggle('Remove outliers')


with tab_baseline:
    st.markdown("Applies Eiler's ALS algorithm to fit a baseline to spectra")
    baseline_p:float = st.slider("log10 (P-parameter)", min_value = -4.5, max_value = -0.5, value = -1.5, step = 0.25)
    baseline_lambda:float = st.slider("log10 (Lambda-parameter)", min_value = 2.0, max_value = 14.0, value = 7.0, step = 0.5)




############## PROCESSED SPECTRUM
processed_spectrum_container = st.container()




########## PROCESS SPECTRA AND PLOT
fig_raw = go.Figure()
fig_processed = go.Figure()


if current_spectrum:

    processed_spectrum = process_spectrum(spectrum=current_spectrum["root"],
                            trim_range= trimm_range,
                            donwsampling_factor=donwsampling_factor,
                            remove_outliers=remove_outliers,
                            baseline_p=baseline_p,
                            baseline_lambda=baseline_lambda)

    # Plots

    fig_raw.add_trace(go.Scatter(x=current_spectrum["root"].indexes,
                                 y=current_spectrum["root"].counts, 
                                 name="Raw spectrum",
                                 mode="markers",
                                 marker={"color":"#455A64"}))
    
    
    fig_raw.add_trace(go.Scatter(x=processed_spectrum.indexes,
                                 y=processed_spectrum.baseline, 
                                 name="Baseline", 
                                 mode="lines",
                                 marker={"color":"#FF1744"}))
    
    fig_raw.add_vrect(x0=min(current_spectrum["root"].indexes),
                      x1=trimm_range[0], 
                      fillcolor="white",
                      opacity=0.7,
                      line_width=10, 
                      line_color= "white")
    
    fig_raw.add_vrect(x0=trimm_range[1],
                      x1=max(current_spectrum["root"].indexes), 
                      fillcolor="white", 
                      opacity=0.7,
                      line_width=10, 
                      line_color= "white")
    
    fig_raw.update_xaxes(title_text="Index")
    fig_raw.update_yaxes(title_text="Counts")
    fig_raw.update_layout(legend=dict(
                        orientation="h",
                        entrywidth=70,
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1))

    
    
    fig_processed.add_trace(go.Scatter(x=processed_spectrum.indexes,
                                 y=processed_spectrum.counts, 
                                 name="Processed spectrum",
                                 mode="markers",
                                 marker={"color":"#455A64"}))
    
    fig_processed.update_xaxes(title_text="Index")
    fig_processed.update_yaxes(title_text="Counts")



else:
    fig_raw.add_trace(go.Scatter(x=[0],
                                 y=[0],
                                 mode="markers",
                                 marker={"color":"#455A64"}))
    
    fig_processed.add_trace(go.Scatter(x=[0],
                                 y=[0],
                                 mode="markers",
                                 marker={"color":"#455A64"}))


raw_spectrum_container.plotly_chart(fig_raw, use_container_width=True)
processed_spectrum_container.plotly_chart(fig_processed, use_container_width=True)


