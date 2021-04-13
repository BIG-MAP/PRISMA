
class Spectrum:    
    object_identifiers = {'Class':'Spectrum',
                        'BattInfo ID': '00X0X0'}

    def __init__(self, energies, counts, parent = None, **kwargs):

        self.energies = energies
        self.counts = counts
        self.parent = parent

        self.metadata = {}
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.metadata.update(value)
            else:
                self.metadata.update({key:value})

    @property
    def class_id(self):
        return self.__class__.object_identifiers #return the class variable of the class instantiating the object



class SpectrumRaw(Spectrum):
    object_identifiers = {'Class':'SpectrumRaw',
                        'BattInfo ID': '12DX0X0'}



class SpectrumProcessed(Spectrum):
    object_identifiers = {'Class':'SpectrumProcessed',
                        'BattInfo ID': '997X0X0'}

    @property
    def baseline(self):
        if self.metadata['Process'] == 'Baseline correction':
            return self.parent.counts - self.counts
        else:
            return None
    


class SpectrumPeakfit(Spectrum):
    object_identifiers = {'Class':'SpectrumPeakfit',
                        'BattInfo ID': '240WPPMIn4'}

    def __init__(self, energies, counts, parent, profiles, **kwargs):
        Spectrum.__init__(self, energies, counts, parent, **kwargs)

        self.profiles = profiles



if __name__ == '__main__':
    raw_spectrum = Spectrum(46,12, wavelnght=45)
    test_object = SpectrumPeakfit(10,25,raw_spectrum, 'kaka', fit_parameters=45)
    print(test_object.parent.parent)
    # print(dir(test_object))
    # print(type(test_object.__str__()))
    