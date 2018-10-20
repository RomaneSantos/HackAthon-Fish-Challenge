import mysql.connector

def conectar():
    mydb = mysql.connector.connect(
        host="localhost", 
        user="root",
        passwd="",
        database="enamor")
    
    return mydb

def inserir_alerta(tabela, alerta, valor, mydb):
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {tabela}(alerta, valor_atual) VALUES ('{alerta}', '{valor}')"
    mycursor.execute(sql)
    mydb.commit()


def buscar(dado, mydb):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT {dado} FROM atual")
    myresult = mycursor.fetchall()
    return myresult[-1][0]

class Valores():
    """Essa classe define se os valores estão dentro do padrão."""
    def __init__(self, valor, padrão):
        self.valor = valor
        self.padrão = padrão
    
    def verificar(self):
        if self.valor == self.padrão:
            return  self.valor
        return self.valor - self.padrão

class Alerta():
    """Classe que controla os níveis de alerta do tanque"""
    def __init__(self, temp, oxi):
        self.temperatura = Valores(buscar("Temperatura", banco), temp)
        self.temp = buscar("Temperatura", banco)
        self.oxigenio = Valores(buscar("Oxigenio", banco), oxi)
        self.oxi = buscar("Oxigenio", banco)
        self.nivel_da_agua = buscar("Agua", banco)
        self.nivel = self.nivel_da_agua
        self.turbidez = Valores(buscar("Turbidez", banco), 25)
        self.turb = 25
    
    def verificar_temp(self):
        """Calcula se a temperatura da água está na ideal"""
        temp = self.temperatura.verificar()

        if 2 < temp < 6:
            return 1
        elif -6 < temp < -2:
            return -1
        elif temp > 6:
            return 2
        elif temp < -6:
            return -2
        return 0

    def verificar_turb(self):
        """Calcula se a turbidez está no nível ideal."""
        turb = self.turbidez.verificar()

        if turb < -15 and turb > 15:
            return 2
        return 0
        
    def verificar_oxi(self):
        """Verifica se a oxigenação é a ideal para espécie."""
        oxi = self.oxigenio.verificar()

        if oxi is not 0:
            return 2
        return 0

    def verificar_nivel(self):
        """Verifica se o nível da água está abaixo"""
        self.nivel = 100 - (((self.nivel_da_agua - 90) * 100) / 880)
        
        if self.nivel < 85:
            return -1
        return 0


banco = conectar()

while True:
    try:
        pintado = Alerta(temp=26, oxi=3)
        inserir_alerta("Nivel", pintado.verificar_nivel(), pintado.nivel, banco)
        inserir_alerta("Oxigenio", pintado.verificar_oxi(), pintado.oxi, banco)
        inserir_alerta("Temperatura", pintado.verificar_temp(), pintado.temp, banco)
        inserir_alerta("Turbidez", pintado.verificar_turb(), pintado.turb, banco)
        print("Ok")
    except IndexError:
        pass
