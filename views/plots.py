import bqplot as plt
import ipywidgets as wdg
import numpy as np

class LinearPlots:
    """Parent class for plots"""

    def __init__(self, x_label = 'x', y_label = 'y', title = ''):
        self.labels = {'axis x':x_label,
                       'axis y':y_label,
                       'title': title}

        self.scales = {'x': plt.LinearScale(),
                        'y' : plt.LinearScale()}

        self.axes = {'x':plt.Axis(scale=self.scales['x'],label=self.labels['axis x'],
                                  orientation='horizontal',grid_lines='none'),
                    'y':plt.Axis(scale=self.scales['y'],label=self.labels['axis y'],
                                 orientation='vertical',grid_lines='none')}  

        self.define_marks()
        self.build_figure()    

#Figure with toolbar
    # def build_figure(self):
    #     out = wdg.Output()
    #     figure = plt.Figure(marks=[mark for mark in self.marks.values()],
    #                                 axes=[self.axes['x'],self.axes['y']],
    #                                 title=self.labels['title'],theme='gg',
    #                                 animation_duration=200)
    #     figure.layout = {'height':'300px', 'width':'550px'}
    #     toolbar = plt.toolbar.Toolbar(figure=figure)
    #     with out:
    #         display(figure, toolbar)
    #     self.interface = out

    
# Figure without toolbar
    def build_figure(self):
        self.interface = plt.Figure(marks=[mark for mark in self.marks.values()],
                                    axes=[self.axes['x'],self.axes['y']],
                                    title=self.labels['title'],theme='gg',
                                    animation_duration=200)
        self.interface.layout = {'height':'300px', 'width':'550px'}




class PlotBaseline(LinearPlots): 

    def define_marks(self):               
        self.marks = {'original': plt.Lines(scales=self.scales, colors=['gray']),
                     'baseline':plt.Lines(scales=self.scales, colors=['tomato'])}

    def update_marks(self,spectrum_raw=None, spectrum_procesed=None):
        if spectrum_raw != None:
            self.marks['original'].x = spectrum_raw.energies
            self.marks['original'].y = spectrum_raw.counts
        if spectrum_procesed != None:
            self.marks['baseline'].x = spectrum_procesed.energies
            self.marks['baseline'].y = spectrum_procesed.baseline




class PlotIntensities(LinearPlots): 

    def define_marks(self):
        self.marks = {'original': plt.Lines(scales=self.scales, colors=['gray'])}

    def update_marks(self,spectrum=None):
        if spectrum != None:
            self.marks['original'].x = spectrum.energies
            self.marks['original'].y = spectrum.counts




class PlotPeaks(LinearPlots): 

    def define_marks(self):
        self.marks = {'original': plt.Lines(scales=self.scales, colors=['gray']),
                     'peak_sum':  plt.Lines(scales=self.scales, stroke_width=3, colors=['turquoise']),
                     'peaks'    :  plt.Lines(scales=self.scales, fill = 'inside', stroke_width = 0)}


    def update_marks(self, spectrum_original=None, spectrum_fit=None):
        if spectrum_original != None:
            self.marks['original'].x = spectrum_original.energies
            self.marks['original'].y = spectrum_original.counts

        if spectrum_fit != None:
            n_peaks = spectrum_fit.metadata['Number of peaks']
            self.marks['peaks'].x = spectrum_fit.energies
            self.marks['peaks'].y = np.array([value for value in spectrum_fit.profiles.values()])
            self.marks['peak_sum'].x = spectrum_fit.energies
            self.marks['peak_sum'].y = spectrum_fit.counts

            self.marks['peaks'].fill_colors = n_peaks *['turquoise']
            self.marks['peaks'].fill_opacities = n_peaks*[0.3]
