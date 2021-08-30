![Logo](./static/logo1.png) 
# PRISMA MODELS API

### Spectrum objects 

#### class Spectrum  
`Spectrum(energies, counts, parent=None, **kwargs)`  
The base spectrum class. Constructs spectrum objects. 
> **Arguments**
>* `energies`: numpy 1D array. The vector of energies of the spectrum   
>* `counts`: numpy 1D array. The vector of corresponding counts (e.g. counts, counts/s, absorbance, etc.). Must have the same shape as energies.  
>* `parent`: spectrum object (default=None). The spectrum object that was used as input to generate the current spectrum object (i.e. a provenance keeper).  
>* `kwargs`: key=value pairs. Anotate the spectrum object with metadata (e.g. name = 'my_spectrum', time = 23, temperature = 45). If the value is a dict, the key:value pairs are unpacked as metadata records as well.  

>**Attributes**
>* `energies`: numpy 1D array.  
>* `counts`: numpy 1D array.  
>* `parent`: spectrum object (default=None).
>* `metadata`: dict. Metadata annotations as key:value pairs. If the spectrum object is output from a process, the metadata contains the type of process and the input parameters used.  
>* `class_id`: dict. Name and identifiers of the class generating the object. The identifiers include the BattINFO Ontological URI.

#### class SpectrumProcessed  
`SpectrumProcessed(energies, counts, parent=None, **kwargs)`  
A processed spectrum. Inherits from class Spectrum with additional properties generated during processing. The medatada of SpectrumProcessed object stores the analysis type and parameters used.  
>**Attributes inherited from Spectrum**


#### class SpectrumPeakfit  
`SpectrumPeakfit(energies, counts, parent, profiles, **kwargs)`  
A peak fitting of the spectrum. Inherits from class Spectrum with additional properties generated during processing. The medatada of the SpectrumPakfit object stores the both the fitting parameters and the resulting fitting coefficients.   
> **Arguments**
>* `profiles`: dict. Individual profile fitting a peak in the spectrum, as profile_number(int):numpy 1D array pairs.  

>**Attributes**
>* `profiles`: dict. Individual profile fitting a peak in the spectrum, as profile_number(int):numpy 1D array pairs.
>* Attributes inherited from Spectrum

### Processing methods
#### class Preprocessing  
`Preprocessing()`  
Class grouping processes that modify the raw spectrum, e.g. smooting, outlier removal, trimming, etc. Each process is defined as a static method that can be invoked with the dot notation.   

`Preprocessing().trimming(spectrum, within)`  
Trims the input spectrum within a range.  
> **Arguments**
>* `spectrum`: spectrum object used as input.
>* `within`: [float,float]. The range defining where the spectrum is trimmed.  

>**Returns**: SpectrumProcessed object (trimmed)  

#### class Baselines  
`Baselines()`  
Class grouping processes that perform baseline correction. Each process is defined as a static method that can be invoked with the dot notation.  

`Baselines().asymmetric_least_squares(spectrum, log_p, log_lambda)`  
Finds an baseline curve for the spectrum using the assymetric least squares method.  
> **Arguments**
>* `spectrum`: spectrum object used as input.
>* `log_p`: float. Controls the weight given to datapoints with low counts (likely to belong to the baseline).    
>* `log_lambda`: float. Controls the degree of smoothness of the baseline curve.

>**Returns**: SpectrumProcessed object (baseline corrected spectrum)  

#### class FitPeaks  
`FitPeaks()`  
Class grouping processes that model as spectrum as a set of overlapping profiles with defined lineshape and parameters.  
`FitPeaks().fit_peaks(spectrum, peak_bounds, guess_widhts, lineshape)`  
Fit a spectrum with a set of overlapping profiles. 
> **Arguments**
>* `spectrum`: spectrum object used as input.
>* `peak_bounds`: list of 2-tuples of floats. Sets the lower and upper bound for the position of each peak. E.g. `[(10,30),(40,60)]` bounds the energy of the first profile between 10 and 30, and the energy of the second profile between 40 and 60. NOTE: len(peak_bounds) must be equal to len(guess_widths)   
>* `guess widths`: list of floats. Provides an initial guess of the profile widths. E.g. `[20, 50]` initialize the fitting with two profiles, one with 20 and other with 50 energy units. NOTE: len(peak_bounds) must be equal to len(guess_widths)   
>* `lineshape`" str. Lineshape of the profiles. Currently available: 'Lorentzian', 'Gaussian', 'Pseudo-Voight 50% Lorentzian'.  

>**Returns**: SpectrumPeakfit object (counts are the sum of the overlapping profiles)

### Parsers
#### class Parsers  
`Parsers()`  
Class grouping parsers that load energies and count arrays from a bitstream (e.g. from a FileUpload widget) and create Spectrum objects. Each parser is defined as a static method that can be invoked with the dot notation.  

`Parsers().single_csv(bitstream)`  
Reads the bitstream from a .csv file and generates spectrum objects. 
> **Arguments**
>* `bitstream`: string. Bitstream representing the content of the .csv file. The .csv file must follow a format where the first column contains the wavenumbers, and the successive columns the count columns labelled with the spectra names. For instance: 
| Wavenumbers       | spect_label_1    | spect_label_2   | spect_label_3 ...| 
| :------------- | :----------: | -----------: | -----------: |
|  100 | 12.2   | 40.8 | 11 |
| 200  | 21.1 | 25.2 | 0.8 |
| 300  | 2.85 | 32.0 | 99.2 |
| ...  | ... | ... | ... |  

>**Returns**:  
>* `spectra`: dict. Dictionary of spectrum_label:spectrum object pairs 
>* `metadata`: dict. Dictionary of parameter:value pairs. E.g. `{'Number of spectra':200, 'Highest wavenumber: 1000}`   

`Parsers().multiple_txt(upload)`  
Reads the bitstream from multiple .txt files and generates spectrum objects.  
> **Arguments**
>* `upload`: dictionary of label:bistream pairs representing the content of each .txt file. The .txt file must follow a format where the first column contains the wavenumbers, and a second column contain the counts; the columns must not be labelled. For instance:  
|      |      |
|  :------------- | -----------: |
|  100 | 12.2 | 
| 200  | 21.1 |
| 300  | 2.85 |
| ...  | ... |

>**Returns**:  
>* `spectra`: dict. Dictionary of spectrum_label:spectrum object pairs. The filenames are used as labels. 
>* `metadata`: dict. Dictionary of parameter:value pairs. E.g. `{'Number of spectra':200, 'Highest wavenumber: 1000}`  

`Parsers().single_txt_bruker(bitstream)`  
Reads the bitstream from a .txt file and generates spectrum objects. This parser is tailored to files exported from Bruker spectrometers.
> **Arguments**
>* `bitstream`: string. Bitstream representing the content of the .txt file. The .txt file follows a particular format, starting from instrument parameters labelled with hashtags, followed by a row of wavenumbers, and successive rows of counts whose first value is time. For instance: 
|  |  |  |  |   |
| :------------- | :----------: | -----------: | -----------: | -----------: |
| #Acquisition time: 10 s  |  |  |  |  |
| #Laser power: 5 mW  |  |  |  |   |
| #Repetitions: 3  |  |  |  |   |
|   | 100   | 200 | 300 | 400... |
| 30  | 12.2 | 21.1 | 2.85 | 16.4... |
| 60  | 40.8 | 25.2  | 32.0 | 67.7... |
| 90  | 11 | 0.8 | 99.2 | 21.0... |
| ...  | ... | ... | ... | 176... |   

>**Returns**:  
>* `spectra`: dict. Dictionary of spectrum_label:spectrum object pairs. The time values (first column) are used as labels. 
>* `metadata`: dict. Dictionary of parameter:value pairs. E.g. `{'Number of spectra':200, 'Highest wavenumber: 1000}`


```python

```
