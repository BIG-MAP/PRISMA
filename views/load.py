import ipywidgets as wdg
import base64


class ViewLoad:

    def __init__(self, parsers):
        self.parsers = parsers
        self.interface = None
        self.widgetbox = {}
        self.widget = {}
        #build subapp
        self.__buildbox()
        self.__buildbox_donwload()
        self.__assemble_interface()
        self.__events()

         
 
    def __buildbox(self):

        default_parser = list(self.parsers.keys())[0]        
        self.widget['Ddn_parser'] = wdg.Dropdown(options=self.parsers.keys(), value=default_parser, description='Parser')

        #keeping the default '--' option avoids changing the widgets value when updating the options, and so avoids triggering another callback
        self.widget['Sct_spectra'] = wdg.Select(options=['--'], value='--') 

        #FileUpload.value:
        #'filename1'
        #--'metadata': {name, size, type, lastModified}
        #--'content': b'230/t555/n231/t5555.....  
        self.widget['Fld_spectra'] = wdg.FileUpload(description='Load spectra', icon='file-o', 
                                                    accept =   self.parsers[default_parser]['file format'], 
                                                    multiple = self.parsers[default_parser]['multiple files'])                                                    
   
        
        self.widgetbox['load_spectra'] = wdg.VBox([self.widget['Ddn_parser'],self.widget['Fld_spectra'],self.widget['Sct_spectra']])
        self.widgetbox['load_spectra'].layout = {'display':'flex','flex_flow':'column','align_content': 'center'} 


    def __buildbox_donwload(self):
        empty_string = 'no data'
        b64 = base64.b64encode(empty_string.encode())
        empty_payload = b64.decode()
        self.widget['Html_donwload'] = wdg.HTML(value="""<a download="{filename}" href="data:text/csv;base64,{payload}" download>
                                                <button class="p-Widget jupyter-widgets jupyter-button widget-button">Donwload spectrum</button>
                                                </a>""".format(filename='empty.csv', payload=empty_payload)) 
               

  
    def __assemble_interface(self):
        label_widget = wdg.HTML(value='<h3>Manage Spectra</h3>')
        self.interface = wdg.VBox([label_widget,self.widgetbox['load_spectra'], self.widget['Html_donwload']])


# ----------- CALLBACKS ----------------

    def __callback_load_mode(self,value):
        self.widget['Fld_spectra'].multiple = self.parsers[value['new']]['multiple files']
        self.widget['Fld_spectra'].accept = self.parsers[value['new']]['file format']


# ----------- EVENTS ----------------

    def __events(self):
        self.widget['Ddn_parser'].observe(self.__callback_load_mode,names='value')



# ---------- API ----------
    def display_spectra_names(self,names):
        self.widget['Sct_spectra'].options = ['--'] + names


    def update_download_button(self, filename = 'empty.csv' , string = 'no data'):
        b64 = base64.b64encode(string.encode())
        payload = b64.decode()

        self.widget['Html_donwload'].value = """<a download="{filename}_processed.csv" href="data:text/csv;base64,{payload}" download>
                                                <button class="p-Widget jupyter-widgets jupyter-button widget-button">Donwload spectrum</button>
                                                </a>""".format(filename=filename, payload=payload)



    @property
    def inputs(self):
        user_inputs = {}
        user_inputs['Parser'] = self.widget['Ddn_parser'].value

        if not self.widget['Fld_spectra'].value:
            pass
        else:
            loaded_filenames = [filename for filename in self.widget['Sct_spectra'].options if filename != '--']
            user_inputs['Number of spectra'] = len(loaded_filenames)

        return user_inputs


    @property
    def current_upload(self):
        if not self.widget['Fld_spectra'].value: 
            return None
        else:
            return self.widget['Fld_spectra'].value


    @property
    def current_parser_name(self):
        return self.widget['Ddn_parser'].value

    @property
    def current_spectrum(self):
        if self.widget['Sct_spectra'].value == '--':
            return None 
        else:
            return self.widget['Sct_spectra'].value




