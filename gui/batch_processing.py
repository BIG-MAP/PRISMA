# © Copyright 2021, PRISMA’s Authors

import ipywidgets as wdg
from zipfile import ZipFile
import base64



class BatchProcessing:
    def __init__(self):
        #gui attributes
        self.interface = None
        self.widget = {}
        self.widgetbox = {}
        #build gui panels
        self.__buildbox_parameters()
        self.__buildbox_run()
        self.__assemble_interface()

    def __buildbox_parameters(self):
        self.widget['HTML_batchparams'] = wdg.HTML(value="<h4>Review Parameters </h4>")

        self.widgetbox['batchparams'] = self.widget['HTML_batchparams']
        self.widgetbox['batchparams'].layout = wdg.Layout(width='30%')

    def __buildbox_run(self):
        self.widget['Button_run'] = wdg.Button(description='Run Batch Processing', 
                                               icon='play', disabled = True, 
                                               style = {'description_width': 'initial'})
        
        self.widget['HTML_log'] = wdg.HTML(value='')
                                               
        self.widget['Label_results'] = wdg.HTML(value="<h4>Download results </h4>")

        self.widget['Buttons_download'] = wdg.HTML(value='')

        self.widgetbox['batchrun'] = wdg.VBox([self.widget['Button_run'],
                                                self.widget['HTML_log'],
                                               self.widget['Label_results'],
                                               self.widget['Buttons_download']])        

    # -----assemble visual interface-----    
    def __assemble_interface(self):
        self.interface = wdg.HBox([self.widgetbox['batchparams'],self.widgetbox['batchrun']])


    # ----------- Auxiliary FUnctions --------------- 


    def aux_disable_donwloads(self):
        self.widget['Buttons_download'].value = ''


    def aux_enable_batch_processing(self):
        self.widget['Button_run'].disabled = False


    def aux_disable_batch_processing(self):
        self.widget['Button_run'].disabled = True


    def aux_prepare_payload(self):
        pass

    def aux_disable_input_summary(self):
        self.widget['HTML_batchparams'].value = '<h5>Review Parameters </h5>'


    def aux_render_input_summary(self, inputs):
        html_text = '<h4>Review Parameters </h4>'
        for key in inputs.keys():
            html_text += '<p><u>{}</u></p><p>'.format(key)
        #parent keys: Files, Baseline, Peakfit
            html_text += '</p><p>'.join(['{}: {}'.format(key,value) for key,value in inputs[key].items() if key != 'Spectra names']) #dont show long list of spectra names
    
        self.widget['HTML_batchparams'].value = html_text


    def update_processing_paramaters(self, parameters = None):
        if not parameters:
            self.aux_disable_batch_processing()
            self.aux_disable_donwload()
            self.aux_disable_input_summary()
        else:
            self.aux_render_input_summary(parameters)
            self.aux_enable_batch_processing()


    def prepare_payload_downloads(self, payload):
        if not payload:
            pass

        else:
            html_text = ''

            for payload_type, data_string in payload.items():
                b64 = base64.b64encode(data_string.encode())
                encoded_string = b64.decode()
                html_text += """<a download="{filename}.csv" href="data:text/csv;base64,{payload}" download> 
                            <button class="p-Widget jupyter-widgets jupyter-button widget-button">{filename}</button>
                            </a>""".format(filename=payload_type,payload=encoded_string) # see MIME Types to check how to download different types of files
        
            self.widget['Buttons_download'].value = html_text
            


    def update_processing_log(self, log='start'):
        processing_start_msg = """<p style="color:DodgerBlue;">Processing...</p>"""

        if log == 'start':
            self.widget['HTML_log'].value = processing_start_msg

        elif log == 'multiple energy axes':
            self.widget['HTML_log'].value = """<p style="color:Tomato;">Batch processing not supported for spectra that do not share a common energy (wavenumber, wavelenght, etc) axis.</p>
                                               <p style="color:Tomato;">Analizying and downloading individual spectra is still possible from the "Explore Processing Parameters" tab</p>"""

        elif isinstance(log,list):
            for label in log:
                processing_start_msg += """<p style="color:Tomato;">Fitting on "{}" did not converge</p>""".format(label)
            self.widget['HTML_log'].value = processing_start_msg + """<p style="color:MediumSeaGreen;">Processing finished</p>"""
