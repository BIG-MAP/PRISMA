import ipywidgets as wdg



class BatchProcessing:
    def __init__(self):
        #gui attributes
        self.interface = None
        self.widget = {}
        self.widget_box = {}
        #build gui panels
        self.__buildbox_batchparams()
        self.__buildbox_run()
        self.__assemble_interface()

    def __buildbox_batchparams(self):
        self.widget['HTML_batchparams'] = wdg.HTML(value="<h5>Review Parameters </h5>")
        self.widget_box['batchparams'] = wdg.VBox([self.widget['HTML_batchparams']])
        
    def __buildbox_run(self):
        self.widget['Button_run'] = wdg.Button(description='Run Batch Processing', icon='play', disabled = True)
        self.widget_box['run'] = wdg.VBox([self.widget['Button_run']])
        
    # -----assemble visual interface-----    
    def __assemble_interface(self):
        self.interface = wdg.VBox([self.widget_box['batchparams'],self.widget_box['run']])

        
    def summarize_current_inputs(self, inputs):
        if not inputs:
            self.widget['HTML_batchparams'].value = ''
        else:
            html_text = ''
            for key in inputs.keys():
                html_text += '<p><u>{}</u></p><p>'.format(key)
            #parent keys: Files, Baseline, Peakfit
                html_text += '</p><p>'.join(['{}: {}'.format(key,value) for key,value in inputs[key].items()])
        
            self.widget['HTML_batchparams'].value = html_text

    def enable_batch_processing(self):
        self.widget['Button_run'].disabled = False

    def disable_batch_processing(self):
        self.widget['Button_run'].disabled = True
        
