# © Copyright 2021, PRISMA’s Authors

import ipywidgets as wdg


class PipelineMenu:

        icons = {'baseline':'./static/icon_baseline.png',
            'baseline_peakfit':'./static/icon_baseline_fit.png',
            'baseline_corr':'./static/icon_baseline_corr.png',
            'peakfit':'./static/icon_fit.png',
            'corr':'./static/icon_corr.png'}

        icon_height = 100
        icon_width = 150
        icon_width_wide = 300
        subcontainers = {}

        def __init__(self):
            self.widget = {}
            self.widgetbox = {}
            self.interface = None
            self.image = {}
  
            self.__read_images()
            self.__buildbox_baseline()
            self.__buildbox_baseline_peakfit()
            self.__buildbox_peakfit()
            self.__assemble_interface()



        def __read_images(self):
            for k, v in PipelineMenu.icons.items():
                with open(v, 'rb') as file:
                    self.image[k] = file.read()


        def __buildbox_baseline(self):            

            self.widget['Img_baseline'] = wdg.Image(value=self.image['baseline'], format = 'png',
                                                width=PipelineMenu.icon_width, height = PipelineMenu.icon_height)
            self.widget['Btn_baseline'] = wdg.Button(icon='play')
            self.widgetbox['baseline'] = wdg.VBox([self.widget['Img_baseline'],self.widget['Btn_baseline']])


        def __buildbox_baseline_peakfit(self):            

            self.widget['Img_baseline_peakfit'] = wdg.Image(value=self.image['baseline_peakfit'], format = 'png',
                                                width=PipelineMenu.icon_width_wide, height = PipelineMenu.icon_height)
            self.widget['Btn_baseline_peakfit'] = wdg.Button(icon='play')
            self.widgetbox['baseline_peakfit'] = wdg.VBox([self.widget['Img_baseline_peakfit'],self.widget['Btn_baseline_peakfit']])


        def __buildbox_peakfit(self):

            self.widget['Img_peakfit'] = wdg.Image(value=self.image['peakfit'], format = 'png',
                                                width=PipelineMenu.icon_width, height = PipelineMenu.icon_height)
            self.widget['Btn_peakfit'] = wdg.Button(icon='play')
            self.widgetbox['peakfit'] =  wdg.VBox([self.widget['Img_peakfit'],self.widget['Btn_peakfit']])



        def __assemble_interface(self):
            self.interface =  wdg.VBox([wdg.HBox([self.widgetbox['baseline'],
                                        self.widgetbox['peakfit']]),
                                        self.widgetbox['baseline_peakfit']])

