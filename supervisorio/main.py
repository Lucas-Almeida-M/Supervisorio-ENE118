from kivy.app import App 
from mainwidget import MainWidget
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty


class MainApp(App):

    def build(self):
       
        self._widget = MainWidget(scan_time = 500, server_ip = '192.168.0.14', server_port = 502,
        modbus_CLP = 
        [
            {'tipo': '4X', 'address': 708, 'bit': None, 'tag': 'co_tipo_motor', 'div': 1},
            {'tipo': '4X', 'address': 710, 'bit': None, 'tag': 'co_pressostato', 'div': 1},
            {'tipo': '4X', 'address': 712, 'bit': 0   , 'tag': 'co_xv1', 'div': 1},
            {'tipo': '4X', 'address': 712, 'bit': 1   , 'tag': 'co_xv2', 'div': 1},
            {'tipo': '4X', 'address': 712, 'bit': 2   , 'tag': 'co_xv3', 'div': 1},
            {'tipo': '4X', 'address': 712, 'bit': 3   , 'tag': 'co_xv4', 'div': 1},
            {'tipo': '4X', 'address': 712, 'bit': 4   , 'tag': 'co_xv5', 'div': 1},
            {'tipo': '4X', 'address': 712, 'bit': 5   , 'tag': 'co_xv6', 'div': 1},
            {'tipo': '4X', 'address': 714, 'bit': None, 'tag': 'co_pv_pid', 'div': 1},
            {'tipo': '4X', 'address': 722, 'bit': None, 'tag': 'co_status_pid', 'div': 1},
            {'tipo': 'FP', 'address': 700, 'bit': None, 'tag': 'co_temp_r', 'div': 10},
            {'tipo': 'FP', 'address': 702, 'bit': None, 'tag': 'co_temp_s', 'div': 10},
            {'tipo': 'FP', 'address': 704, 'bit': None, 'tag': 'co_temp_t', 'div': 10},
            {'tipo': 'FP', 'address': 706, 'bit': None, 'tag': 'co_temp_carc', 'div': 10},
            {'tipo': 'FP', 'address': 714, 'bit': None, 'tag': 'co_pressao', 'div': 1},
            {'tipo': 'FP', 'address': 716, 'bit': None, 'tag': 'co_fit02', 'div': 1},
            {'tipo': 'FP', 'address': 718, 'bit': None, 'tag': 'co_fit03', 'div': 1},
            {'tipo': 'FP', 'address': 814, 'bit': None, 'tag': 'co_mv_le', 'div': 1},
            {'tipo': '4X', 'address': 800, 'bit': None, 'tag': 'co_thd_tensao_rn', 'div': 10},
            {'tipo': '4X', 'address': 801, 'bit': None, 'tag': 'co_thd_tensao_sn', 'div': 10},
            {'tipo': '4X', 'address': 802, 'bit': None, 'tag': 'co_thd_tensao_tn', 'div': 10},
            {'tipo': '4X', 'address': 804, 'bit': None, 'tag': 'co_thd_tensao_rs', 'div': 10},
            {'tipo': '4X', 'address': 805, 'bit': None, 'tag': 'co_thd_tensao_st', 'div': 10},
            {'tipo': '4X', 'address': 806, 'bit': None, 'tag': 'co_thd_tensao_tr', 'div': 10},
            {'tipo': '4X', 'address': 830, 'bit': None, 'tag': 'co_frequencia', 'div': 100},
            {'tipo': '4X', 'address': 840, 'bit': None, 'tag': 'co_corrente_r', 'div': 10},
            {'tipo': '4X', 'address': 841, 'bit': None, 'tag': 'co_corrente_s', 'div': 10},
            {'tipo': '4X', 'address': 842, 'bit': None, 'tag': 'co_corrente_t', 'div': 10},
            {'tipo': '4X', 'address': 843, 'bit': None, 'tag': 'co_corrente_n', 'div': 10},
            {'tipo': '4X', 'address': 845, 'bit': None, 'tag': 'co_corrente_media', 'div': 10},
            {'tipo': '4X', 'address': 847, 'bit': None, 'tag': 'co_tensao_rs', 'div': 10},
            {'tipo': '4X', 'address': 848, 'bit': None, 'tag': 'co_tensao_st', 'div': 10},
            {'tipo': '4X', 'address': 849, 'bit': None, 'tag': 'co_tensao_tr', 'div': 10},
            {'tipo': '4X', 'address': 852, 'bit': None, 'tag': 'co_ativa_r', 'div': 1},
            {'tipo': '4X', 'address': 853, 'bit': None, 'tag': 'co_ativa_s', 'div': 1},
            {'tipo': '4X', 'address': 854, 'bit': None, 'tag': 'co_ativa_t', 'div': 1},
            {'tipo': '4X', 'address': 855, 'bit': None, 'tag': 'co_ativa_total', 'div': 1},
            {'tipo': '4X', 'address': 856, 'bit': None, 'tag': 'co_reativa_r', 'div': 1},
            {'tipo': '4X', 'address': 857, 'bit': None, 'tag': 'co_reativa_s', 'div': 1},
            {'tipo': '4X', 'address': 858, 'bit': None, 'tag': 'co_reativa_t', 'div': 1},
            {'tipo': '4X', 'address': 859, 'bit': None, 'tag': 'co_reativa_total', 'div': 1},
            {'tipo': '4X', 'address': 860, 'bit': None, 'tag': 'co_aparente_r', 'div': 1},
            {'tipo': '4X', 'address': 861, 'bit': None, 'tag': 'co_aparente_s', 'div': 1},
            {'tipo': '4X', 'address': 862, 'bit': None, 'tag': 'co_aparente_t', 'div': 1},
            {'tipo': '4X', 'address': 863, 'bit': None, 'tag': 'co_aparente_total', 'div': 1},
            {'tipo': '4X', 'address': 868, 'bit': None, 'tag': 'co_fp_r', 'div': 1000},
            {'tipo': '4X', 'address': 869, 'bit': None, 'tag': 'co_fp_s', 'div': 1000},
            {'tipo': '4X', 'address': 870, 'bit': None, 'tag': 'co_fp_t', 'div': 1000},
            {'tipo': '4X', 'address': 871, 'bit': None, 'tag': 'co_fp_total', 'div': 1000},
            {'tipo': '4X', 'address': 874, 'bit': None, 'tag': 'co_thd_corrente_r', 'div': 10},
            {'tipo': '4X', 'address': 875, 'bit': None, 'tag': 'co_thd_corrente_s', 'div': 10},
            {'tipo': '4X', 'address': 876, 'bit': None, 'tag': 'co_thd_corrente_t', 'div': 10},
            {'tipo': '4X', 'address': 877, 'bit': None, 'tag': 'co_thd_corrente_n', 'div': 10},
            {'tipo': '4X', 'address': 886, 'bit': None, 'tag': 'co_status_ats48', 'div': 1},
            {'tipo': '4X', 'address': 888, 'bit': None, 'tag': 'co_status_atv31', 'div': 1},
            {'tipo': '4X', 'address': 890, 'bit': None, 'tag': 'co_status_tesys', 'div': 1},
            {'tipo': 'FP', 'address': 884, 'bit': None, 'tag': 'co_encoder', 'div': 1},
            {'tipo': '4X', 'address': 1216, 'bit': None, 'tag': 'co_indica_driver', 'div': 1},
            {'tipo': '4X', 'address': 1316, 'bit': None, 'tag': 'co_ats48', 'div': 1},
            {'tipo': '4X', 'address': 1317, 'bit': None, 'tag': 'co_ats48_acc', 'div': 1},
            {'tipo': '4X', 'address': 1318, 'bit': None, 'tag': 'co_ats48_dcc', 'div': 1},
            {'tipo': '4X', 'address': 1319, 'bit': None, 'tag': 'co_tesys', 'div': 1},
            {'tipo': '4X', 'address': 1324, 'bit': None, 'tag': 'co_sel_driver', 'div': 1},
            {'tipo': '4X', 'address': 1332, 'bit': None, 'tag': 'co_sel_pid', 'div': 1},
            {'tipo': '4X', 'address': 1204, 'bit': None, 'tag': 'co_demanda_anterior', 'div': 10},
            {'tipo': '4X', 'address': 1205, 'bit': None, 'tag': 'co_demanda_atual', 'div': 10},
            {'tipo': '4X', 'address': 1206, 'bit': None, 'tag': 'co_demanda_media', 'div': 10},
            {'tipo': '4X', 'address': 1207, 'bit': None, 'tag': 'co_demanda_pico', 'div': 10},
            {'tipo': '4X', 'address': 1208, 'bit': None, 'tag': 'co_demanda_prevista', 'div': 10},
            {'tipo': '4X', 'address': 1210, 'bit': None, 'tag': 'co_energia_ativa', 'div': 1},
            {'tipo': '4X', 'address': 1212, 'bit': None, 'tag': 'co_energia_reativa', 'div': 1},
            {'tipo': '4X', 'address': 1214, 'bit': None, 'tag': 'co_energia_aparente', 'div': 1},
            {'tipo': '4X', 'address': 1312, 'bit': None, 'tag': 'co_atv31', 'div': 1},
            {'tipo': '4X', 'address': 1313, 'bit': None, 'tag': 'co_atv31_velocidade', 'div': 10},
            {'tipo': '4X', 'address': 1328, 'bit': 1   , 'tag': 'co_habilita', 'div': 1},
            {'tipo': 'FP', 'address': 1302, 'bit': None, 'tag': 'co_sp_pid', 'div': 1},
            {'tipo': 'FP', 'address': 1304, 'bit': None, 'tag': 'co_p', 'div': 1},
            {'tipo': 'FP', 'address': 1306, 'bit': None, 'tag': 'co_i', 'div': 1},
            {'tipo': 'FP', 'address': 1308, 'bit': None, 'tag': 'co_d', 'div': 1},
            {'tipo': 'FP', 'address': 1310, 'bit': None, 'tag': 'co_mv_escreve', 'div': 1},
            {'tipo': 'FP', 'address': 1314, 'bit': None, 'tag': 'co_pv_pid', 'div': 1},
            {'tipo': 'FP', 'address': 1420, 'bit': None, 'tag': 'co_torque', 'div': 1}                   
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