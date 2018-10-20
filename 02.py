import serial
import mysql.connector

porta = 'COM5'
baud_rate = 9600
cont = 0
temp = 0
oxi = 10
agua = 0
turb = 0

def insert():
    global agua, oxi, temp, turb
    mycursor = mydb.cursor()
    sql = "INSERT INTO atual VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, (str(agua), str(oxi), str(temp), str(turb)))
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def verifica_portas():
    portas_ativas = []
    for numero in range(10):
        try:
            objeto_verifica = serial.Serial("COM"+str(numero))
            portas_ativas.append((numero, objeto_verifica.portstr))
            objeto_verifica.close()
        except serial.SerialException:
            pass
    return portas_ativas

def mandarValor(valor):
    global cont, temp, agua, turb
    if cont % 4 == 0:
      insert()  
    elif valor[0] == 'T':
        temp = float(valor.replace("T", ''))
        print(temp)
    elif valor[0] == 'N':
        agua = int(valor.replace("N", ''))
        print(agua)
    elif valor[0] == 'Z':
        turb = valor.replace("Z", '')
        print(turb)
 
def ler_porta():
   global cont
   try:
       Obj_porta = serial.Serial(porta, baud_rate)
       while(1):
           valor = Obj_porta.readline()
           valor = str(valor);
           valor = valor.replace('b\'', '')
           valor = valor.replace('\\r\\n\'', '')
           cont = cont + 1
           mandarValor(valor)
       Obj_porta.close()
   except serial.SerialException:
       print("ERRO: Verifique se ha algum dispositivo conectado na porta!")

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="enamor")

for numero,portas_ativas in verifica_portas():
    porta = portas_ativas

ler_porta()
