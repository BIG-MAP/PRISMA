import ipywidgets as wdg

from main.pipeline_menu import PipelineMenu
from main.batch_processing import BatchProcessing

from pipelines.baseline import BaselineCorrection
from pipelines.baseline_peakfit import BaselinePeakFitting
from pipelines.peakfit import PeakFitting




class Main:
    
    logo = './main/logo_draft1.png'

    title = 'PRISMA: An app for the analysis of spectra'

    sub_title = """<p><i>Eibar Flores, Technical University Denmark</i> </p>
                  <p>Cite this code: TBD</p>"""


    def __init__(self):
        self.widget = {}
        self.widgetbox = {}
        self.subapps = {}
        self.container = None
        self.interface = None

        self.__buildbox_heading()
        self.__buildbox_pipeline_menu()
        self.__buildbox_batch_processing()
        self.__assemble_interface()
        self.__events()


    def __buildbox_heading(self):
        logo_height = 200
        logo_width = 200 

        with open(Main.logo, 'rb') as file:
                image = file.read()

        self.widget['Img_logo'] = wdg.Image(value=image, format = 'png',
                                            width=logo_width, height = logo_height)
        self.widget['Html_title'] = wdg.HTML(value='<h2>{}</h2>'.format(Main.title))
        self.widget['Html_subtitle'] = wdg.HTML(value=Main.sub_title)

        self.widgetbox['heading'] = wdg.HBox([self.widget['Img_logo'],
                                            wdg.VBox([self.widget['Html_title'],
                                            self.widget['Html_subtitle']])])


    def __buildbox_pipeline_menu(self):
        self.subapps['pipeline_menu'] =  PipelineMenu()
        self.widgetbox['pipelines'] = self.subapps['pipeline_menu'].interface  


    def __buildbox_batch_processing(self):
        self.subapps['batch_processing'] =  BatchProcessing()
        self.widgetbox['batch_processing'] = self.subapps['batch_processing'].interface



    def __assemble_interface(self):
        self.container = wdg.Output()

        self.widget['accordion'] = wdg.Accordion(children=[self.widgetbox['pipelines'],self.container,self.widgetbox['batch_processing']])
        self.widget['accordion'].set_title(0,'Choose a Pipeline')
        self.widget['accordion'].set_title(1,'Explore Processing Parameters')
        self.widget['accordion'].set_title(2,'Apply Parameters to all Spectra')

        self.interface = wdg.VBox([self.widgetbox['heading'],self.widget['accordion']])


    def __pipeline_baseline(self,_):
        self.subapps['pipeline'] = BaselineCorrection()

        self.container.clear_output()
        with self.container:   
            display(self.subapps['pipeline'].interface)

        self.widget['accordion'].selected_index = 1


    def __pipeline_peakfit(self,_):
        self.subapps['pipeline'] = PeakFitting()

        self.container.clear_output()
        with self.container:   
            display(self.subapps['pipeline'].interface)

        self.widget['accordion'].selected_index = 1


    def __pipeline_baseline_peakfit(self,_):
        self.subapps['pipeline'] = BaselinePeakFitting()

        self.container.clear_output()
        with self.container:   
            display(self.subapps['pipeline'].interface)

        self.widget['accordion'].selected_index = 1


    def __update_batch_processing_parameters(self,_):    
        try:    
            self.subapps['batch_processing'].update_processing_paramaters(self.subapps['pipeline'].inputs)
        except KeyError:
            pass


    def __run_batch_processing(self, _):

        self.subapps['batch_processing'].update_processing_log(log='start')
        unsuccessful_fits = self.subapps['pipeline'].batch_processing()

        if unsuccessful_fits == 'multiple energy axes':
            self.subapps['batch_processing'].update_processing_log(log='multiple energy axes')

        else:
            csv_payloads = self.subapps['pipeline'].export_batch_processing_payloads()
            self.subapps['batch_processing'].prepare_payload_downloads(csv_payloads)
            self.subapps['batch_processing'].update_processing_log(log=unsuccessful_fits)


   


    def __events(self):
        self.subapps['pipeline_menu'].widget['Btn_baseline'].on_click(self.__pipeline_baseline)
        self.subapps['pipeline_menu'].widget['Btn_peakfit'].on_click(self.__pipeline_peakfit)
        self.subapps['pipeline_menu'].widget['Btn_baseline_peakfit'].on_click(self.__pipeline_baseline_peakfit)
        self.widget['accordion'].observe(self.__update_batch_processing_parameters,names='selected_index')
        self.subapps['batch_processing'].widget['Button_run'].on_click(self.__run_batch_processing)
