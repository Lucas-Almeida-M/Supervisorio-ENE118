from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup, DataGraphPopup, motorPopup, HistGraphPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread, Lock
from time import sleep
from datetime import datetime
import random
from timeseriesgraph import TimeSeriesGraph
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from bdhandler import BDHandler
from kivy_garden.graph import LinePlot


class MainWidget (BoxLayout):
    """
    Widget principal da aplicação
    """
    _updateThread = None
    _updateWidgets = True
    _tags = {}
    _pressure = 0.5
    _max_points = 15
    _max_y = [6,15]
    _tags_with_graphs = ['co_pressao','co_fit02']
    _tags_with_graphs_values = {
    'co_pressao': {'max': 5, 'min': 0},
    'co_fit02': {'max': 15, 'min': 0}
    }   

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
        self._meas = {}
        self._meas ['timestamp'] = None
        self._meas ['values'] = {}

        for item in self._modbusCLP:
            tag = item.pop('tag')
            self._tags[tag] = item
            plot_color = (random.random(),random.random(),random.random(),1)
            self._tags[tag]['color'] = plot_color
        
        self._graph = {} # Cria dicionário dos gráficos

        # Inicializa gráfico da variável Pressão        
        self._graph[self._tags_with_graphs[0]] = (DataGraphPopup(self._max_points, self._tags[self._tags_with_graphs[0]]['color'], self._max_y[0]))
        self._graph[self._tags_with_graphs[0]].title = 'Pressão'
        self._graph[self._tags_with_graphs[0]].ids.graph.ylabel = 'Pressao [Kgf/cm2]' 
        
        # Inicializa gráfico da variável Fluxo 
        self._graph[self._tags_with_graphs[1]] = (DataGraphPopup(self._max_points, self._tags[self._tags_with_graphs[1]]['color'], self._max_y[1]))
        self._graph[self._tags_with_graphs[1]].title = 'Fluxo'
        self._graph[self._tags_with_graphs[1]].ids.graph.ylabel = 'Fluxo [Nm3/min]' 

        self._hgraph = HistGraphPopup(tags = self._tags)
        self._db = BDHandler(kwargs.get('db_path'),self._tags)
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
        self._modbusClient.host = self._serverIP   #input do IP do server
        self._modbusClient.port = self._serverPort #input da porta do server
        try: #tratamento de erros
            Window.set_system_cursor("wait")  #modifica a aparência do cursor 
            self._modbusClient.open()         #inicia a comunicação com o server dados inputs de IP e porta
            Window.set_system_cursor("arrow") #modifica a aparência do cursor 
            if self._modbusClient.is_open:    #verifica se obteve sucesso na comunicação
                self._updateThread = Thread(target=self.updater) #cria uma estrutura de multitarefa (thread)
                self._updateThread.start()                       #Dá o start na Thread com o método updater()
                self.ids.img_con.source = "imgs/conectado.png"   #altera uma imagem na tela principal do supervisório para indicar a conexão
                self._modbusPopup.dismiss()   #Fecha o popup de conexão
            else:
                self._modbusPopup.setInfo("Falha na conexão com o servidor")  #Exibe a mensagem em caso de falha na conexão

        except Exception as e: #tratamento de erros
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
                self._db.insertData(self._meas)
                sleep(self._scan_time/1000) #ms
        except Exception as e:
            self._modbusClient.close()
            print("Erro: ", e.args)

    def readData(self):
        '''
        Method for reading data using the MODBUS protocol
        '''
        self._lock.acquire() #Bloqueio por semáforo, garante que o dicionário _meas não seja acessado enquanto é atualizado
        self._meas['timestamp'] = datetime.now() #Salva o tempo atual (horário da leitura mais recente)
        self._lock.release() #libera o semáforo
        
        for key, value in self._tags.items(): #Faz a varredura de todas as tags
            self._lock.acquire() #bloqueio por semáforo
            try:
                if value['bit'] is not None: #verifica se a grandeza avaliada tem a "propriedade" "bit"
                    self._meas['values'][key] = ((self._modbusClient.read_holding_registers(value['address'], 1)[0] & (1 << value['bit'])) >> value['bit']) 
                    # ^  Faz a leitura do registrador de acordo com o endereço ("address") da tag. Separa cada um dos bits em uma váriavel
                else:
                    if value['tipo'] == 'FP': #Verifica se a grandeza é do tipo float
                        decoder = BinaryPayloadDecoder.fromRegisters(self._modbusClient.read_holding_registers(value['address'], 2), Endian.BIG, Endian.LITTLE)
                        # ^ Converte o valor lido para float
                        self._meas['values'][key] = round(decoder.decode_32bit_float()/value['div'],3)
                        # ^ Faz a divisão da grandeza lida pelo divisor, casa aja
                    else:
                        self._meas['values'][key] = self._modbusClient.read_holding_registers(value['address'], 1)[0] / value['div']
                        # ^ Faz a leitura das grandezas inteiras e faz a divisão pelo divisor (se necessário)
            except Exception as e:  #tratamento de erros
                print(f"Error reading and decoding {key}: {e}")
            finally:
                self._lock.release()
        

            
        #self._lock.acquire()
        #self._meas['values']['co_fit02'] = random.random() * 5
        #self._meas['values']['co_pressao'] = random.random() * 5
        #self._lock.release()
       
        
    
    def writeData(self, tag, value):

        """
        Método que escreve valores nos registradores do CLP
        """
        self._lock.acquire() #bloqueio por semáforo
        if self._modbusClient.is_open:         #Verifica se há comunicação
            if self._tags[tag]['bit'] != None: #Verifica se a tag corresponde a 1 bit da variável
                #\/ Lê estado da variável
                val = self._modbusClient.read_holding_registers(self._tags[tag]['address'],1)[0] 
                if value: #se o valor for 1
                    val |= val (1 << self._tags[tag]['bit']) #inverte o valor do bit
                else:
                    val &= ~(1 << self._tags[tag]['bit'])    #inverte o valor do bit
                #\/ Escreve no registrador o valor atualizado
                self._modbusClient.write_single_register(self._tags[tag]['address'], val) 
            else:# caso contrário, escreve diretamente o valor no registrador
                self._modbusClient.write_single_register(self._tags[tag]['address'], value)
        self._lock.release()

        pass

    def toggleBitValue(self, tag):
        """
        Método que inverte o valor da variável 
        """
        self._lock.acquire()           #bloqueio por semáforo
        if self._modbusClient.is_open: #Verifica se há comunicação
            #\/ Lê estado da variável 
            val = self._modbusClient.read_holding_registers(self._tags[tag]['address'],1)[0]
            #\/ inverte o valor do bit
            val ^= (1 << self._tags[tag]['bit'])
            #\/ Escreve no registrador o valor atualizado
            self._modbusClient.write_single_register(self._tags[tag]['address'], val)
        self._lock.release()

        
    def updateGUI(self):
        """
        Metodo para atualizacao da interface grafica a partir dos dados lidos
        """

        self._lock.acquire()
        self.updateGraphs()
        self._lock.release()

        self._lock.acquire()
        self.updateVisualElements()
        self._lock.release()



        self._lock.acquire()
        pressure_size_x = self.ids.pressure.size[0]
        mapped_size_x = pressure_size_x * (0.15 + 0.7 * (self._meas['values']['co_pressao'] / self._tags_with_graphs_values["co_pressao"]['max']))
        self.ids.lb_pressure.size = (mapped_size_x, self.ids.lb_pressure.size[1])
        self._lock.release()

        self._lock.acquire()
        fluxo_size_x = self.ids.fluxo.size[0]
        mapped_size_x = fluxo_size_x * (0.15 + 0.7 * (self._meas['values']['co_fit02'] / self._tags_with_graphs_values["co_fit02"]['max']))
        self.ids.lb_fluxo.size = (mapped_size_x, self.ids.lb_fluxo.size[1])
        self._lock.release()
        # self._bar.pressure = random.random()


    def updateGraphs(self):
        for tag in self._tags_with_graphs: #Faz a varredura de todas as tags que se deseja visualizar o gráfico
            self._graph[tag].ids.graph.updateGraph((self._meas['timestamp'], self._meas['values'][tag]),0)
            # ^ Cria um gráfico pra cada tag


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

                case 'co_pressao':
                    self.ids.lbt6.text = str(self._meas['values']['co_pressao']) + ' ' +  '[Kgf/cm2]'
                case 'co_fit02':
                    self.ids.lbt7.text = str(self._meas['values']['co_fit02']) + ' ' +  '[Nm3/min]'

                case 'co_tensao_rs':
                    self._motorPopup.ids.var1.text = f"{self._meas['values']['co_tensao_rs']}"
                case 'co_tensao_st':
                    self._motorPopup.ids.var3.text = f"{self._meas['values']['co_tensao_st']}"
                case 'co_tensao_tr':
                    self._motorPopup.ids.var5.text = f"{self._meas['values']['co_tensao_tr']}"
                case 'co_corrente_r':
                    self._motorPopup.ids.var2.text = f"{self._meas['values']['co_corrente_r']}"
                case 'co_corrente_s':
                    self._motorPopup.ids.var4.text = f"{self._meas['values']['co_corrente_s']}"
                case 'co_corrente_t':
                    self._motorPopup.ids.var6.text = f"{self._meas['values']['co_corrente_r']}"
                case 'co_aparente_total':
                    self._motorPopup.ids.var7.text = f"{self._meas['values']['co_aparente_total']}"
                case 'co_fp_total':
                    self._motorPopup.ids.var8.text = f"{self._meas['values']['co_fp_total']}" if self._meas['values']['co_fp_total'] <= 1 else f"{0}"
                case 'co_frequencia':
                    self._motorPopup.ids.var9.text = f"{self._meas['values']['co_frequencia']}"
                case 'co_temp_carc':
                    self._motorPopup.ids.var10.text = f"{self._meas['values']['co_temp_carc']}"

                case 'co_habilita':
                    if self._meas['values']['co_habilita']:
                        self.ids.bt_motor.background_normal = 'imgs/MotorOn.png'
                    else:
                        self.ids.bt_motor.background_normal = 'imgs/MotorOff.png'



    def modoPartidaMotor(self, val):
        self.writeData('co_sel_driver', val)
    
    def acionamentoMotor(self):
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


    def getDataDB(self):
 
        try:
            # Obtém os tempos inicial e final a partir dos campos de texto no gráfico
            init_t = self.parseDTString(self._hgraph.ids.txt_init_time.text)
            final_t = self.parseDTString(self._hgraph.ids.txt_final_time.text)
            cols = []

            # Adiciona o sensor selecionado à lista de colunas
            for sensor in self._hgraph.ids.sensores.children:
                if sensor.ids.checkbox.active:
                    cols.append(sensor.id)
                    key = sensor.id

            # Se o tempo inicial, tempo final ou colunas estiverem vazias, limpa os plots e retorna
            if init_t == None or final_t == None or len(cols) == 0:
                self._hgraph.ids.graph.clearPlots()
                return
            
            # Adiciona a coluna "timestamp" às colunas selecionadas
            cols.append("timestamp")

            # Seleciona os dados do banco de dados com base nas colunas e nos tempos inicial e final
            dados = self._db.selectData(cols, init_t, final_t)
            
            # Se os dados estiverem vazios, retorna
            if dados == None or len(dados['timestamp']) == 0:
                return
            
            # Limpa os plots do gráfico
            self._hgraph.ids.graph.clearPlots()
            # Cria um novo plot de linha com a cor e a largura da linha especificadas
            p = LinePlot(line_width = 1.5, color = self._tags[key]['color'])
            # Define os pontos do plot
            p.points = [(x, dados[key][x]) for x in range (0, len(dados[key]))]
            # Adiciona o plot ao gráfico
            self._hgraph.ids.graph.add_plot(p)
            # Define o valor máximo do eixo x
            self._hgraph.ids.graph.xmax = len(dados[cols[0]])
            # Atualiza os rótulos do eixo x com os timestamps formatados
            self._hgraph.ids.graph.update_x_labels([datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f' ) for x in dados['timestamp']])
            # Define o rótulo do eixo y e o valor máximo do eixo y
            self._hgraph.ids.graph.ylabel = self._tags[key]['grandeza']
            self._hgraph.ids.graph.ymax = self._tags[key]['limits'][1]
        except Exception as e:
            # Captura e imprime qualquer exceção que ocorra
            print(f"erro = {e.args} ")


    def parseDTString (self, datetime_str):

        try:
            # Converte a string de data e hora para o formato desejado
            date = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
            return date.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            # Captura e imprime qualquer exceção que ocorra
            print(f"erro = {e.args} ")

