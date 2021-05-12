import ipywidgets as wdg
import pandas as pd



class ViewFitPeaks:

    available_lineshapes = ['Lorentzian', 'Gaussian', 'Pseudo-Voight 50% Lorentzian']

    def __init__(self):
        #gui attributes
        self.interface = None
        self.widget = {}
        self.widgetbox = {}
        self.input_peaks = {'--':{}}
        #build gui panels
        self.__buildbox_addpeak()
        self.__buildbox_fitted_parameters()
        self.__buildbox_boundpeak()  
        self.__assemble_interface()
        self.__events()
    
    #----- build widget boxes -----

    def __buildbox_addpeak(self):
        self.widget['Button_add'] = wdg.Button(description='Add', icon='plus-square')
        self.widget['Button_remove'] = wdg.Button(description='Remove', icon='minus-square')
        self.widget['Select_peak'] = wdg.Select(options=['--'], value='--')

        self.widget['Select_peak'].layout = wdg.Layout(height='100px')
        
        self.widgetbox['addpeak'] = wdg.VBox([wdg.HBox([self.widget['Button_add'],
                                                        self.widget['Button_remove']]),
                                              self.widget['Select_peak']])


    def __buildbox_fitted_parameters(self):
        self.widget['Label_fitted_params'] = wdg.HTML() #'<h4>Fitted parameters</h4>'
        self.widget['Out_fitted_params'] = wdg.Output()
        self.widgetbox['fittedparams'] = wdg.VBox([self.widget['Label_fitted_params'], self.widget['Out_fitted_params']])


        
    def __buildbox_boundpeak(self):

        self.widget['Dropdown_lineshape'] = wdg.Dropdown(options=ViewFitPeaks.available_lineshapes)

        self.widget['Range_bounds'] = wdg.FloatRangeSlider(min=0, max=10000, step=1, 
                                                            orientation='horizontal',   
                                                            description='Bound within',
                                                            continuous_update=False)

        self.widget['Slider_width'] = wdg.FloatSlider(value=50.0,min=1.0,max=300.0,step=1,
                                                      orientation='horizontal',
                                                      description='Guess width',
                                                      continuous_update=False)

        self.widget['Button_peakfit'] = wdg.Button(description='Peak fit', icon='area-chart', 
                                                   disabled=True)

        self.widget['Range_bounds'].layout = {'width':'500px'}
        self.widget['Slider_width'].layout = {'width':'500px'}

        self.widgetbox['boundpeak'] = wdg.VBox([self.widget['Dropdown_lineshape'], self.widget['Range_bounds'],
                                                self.widget['Slider_width'],self.widget['Button_peakfit']])
        

     # -----assemble visual interface-----
    
    def __assemble_interface(self):
        
        self.widget['Label_PeakFit'] = wdg.HTML(value='<h3>Peak Fitting</h3>')

        self.interface = wdg.VBox([self.widget['Label_PeakFit'],
                                   wdg.HBox([self.widgetbox['addpeak'],
                                            self.widgetbox['fittedparams']]),
                                            self.widgetbox['boundpeak']]) 
        
    
    

    #------------------  Callback  helpers ----------

    def __newpeak_label(self,option_list):
        peak_label = 'New peak'
        peak_count = 1
        while peak_label in option_list:
            peak_label = 'New peak ' + str(peak_count)
            peak_count +=1
        return peak_label  


    def update_peakfit_status(self):
        parametrized_peaks = [key for key in self.input_peaks.keys() if (key != '--') and (not key.startswith('New peak'))]
        if len(parametrized_peaks) < 1:
            self.widget['Button_peakfit'].disabled = True
        else:
            self.widget['Button_peakfit'].disabled = False


    # ---------------------- Callbacks ------------------


    def callback_add_peak(self, _):
        new_label = self.__newpeak_label(list(self.widget['Select_peak'].options)) #generate non-repeating label from old options
        self.input_peaks.update({new_label:{'Bounds':[],'Width':0}})
        new_options = list(self.input_peaks.keys())
        new_options.sort()
        self.widget['Select_peak'].options = new_options
        self.widget['Select_peak'].value = self.widget['Select_peak'].options[-1] 

        self.update_peakfit_status()



    def callback_remove_peak(self, _):
        if self.widget['Select_peak'].value == '--':
            pass
        else:
            self.input_peaks.pop(self.widget['Select_peak'].value)
            new_options = list(self.input_peaks.keys())
            new_options.sort()
            self.widget['Select_peak'].options = new_options

        self.update_peakfit_status()


      
    def callback_relabel_peak(self,_):
        if self.widget['Select_peak'].value == '--':
            pass
        else:
            self.input_peaks.pop(self.widget['Select_peak'].value) #delete key with old name
            new_label = 'Bounds: {:.0f} - {:.0f} | Witdh: {:.0f}'.format(self.widget['Range_bounds'].value[0],self.widget['Range_bounds'].value[1],self.widget['Slider_width'].value)
            self.input_peaks.update({new_label:{'Bounds':self.widget['Range_bounds'].value,'Width':self.widget['Slider_width'].value}})
            new_options = list(self.input_peaks.keys())
            new_options.sort()
            self.widget['Select_peak'].options = new_options
            self.widget['Select_peak'].value = new_label
        
        self.update_peakfit_status()



    def callback_update_widgets(self, _):
        if self.widget['Select_peak'].value == '--' or self.widget['Select_peak'].value.startswith('New peak'):
            pass
        else:
            #Get current values before changing widget values. Once widget values change, the relabel_peak function runs
            current_bounds, current_width = self.input_peaks[self.widget['Select_peak'].value].values()
            self.widget['Range_bounds'].value = current_bounds
            self.widget['Slider_width'].value = current_width

            
    #------------------------- API ------------------------------------

    def set_bound_limits(self, bound_limits, n_datapoints):
        interval = bound_limits[1]-bound_limits[0]
        self.widget['Range_bounds'].min = bound_limits[0]
        self.widget['Range_bounds'].max = bound_limits[1]        
        self.widget['Range_bounds'].step = 2*interval/n_datapoints
        self.widget['Range_bounds'].value = [bound_limits[0]+0.25*interval,bound_limits[0]+0.75*interval]
        

    def set_width_limits(self, bound_limits, n_datapoints):
        interval = bound_limits[1]-bound_limits[0]
        self.widget['Slider_width'].min = 2*interval/n_datapoints
        self.widget['Slider_width'].max = 0.25*interval
        self.widget['Slider_width'].step = 2*interval/n_datapoints
        self.widget['Slider_width'].value = 0.25*interval + bound_limits[0]

    
    def clear_peaks(self):
        self.input_peaks = {'--':{}}
        self.widget['Select_peak'].options = ['--']
        self.widget['Select_peak'].value = '--'
        self.update_peakfit_status()

    @property    
    def inputs(self):
        list_bounds, list_widths = [],[]
        for peak_label, peak_params in self.input_peaks.items():
            if (peak_label != '--') and (not peak_label.startswith('New peak')):
                list_bounds.append(peak_params['Bounds'])
                list_widths.append(peak_params['Width'])

        summary = {'Bounds':list_bounds}
        summary.update({'Widths':list_widths})
        # summary.update({'Peak search':{key:value for key, value in self.input_peaks.items() if (key != '--') and (not key.startswith('New peak'))}})
        summary.update({'Lineshape':self.widget['Dropdown_lineshape'].value})

        return summary

    

    #---------------------- Events ---------------------------------

    def __events(self):
        self.widget['Button_add'].on_click(self.callback_add_peak)
        self.widget['Button_remove'].on_click(self.callback_remove_peak)
        self.widget['Range_bounds'].observe(self.callback_relabel_peak, names='value')
        self.widget['Slider_width'].observe(self.callback_relabel_peak, names='value')
        self.widget['Select_peak'].observe(self.callback_update_widgets, names='value')

    

    def render_parameter_table(self,spectrum):

        self.widget['Out_fitted_params'].clear_output()


        if spectrum.metadata['Fitting success']:

            peak_parameters = {'Center':[], 'Height':[], 'Width':[]}
            fitted_parameters_keys = list(spectrum.metadata['Fitted parameters'].keys())
            fitted_parameters_keys.sort()

            for key in fitted_parameters_keys:
                if key.startswith('p'):
                    peak_parameters['Center'].append(spectrum.metadata['Fitted parameters'][key])
                elif key.startswith('h'):
                    peak_parameters['Height'].append(spectrum.metadata['Fitted parameters'][key])
                elif key.startswith('w'):
                    peak_parameters['Width'].append(spectrum.metadata['Fitted parameters'][key])

            with self.widget['Out_fitted_params']:
                display(pd.DataFrame(peak_parameters, columns = list(peak_parameters.keys())).T)

        else:
            with self.widget['Out_fitted_params']:
                display(wdg.HTML(value="""<p style="color:Tomato;"> The fitting did not converge. Try:</p> 
                                            <ul style="color:Tomato;">
                                            <li>Changing the lineshape</li>
                                            <li>Improving the width guesses</li>
                                            <li>Modifying the peak bounds</li>                                            
                                            <li>Narrowing the trim range</li>                                            
                                            </ul>"""))


