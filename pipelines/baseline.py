import ipywidgets as wdg
import pandas as pd
import functools 

from views.baselines import ViewBaselineAls
from views.load import ViewLoad
from views.plots import PlotBaseline, PlotIntensities

from models.preprocessing import Preprocessing
from models.baselines import Baselines
from models.parsers import Parsers





class BaselineCorrection:

    def __init__(self):
        self.interface = None
        self.spectra = {}

        self.view_load_subapps()
        self.view_assemble_interface()
        self.control_events()



    def view_load_subapps(self):
        self.subapps = {'Load':ViewLoad(Parsers().available_parsers),
                        'Baseline':ViewBaselineAls(),
                        'Plot Baseline': PlotBaseline(x_label='Raman shift [cm-1]',y_label='Counts [a.u.]',title='Original'),
                        'Plot Intensities':PlotIntensities(x_label='Raman shift [cm-1]',y_label='Counts [a.u.]',title='Baseline corrected')}



    def view_assemble_interface(self):
        plot_box = wdg.HBox([self.subapps['Plot Baseline'].interface, 
                            self.subapps['Plot Intensities'].interface])

        load_baseline_box = wdg.HBox([self.subapps['Load'].interface, 
                            self.subapps['Baseline'].interface])

        self.interface = wdg.VBox([load_baseline_box, plot_box])
  

    
    @property
    def inputs(self):
        user_inputs = {}

        user_inputs['Files'] = self.subapps['Load'].inputs
        user_inputs['Baseline'] = self.subapps['Baseline'].inputs

        return user_inputs



    # ------------------- Auxiliary functions -------------

    def aux_get_payload_from_file_upload(self, upload):
        parser_name = self.subapps['Load'].current_parser_name

        if Parsers().available_parsers[parser_name]['multiple files']:
            payload =  {key:value['content'] for key, value in upload.items()}
        else: 
            filename = list(upload.keys())[0]
            payload = upload[filename]['content'] 

        return payload, parser_name



    def aux_process_spectrum(self,label):
        baseline_parameters = self.subapps['Baseline'].inputs

        trimmed_spectrum = Preprocessing().trimming(self.spectra[label]['root'], 
                                                    within=baseline_parameters['Trim'])
        self.spectra[label]['processed'] = Baselines().asymmetric_least_squares(trimmed_spectrum, 
                                                                                log_p=baseline_parameters['Log p'], 
                                                                                log_lambda=baseline_parameters['Log lambda'])


    
    def aux_refresh_plots(self,label):
        self.subapps['Plot Baseline'].update_marks(self.spectra[label]['root'],
                                                   self.spectra[label]['processed'])
        self.subapps['Plot Intensities'].update_marks(self.spectra[label]['processed'])



    def aux_update_download_payload(self, label):
        individual_dataframes = [pd.DataFrame(self.spectra[label]['root'].counts, columns=['Original'], index=self.spectra[label]['root'].energies),
                                 pd.DataFrame(self.spectra[label]['processed'].counts, columns=['Processed'], index=self.spectra[label]['processed'].energies)]
        
        spectrum_dataframe = functools.reduce(lambda  left,right: pd.merge(left,right, left_index=True, right_index=True, how='outer'), individual_dataframes)
        spectrum_csv = spectrum_dataframe.to_csv(sep=',')

        self.subapps['Load'].update_download_button(filename=label,string=spectrum_csv)



    # ------------------ CALLBACKS -------------------------
    def callback_upload_spectra(self, button_upload):
        payload, parser_name = self.aux_get_payload_from_file_upload(button_upload['new'])   

        self.spectra, self.spectra_metadata = Parsers().parse(payload, parser_name)
        list_of_spectra = list(self.spectra.keys())
        list_of_spectra.sort()

        self.subapps['Load'].display_spectra_names(list_of_spectra)
        self.subapps['Baseline'].set_trim_limits(self.spectra_metadata['energy_limits'])



    def callback_update_processing(self,_):
        current_spectrum_label = self.subapps['Load'].current_spectrum
 
        if current_spectrum_label == None:
            pass
        else:
            self.aux_process_spectrum(current_spectrum_label)
            self.aux_refresh_plots(current_spectrum_label)
            self.aux_update_download_payload(current_spectrum_label)


            
    # --------------------EVENTS-------------------

    def control_events(self):
        self.subapps['Load'].widget['Fld_spectra'].observe(self.callback_upload_spectra, names='value')
        self.subapps['Load'].widget['Sct_spectra'].observe(self.callback_update_processing, names='value')
        self.subapps['Baseline'].widget['Range_trim'].observe(self.callback_update_processing, names='value')
        self.subapps['Baseline'].widget['Slider_baseline_p'].observe(self.callback_update_processing, names='value')
        self.subapps['Baseline'].widget['Slider_baseline_l'].observe(self.callback_update_processing, names='value')


    # --------------------API------------------- 

    def batch_processing(self):        
        baseline_parameters = self.subapps['Baseline'].inputs

        if not self.spectra:
            pass
        else:
            for label in self.spectra.keys():
                trimmed_spectrum = Preprocessing().trimming(self.spectra[label]['root'], 
                                                            within=baseline_parameters['Trim'])
                self.spectra[label]['processed'] = Baselines().asymmetric_least_squares(trimmed_spectrum, 
                                                                                        log_p=baseline_parameters['Log p'], 
                                                                                        log_lambda=baseline_parameters['Log lambda'])


    def export_batch_processing_payloads(self):
        label_first_spectrum = list(self.spectra.keys())[0] #all spectra share same energy vector. Enough to take the first one to not iterate over all
        csv_payload = {}

        csv_payload['Processed_spectra']  = pd.DataFrame(data = {label: value['processed'].counts for label, value in self.spectra.items()}, 
                                                        columns = list(self.spectra.keys()), 
                                                        index = self.spectra[label_first_spectrum]['processed'].energies).to_csv(sep=',')

        metadata_dict = self.subapps['Load'].inputs
        metadata_dict.update(self.subapps['Baseline'].inputs)
        csv_payload['Metadata'] = pd.DataFrame({'Parameter':list(metadata_dict.keys()),'Value':list(metadata_dict.values())}).to_csv(sep=',')

        return csv_payload