# © Copyright 2021, PRISMA’s Authors
import numpy as np

"""Templates of Spectrum object"""

class Spectrum:    


    object_identifiers = {'Class':'Spectrum',
                        'BattInfo ID': '00X0X0'}


    def __init__(self, indexes:np.array, counts:np.array, baseline:np.array=None, peaks:dict=None, **kwargs):

        self.indexes = indexes
        self.counts = counts
        self.baseline = baseline
        self.peaks = peaks
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







if __name__ == '__main__':
    raw_spectrum = Spectrum(46,12, wavelnght=45)
    # print(dir(test_object))
    # print(type(test_object.__str__()))
    