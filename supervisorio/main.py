from kivy.app import App 
from mainwidget import MainWidget
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty


class MainApp(App):

    def build(self):
       
        self._widget = MainWidget(scan_time = 500, server_ip = '192.168.0.14', server_port = 502,db_path = "db\scada.db",
        modbus_CLP = 
        [
            {'tipo': '4X', 'address': 710, 'bit': None, 'tag': 'co_pressostato', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 712, 'bit': 0, 'tag': 'co_xv1', 'div': 1, 'hist_graph': 1, 'grandeza': ' ', 'limits': [0, 2]},
            {'tipo': '4X', 'address': 712, 'bit': 1, 'tag': 'co_xv2', 'div': 1, 'hist_graph': 1, 'grandeza': ' ', 'limits': [0, 2]},
            {'tipo': '4X', 'address': 712, 'bit': 2, 'tag': 'co_xv3', 'div': 1, 'hist_graph': 1, 'grandeza': ' ', 'limits': [0, 2]},
            {'tipo': '4X', 'address': 712, 'bit': 3, 'tag': 'co_xv4', 'div': 1, 'hist_graph': 1, 'grandeza': ' ', 'limits': [0, 2]},
            {'tipo': '4X', 'address': 712, 'bit': 4, 'tag': 'co_xv5', 'div': 1, 'hist_graph': 1, 'grandeza': ' ', 'limits': [0, 2]},
            {'tipo': '4X', 'address': 712, 'bit': 5, 'tag': 'co_xv6', 'div': 1, 'hist_graph': 1, 'grandeza': ' ', 'limits': [0, 2]},
            {'tipo': 'FP', 'address': 706, 'bit': None, 'tag': 'co_temp_carc', 'div': 10, 'hist_graph': 1, 'grandeza': 'C', 'limits': [0, 100]},
            {'tipo': 'FP', 'address': 714, 'bit': None, 'tag': 'co_pressao', 'div': 1, 'hist_graph': 1, 'grandeza': 'kgf/cm3', 'limits': [0, 5]},
            {'tipo': 'FP', 'address': 716, 'bit': None, 'tag': 'co_fit02', 'div': 1, 'hist_graph': 1, 'grandeza': 'Nm3/min', 'limits': [0, 15]},
            {'tipo': '4X', 'address': 830, 'bit': None, 'tag': 'co_frequencia', 'div': 100, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 840, 'bit': None, 'tag': 'co_corrente_r', 'div': 10, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 841, 'bit': None, 'tag': 'co_corrente_s', 'div': 10, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 842, 'bit': None, 'tag': 'co_corrente_t', 'div': 10, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 847, 'bit': None, 'tag': 'co_tensao_rs', 'div': 10, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 848, 'bit': None, 'tag': 'co_tensao_st', 'div': 10, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 849, 'bit': None, 'tag': 'co_tensao_tr', 'div': 10, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 863, 'bit': None, 'tag': 'co_aparente_total', 'div': 1, 'hist_graph': 1, 'grandeza': 'KVA', 'limits': [0, 2500]},
            {'tipo': '4X', 'address': 871, 'bit': None, 'tag': 'co_fp_total', 'div': 1000, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 886, 'bit': None, 'tag': 'co_status_ats48', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 888, 'bit': None, 'tag': 'co_status_atv31', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 890, 'bit': None, 'tag': 'co_status_tesys', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 1316, 'bit': None, 'tag': 'co_ats48', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 1317, 'bit': None, 'tag': 'co_ats48_acc', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 1318, 'bit': None, 'tag': 'co_ats48_dcc', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 1319, 'bit': None, 'tag': 'co_tesys', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 1324, 'bit': None, 'tag': 'co_sel_driver', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 1312, 'bit': None, 'tag': 'co_atv31', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]},
            {'tipo': '4X', 'address': 1328, 'bit': 1, 'tag': 'co_habilita', 'div': 1, 'hist_graph': 0, 'grandeza': ' ', 'limits': [0, 0]}
            ]
        )
        Window.size = (1150, 712)
        return self._widget
    
    def on_stop(self):
        '''
        Metodo executado quando a aplicacao e fechada
        '''
        self._widget.stopRefresh()
        
    

if __name__ == '__main__':
    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(), rulesonly = True)
    Builder.load_string(open("popups.kv", encoding="utf-8").read(), rulesonly = True)
    MainApp().run()