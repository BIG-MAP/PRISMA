"""Templates of Spectrum object"""

class Spectrum:    


    object_identifiers = {'Class':'Spectrum',
                        'BattInfo ID': '00X0X0'}


    def __init__(self, indexes, counts, **kwargs):

        self.indexes = indexes
        self.counts = counts
        self.__load_metadata(**kwargs)

    
    def __load_metadata(self, **kwargs):

        self.metadata = {}
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.metadata.update(value)
            else:
                self.metadata.update({key:value})


    @property
    def class_id(self):
        return self.__class__.object_identifiers #return the class variable of the class instantiating the object





class SpectrumProcessed(Spectrum):


    object_identifiers = {'Class':'SpectrumProcessed',
                        'BattInfo ID': '997X0X0'}
                        
    def __init__(self, indexes, counts, baseline, **kwargs):
        Spectrum.__init__(self, indexes, counts, **kwargs)
        self.baseline = baseline
    




class SpectrumPeakfit(Spectrum):


    object_identifiers = {'Class':'SpectrumPeakfit',
                        'BattInfo ID': '240WPPMIn4'}

    def __init__(self, indexes, counts, profiles, **kwargs):
        Spectrum.__init__(self, indexes, counts,  **kwargs)
        self.profiles = profiles







if __name__ == '__main__':
    raw_spectrum = Spectrum(46,12, wavelnght=45)
    test_object = SpectrumPeakfit(10,25,raw_spectrum, 'kaka', fit_parameters=45)
    # print(dir(test_object))
    # print(type(test_object.__str__()))
    