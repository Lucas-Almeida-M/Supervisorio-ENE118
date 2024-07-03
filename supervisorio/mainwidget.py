from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup, DataGraphPopup, motorPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread, Lock
from time import sleep
from datetime import datetime
import random
from timeseriesgraph import TimeSeriesGraph





class MainWidget (BoxLayout):
    """
    Widget principal da aplicação
    """
    _updateThread = None
    _updateWidgets = True
    _tags = {}
    _pressure = 0.5
    _max_points = 20
    _tags_with_graphs = ['co_pressao','co_fit03']

    def __init__(self, **kwargs):
        """
        construtor do widget principal
        """
        super().__init__()
        self._scan_time = kwargs.get('scan_time')
        self._serverIP = kwargs.get('server_ip')
        self._serverPort = kwargs.get('server_port')
        # self._ControlePopup = ControlePopup()
        self._modbusCLP = kwargs.get('modbus_CLP')
        self._modbusPopup = ModbusPopup(self._serverIP, self._serverPort)
        self._scanPopup = ScanPopup(scantime = self._scan_time)
        self._modbusClient = ModbusClient(host = self._serverIP, port = self._serverPort)
        self._lock = Lock()

        self._motorPopup = motorPopup()
        self._bar = self.ids.pressure_bar
        self._meas = {}
        self._meas ['timestamp'] = None
        self._meas ['values'] = {}

        for item in self._modbusCLP:
            tag = item.pop('tag')
            self._tags[tag] = item
            plot_color = (random.random(),random.random(),random.random(),1)
            self._tags[tag]['color'] = plot_color
        
        self._graph = {}
        
        self._graph[self._tags_with_graphs[0]] = (DataGraphPopup(self._max_points, self._tags[self._tags_with_graphs[0]]['color']))
        self._graph[self._tags_with_graphs[0]].title = 'Pressão'
        self._graph[self._tags_with_graphs[0]].ids.graph.ylabel = 'Pressao' 
        

        self._graph[self._tags_with_graphs[1]] = (DataGraphPopup(self._max_points, self._tags[self._tags_with_graphs[1]]['color']))
        self._graph[self._tags_with_graphs[1]].title = 'Fluxo'
        self._graph[self._tags_with_graphs[1]].ids.graph.ylabel = 'Fluxo' 


        # for key,value in kwargs.get('modbus_CLP').items():
        #     if key == 'fornalha':
        #         plot_color = (1,0,0,1)
        #     else:
        #         plot_color = (random.random(),random.random(),random.random(),1)
        #     self._tags[key] = {'addr' : value, 'color' : plot_color}
        # self._graph = DataGraphPopup(self._max_points, self._tags['fornalha']['color'])

        

    def startDataRead(self, ip, port):
        """
        Método utilizado para configuração do IP e porta do servidor Modbus e
        inicializar uma thread para a leitura dos dados e atualização da interface
        gráfica
        """

        self._serverIP = ip
        self._serverPort = port
        self._modbusClient.host = self._serverIP
        self._modbusClient.port = self._serverPort
        try:
            Window.set_system_cursor("wait")
            self._modbusClient.open()
            Window.set_system_cursor("arrow")
            if self._modbusClient.is_open:
                self._updateThread = Thread(target=self.updater)
                self._updateThread.start()
                self.ids.img_con.source = "imgs/conectado.png"
                self._modbusPopup.dismiss()
            else:
                self._modbusPopup.setInfo("Falha na conexão com o servidor")

        except Exception as e:
            print("Erro: ", e.args)

    def updater(self):
        """
        Método que invoca as rotinas de leitura dos dados, atualização da 
        interface e inserção dos dados no Banco de Dados
        """

        try:
            while self._updateWidgets:
                self.readData()
                self.updateGUI()
                #inserir dados no BD
                sleep(self._scan_time/1000) #ms
        except Exception as e:
            self._modbusClient.close()
            print("Erro: ", e.args)

    def readData(self):
        '''
        Metodo para leitura dos dados por meio do protocolo MODBUS
        '''
        self._lock.acquire()
        self._meas ['timestamp'] = datetime.now()
        self._lock.release()
        for key, value in self._tags.items():
            self._lock.acquire()
            if value['bit'] != None:
                self._meas['values'][key] = ((self._modbusClient.read_holding_registers(value['address'],1)[0] & (1 << value['bit'])) >> value['bit'])
            else:
                self._meas['values'][key] = self._modbusClient.read_holding_registers(value['address'],1)[0] / value['div']
            self._lock.release()
        self._lock.acquire()
        self._meas['values']['co_pressao'] = 50#int(random.random() * 100) 
        self._meas['values']['co_fit03'] = 30#int (random.random() * 100) 
        self._lock.release()
       
        
    
    def writeData(self, tag, value):
        self._lock.acquire()
        if self._modbusClient.is_open:
            if self._tags[tag]['bit'] != None:
                val = self._modbusClient.read_holding_registers(self._tags[tag]['address'],1)[0]
                if value:
                    val |= val (1 << self._tags[tag]['bit'])
                else:
                    val &= ~(1 << self._tags[tag]['bit']) 
                self._modbusClient.write_single_register(self._tags[tag]['address'], val)
            else:
                self._modbusClient.write_single_register(self._tags[tag]['address'], value)
        self._lock.release()

        pass

    def toggleBitValue(self, tag):
        self._lock.acquire()
        if self._modbusClient.is_open:
            val = self._modbusClient.read_holding_registers(self._tags[tag]['address'],1)[0]
            val ^= (1 << self._tags[tag]['bit'])
            self._modbusClient.write_single_register(self._tags[tag]['address'], val)
            # print('aqui')
            # self.ids.lbt8.background_color = (1,0,0,1)
        self._lock.release()

        
    def updateGUI(self):
        """
        Metodo para atualizacao da interface grafica a partir dos dados lidos
        """

        #atualizacao dos labels das temperaturas
        # for key,value in self._tags.items():
        #     self.ids[key].text = str(self._meas['values'][key]) + ' C'

        # #Atualizar nivel do termometro 
        # self.ids.lb_temp.size = (self.ids.lb_temp.size[0], self._meas['values']['fornalha']/450*self.ids.termometro.size[1])
        #Atualizacao do grafico
        self._lock.acquire()
        self.updateGraphs()
        self._lock.release()

        self._lock.acquire()
        self.updateVisualElements()
        self._lock.release()

        self._bar.pressure = random.random()


    def updateGraphs(self):
        for tag in self._tags_with_graphs:
            self._graph[tag].ids.graph.updateGraph((self._meas['timestamp'], self._meas['values'][tag]),0)


    def updateVisualElements(self):
        for key, value in self._tags.items():
            match key:
                #atualiza os ícones das cargas/válvulas
                case 'co_xv2':
                    if self._meas['values'][key]:  
                        self.ids.bt_xv2.background_normal = 'imgs/ClosedValve.png'
                    else: 
                        self.ids.bt_xv2.background_normal = 'imgs/OpenValve.png'
                case 'co_xv3':
                    if self._meas['values'][key]:  
                        self.ids.bt_xv3.background_normal = 'imgs/ClosedValve.png'
                    else: 
                        self.ids.bt_xv3.background_normal = 'imgs/OpenValve.png'
                case 'co_xv4':
                    if self._meas['values'][key]:  
                        self.ids.bt_xv4.background_normal = 'imgs/ClosedValve.png'
                    else: 
                        self.ids.bt_xv4.background_normal = 'imgs/OpenValve.png'
                case 'co_xv5':
                    if self._meas['values'][key]:  
                        self.ids.bt_xv5.background_normal = 'imgs/ClosedValve.png'
                    else: 
                        self.ids.bt_xv5.background_normal = 'imgs/OpenValve.png'
                case 'co_xv6':
                    if self._meas['values'][key]:  
                        self.ids.bt_xv6.background_normal = 'imgs/ClosedValve.png'
                    else: 
                        self.ids.bt_xv6.background_normal = 'imgs/OpenValve.png'

                case 'co_sel_driver':
                
                    match self._meas['values'][key]:
                        
                        case 1:
                            self.ids.bt_soft.background_color = (53.0*1/255,63.0*1/255,80.0*1/255,1)
                            self.ids.bt_inversor.background_color = (214.0*2.5/255, 220.0*2.5/255, 229.0*2.5/255)
                            self.ids.bt_direta.background_color = (214.0*2.5/255, 220.0*2.5/255, 229.0*2.5/255)
                        case 2:
                            self.ids.bt_soft.background_color = (214.0*2.5/255, 220.0*2.5/255, 229.0*2.5/255)
                            self.ids.bt_inversor.background_color = (53.0*1/255,63.0*1/255,80.0*1/255,1)
                            self.ids.bt_direta.background_color = (214.0*2.5/255, 220.0*2.5/255, 229.0*2.5/255)
                        case 3:
                            self.ids.bt_soft.background_color = (214.0*2.5/255, 220.0*2.5/255, 229.0*2.5/255)
                            self.ids.bt_inversor.background_color = (214.0*2.5/255, 220.0*2.5/255, 229.0*2.5/255)
                            self.ids.bt_direta.background_color = (53.0*1/255,63.0*1/255,80.0*1/255,1)

                case 'co_pressostato':
                    self.ids.lbt6.text = str(self._meas['values']['co_pressao'])
                case 'co_fit03':
                    self.ids.lbt7.text = str(self._meas['values']['co_fit03'])

                case 't1':
                    self._motorPopup.ids.var1.text = f"{self._meas['values']['t1']}"
                case 't1':
                    self._motorPopup.ids.var2.text = f"{self._meas['values']['t1']}"
                case 't1':
                    self._motorPopup.ids.var3.text = f"{self._meas['values']['t1']}"
                case 't1':
                    self._motorPopup.ids.var4.text = f"{self._meas['values']['t1']}"
                case 't1':
                    self._motorPopup.ids.var5.text = f"{self._meas['values']['t1']}"
                case 't1':
                    self._motorPopup.ids.var6.text = f"{self._meas['values']['t1']}"
                case 't1':
                    self._motorPopup.ids.var7.text = f"{self._meas['values']['t1']}"
                case 't1':
                    self._motorPopup.ids.var8.text = f"{self._meas['values']['t1']}"


    def modoPartidaMotor(self, val):
        self.writeData('co_sel_driver', val)
    
    def acionamentoMotor(self):
        val = -1
        self._lock.acquire()
        try:
            match self._meas['values']['co_sel_driver']:
                case 1:
                    if self._meas['values']['co_ats48'] == 1:
                        val = 0
                    else:
                        val = 1
                    self._lock.release()
                    self.writeData('co_ats48', val)
                    self.writeData('co_atv31', 0)
                    self.writeData('co_tesys', 0)
                case 2:
                    if self._meas['values']['co_atv31'] == 1:
                        val = 0
                    else:
                        val = 1
                    self._lock.release()
                    self.writeData('co_ats48', 0)
                    self.writeData('co_atv31', val)
                    self.writeData('co_tesys', 0)
                case 3:
                    if self._meas['values']['co_tesys'] == 1:
                        val = 0
                    else:
                        val = 1
                    self._lock.release()
                    self.writeData('co_ats48', 0)
                    self.writeData('co_atv31', 0)
                    self.writeData('co_tesys', val)
            #Atualiza o ícone do motor
            match val:
                case 0:
                    self.ids.bt_motor.background_normal = 'imgs/MotorOff.png'
                case 1:
                    self.ids.bt_motor.background_normal = 'imgs/MotorOn.png'
        except Exception as e:
            self._lock.release()
            print(e)
        pass

    def openMotorStatus(self):
        self._motorPopup.open()
        pass

    def on_enter_button(self, instance):
        Window.set_system_cursor('hand')

    def stopRefresh(self):
        self._updateWidgets = False



# class PressureBar(BoxLayout):
#     pressure = 0.4
#     def set_pressure(self, value):
#         self.pressure = value