import numpy as np
from models.spectrum import SpectrumRaw
# from spectrum import Spectrum



class Parsers:
    """Load spectra from different formatted files and instantiates Spectrum objects along with their metadata"""

    available_parsers = {'Single .csv':          {'multiple files': False,'file format':'.csv'},
                         'Single .txt (Bruker)': {'multiple files': False,'file format':'.txt'},
                         'Multiple .txt':        {'multiple files': True, 'file format':'*'}}    


    @staticmethod
    def parse(payload, parser):
        if parser == 'Single .csv':
            return Parsers.single_csv(payload)
        elif parser == 'Single .txt (Bruker)':
            return Parsers.single_txt_bruker(payload)
        elif parser == 'Multiple .txt':
            return Parsers.multiple_txt(payload)
        else:
            raise KeyError('The parser is not defined')



    @staticmethod
    def single_txt_bruker(bitstream: str):
        
        #initialize variables
        spectra, spectra_metadata = {}, {}
        energies = None

        try:
            for line in bitstream.split(sep=b'\n'):
                counts, label = None, None #refresh after every loop

                if line.startswith(b'#'): #ignore metadata from instrument 
                    pass

                elif line == b'': #ignore empty lines (like the last line)
                    pass

                elif line.startswith(b'\t'): #line where wavenumbers are stored
                    energies = np.array(line.split(b'\t'))[1:].astype('float64') #avoid first element because is ''

                else:
                    temporary_array = np.array(line.split(b'\t')).astype('float64')
                    label, counts = temporary_array[0], temporary_array[1:]   
                    #for every line of counts, instatiate spectrum          
                    spectra[label] = {'root': SpectrumRaw(energies = energies, 
                                                        counts = counts, 
                                                        name=label, 
                                                        min_resolvable_width = np.abs(energies[1]-energies[0]))} 

            spectra_metadata['common_energy_axis'] = True
            spectra_metadata['energy_limits']=[np.amin(energies),np.amax(energies)]
            spectra_metadata['number_of_spectra'] = len(spectra)   
            spectra_metadata['number_of_datapoints'] = len(energies)
            spectra_metadata['min_resolvable_width'] = np.abs(energies[1]-energies[0])
            spectra_metadata['error'] = ''

            if spectra_metadata['number_of_spectra'] == 0:
                spectra = None
                spectra_metadata['error'] = "File not recognized. Consult the documentation for supported *.txt file format"
            else:
                spectra_metadata['error'] = ""

        except ValueError:
            spectra = None
            spectra_metadata['error'] = "File not recognized. Consult the documentation for supported *.txt file format"

        return spectra, spectra_metadata



    @staticmethod
    def single_csv(bitstream: str): 
        
        #initialize variables
        spectra, spectra_metadata = {}, {}

        try:

            #separate bitstream into a list of lines
            read_lines = bitstream.split(sep=b'\r\n')

            #read the first line: names attached to each spectrum. Ignores first element of line (empty string)
            spectra_names = np.array(read_lines[0].split(sep=b',')[1:], dtype=str) 

            #Read remaining lines. Each line is a row that starts with the wavenumber, and continues with the intensity of each spectrum at that wavenumber.
            #Each line is split into elements (via ;), transformed into a numpy array and stored as an element of the list
            #Lines starting with empty string (b'') are ignored.
            #List is also transformed to a numpy array
            spectra_data = np.array([np.array(line.split(sep=b','), dtype=float) for line in read_lines[1:] if line.split(sep=b',')[0] != b''])

            energies = spectra_data.T[0]


            for label, column in zip(spectra_names, spectra_data.T[1:]):
                spectra[label] = {'root': SpectrumRaw(energies = energies, 
                                                    counts = column, 
                                                    name=label, 
                                                    min_resolvable_width = np.abs(energies[1]-energies[0]))} #instatiate spectrum


            spectra_metadata['common_energy_axis'] = True
            spectra_metadata['energy_limits']=[np.amin(energies),np.amax(energies)]
            spectra_metadata['number_of_spectra'] = len(spectra) 
            spectra_metadata['number_of_datapoints'] = len(energies)  
            spectra_metadata['min_resolvable_width'] = np.abs(energies[1]-energies[0])

            if spectra_metadata['number_of_spectra'] == 0:
                spectra = None
                spectra_metadata['error'] = "File not recognized. Consult the documentation for supported *.csv file format"
            else:
                spectra_metadata['error'] = ""

        except ValueError:
            spectra = None
            spectra_metadata['error'] = "File not recognized. Consult the documentation for supported *.csv file format"

        return spectra, spectra_metadata




    @staticmethod
    def multiple_txt(upload: dict):        

        #initialize variables
        energies_min, energies_max, overall_min_res_width, n_datapoints = float('inf'), -float('inf'), float('inf'), 0 
        first_energy_axis = np.array([])
        spectra, spectra_metadata = {}, {'common_energy_axis': True} 

        try:

            for label, bitstream in upload.items():

                #read byte string with spectrum values    
                array = np.array(bitstream.split(sep=None))
                energies, counts = array.reshape((int(len(array)/2),2)).astype('float64').T 


                #check if spectra share energy axis
                if not np.any(first_energy_axis):
                    first_energy_axis = energies
                elif not np.array_equal(first_energy_axis,energies):
                    spectra_metadata['common_energy_axis'] = False
                    

                #update overall minimum and maximum values of energy, and the maximum number of datapoints
                current_minimum_energy_value = np.amin(energies)
                current_maximum_energy_value = np.amax(energies)
                current_n_datapoints = len(energies)
                current_min_res_width = np.abs(energies[1]-energies[0])
                energies_min = current_minimum_energy_value if current_minimum_energy_value < energies_min else energies_min
                energies_max = current_maximum_energy_value if current_maximum_energy_value > energies_max else energies_max
                n_datapoints = current_n_datapoints if current_n_datapoints > n_datapoints else n_datapoints
                overall_min_res_width = current_min_res_width if current_min_res_width < overall_min_res_width else overall_min_res_width

                #add spectrum object to dictionary
                spectra[label] = {'root': SpectrumRaw(energies = energies, 
                                                    counts = counts, 
                                                    name=label, 
                                                    min_resolvable_width = current_min_res_width)} #parent: None


            spectra_metadata['energy_limits']=[energies_min,energies_max]
            spectra_metadata['number_of_spectra'] = len(spectra)
            spectra_metadata['number_of_datapoints'] = n_datapoints 
            spectra_metadata['min_resolvable_width'] = overall_min_res_width


            if spectra_metadata['number_of_spectra'] == 0:
                spectra = None
                spectra_metadata['error'] = "Some of the files were not recognized. Consult the documentation for supported *.txt file format"
            else:
                spectra_metadata['error'] = ""

        except ValueError:
            spectra = None
            spectra_metadata['error'] = "Some of the files were not recognized. Consult the documentation for supported *.txt file format"

        return spectra, spectra_metadata








if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # #load data from single textfile
    # path = r'C:\Users\eibfl\Documents\Lead_projects\software_spectra_analysis\example_data_horiba_chalmers'
    # filename = 'HC Li LP40 operando_01.txt'
    # spectra, spectra_metadata = Parsers().horiba_single_file(path, filename)
    # name = list(spectra.keys())[0]
    # plt.plot(spectra[name].raw['energies'],spectra[name].raw['counts'])
    # plt.show()

    # #load binary text file
    path = r'C:\Users\eibfl\Documents\Lead_projects\software_spectra_analysis\example_data_horiba_psi\dummy_file.txt'
    with open(path,mode='rb') as spectra_file:
        spectra, spectra_metadata = Parsers().multiple_txt({'test file':spectra_file.read()})
    name = 'test file'

    print(spectra)

    plt.plot(spectra[name]['root'].energies,spectra[name]['root'].counts)
    plt.show()