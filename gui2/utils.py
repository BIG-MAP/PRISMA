import pandas as pd
from typing import Union, List
from streamlit.uploaded_file_manager import UploadedFile




def read_spectra(uploaded_files: List[UploadedFile]):

    assert isinstance(uploaded_files, list), "The argument passed to read_spectra is not a list, but {}".format(type(uploaded_files))

    number_of_files = len(uploaded_files)

    if number_of_files == 0:
        pass

    elif number_of_files == 1:
        pass

    elif number_of_files > 1:
        pass

