import sqlite3
from threading import Lock

class BDHandler():
    """
    Classe para a manipulação do banco de dados
    """
    def __init__(self,dbpath,tags,tablename='dataTable'):
        """
        Construtor
        """
        # Inicialização do banco de dados SQL
        self._dbpath = dbpath
        self._tablename = tablename
        self._con = sqlite3.connect(self._dbpath, check_same_thread=False)
        self._cursor = self._con.cursor()
        self._col_names = tags.keys()
        self._lock = Lock()
        self.createTable()


    def createTable(self):
        """
        Método que cria a tabela para armazenamento dos dados caso ela não exista
        """

        try:
            # Monta a string SQL para criação da tabela
            sqr_str = f"""
            CREATE TABLE IF NOT EXISTS {self._tablename} (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                timestamp TEXT NOT NULL,
                """
            # Adiciona cada coluna especificada em tags
            for n in self._col_names:
                sqr_str += f'{n} REAL,'
            sqr_str = sqr_str[:-1]
            sqr_str += ');'
            self._lock.acquire() # Adquire o lock para operações thread-safe
            self._cursor.execute(sqr_str) # Executa a criação da tabela
            self._con.commit() # Confirma a transação
            self._lock.release() # Libera o lock
        except Exception as e:
            print("Erro: ",e.args)

    def insertData(self, data):
        """
        Método para inserção dos dados no BD
        """
        try:
            self._lock.acquire() # Adquire o lock para operações thread-safe
            timestamp = str(data['timestamp']) # Obtém o timestamp dos dados
             # Monta a string de colunas e valores para inserção
            str_cols = 'timestamp,'+','.join(data['values'].keys())
            str_values = f"'{timestamp}',"+','.join([str(data['values'][k]) for k in data['values'].keys()])
            sql_str = f'INSERT INTO {self._tablename} ({str_cols}) VALUES  ({str_values});'
            self._cursor.execute(sql_str) # Executa a inserção dos dados
            self._con.commit() # Confirma a transação
        except Exception as e:
            print("Erro: ",e.args)
        finally:
            self._lock.release() # Libera o lock

    
    def selectData(self, cols, init_t, final_t):
        """
        Método que realiza a busca no BD entre 2 horários especificados
        """
        try:
            self._lock.acquire() # Adquire o lock para operações thread-safe
            # Monta a string SQL para seleção dos dados entre os horários especificados
            sql_str = f"SELECT {','.join(cols)} FROM {self._tablename} WHERE timestamp BETWEEN '{init_t}' AND '{final_t}'"
            self._cursor.execute(sql_str) # Executa a consulta
            dados = dict((sensor, []) for sensor in cols) # Inicializa o dicionário para armazenar os dados
            for linha in self._cursor.fetchall():  #Para cada linha retornada pela consulta
                for d in range(0, len(linha)):
                    dados[cols[d]].append(linha[d])    # Adiciona os valores aos respectivos sensores
            self._lock.release() # Libera o lock
            return dados # Retorna os dados selecionados
        except Exception as e:
            print("Erro: ",e.args)
        



