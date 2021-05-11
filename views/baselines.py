import ipywidgets as wdg         


class ViewBaselineAls:
    def __init__(self):
 
        self.interface = None
        self.widget = {}

        self.__buildbox()
        self.__assemble_interface()


    def __buildbox(self):
        """widgets for trim and baseline parameters""" 

        self.widget['Range_trim'] = wdg.FloatRangeSlider(min=0, max=10000, step=1, 
                                                        orientation='horizontal',   
                                                        description='Trim', 
                                                        continuous_update=False)

        self.widget['Slider_baseline_p'] = wdg.FloatSlider(value=-1.5,min=-4,max=0,step=0.5,
                                                           orientation='horizontal',
                                                           description='Log p',
                                                           continuous_update=False)

        self.widget['Slider_baseline_l'] = wdg.FloatSlider(value=7,min=0,max=14,step=0.5,
                                                          orientation='horizontal',
                                                          description='Log λ',
                                                          continuous_update=False)

        self.widget['Range_trim'].layout = {'width':'620px'}
        self.widget['Slider_baseline_p'].layout = {'width':'650px'}
        self.widget['Slider_baseline_l'].layout = {'width':'650px'}


    
    def __assemble_interface(self):
        self.widget['Label_Baseline'] = wdg.HTML(value='<h3>Baseline Correction</h3>')

        self.interface = wdg.VBox([self.widget['Label_Baseline'], self.widget['Range_trim'],
                                   self.widget['Slider_baseline_p'],self.widget['Slider_baseline_l']])
        



    def set_trim_limits(self, trim_limits, n_datapoints):
        interval = trim_limits[1]-trim_limits[0]
        self.widget['Range_trim'].min = trim_limits[0]
        self.widget['Range_trim'].max = trim_limits[1]
        self.widget['Range_trim'].step = 2*interval/n_datapoints
        self.widget['Range_trim'].value = [trim_limits[0]+0.25*interval,trim_limits[0]+0.75*interval]

    
    @property
    def inputs(self):
        summary = {'Trim':self.widget['Range_trim'].value,
                  'Log p':self.widget['Slider_baseline_p'].value,
                  'Log lambda': self.widget['Slider_baseline_l'].value}
        return summary

