import paho.mqtt.client as mqtt
import time
import random
import datetime

class TempSensor():
    def __init__(self, id, tipo, temp=0, timestamp=0, alert=''):
        self.id = id
        self.tipo = tipo
        self.temp = temp
        self.timestamp = timestamp
        self.alert = alert
    
    def __str__(self):
        return f'\nSensor: {self.id} \n Tipo: {self.tipo} \n Temperatura: {self.temp} \n alerta={self.alert}\n Timestamp: {self.timestamp} \n '
    
    def checkTemp(self):
        if self.tipo == 'freezer':
            if (self.temp < -25) or (self.temp > -10):
                self.alert = 'Temperatura fora do padrão, checar freezer!'
        elif self.tipo == 'geladeira':
            if (self.temp < 2) or (self.temp > 10):
                self.alert = 'Temperatura fora do padrão, checar geladeira!'
        else:
            self.alert = 'erro'
    
    def generateData(self):
        current_datetime = datetime.datetime.now()
        timestamp = current_datetime.timestamp()
        datetime_object = datetime.datetime.fromtimestamp(timestamp)
        self.timestamp = datetime_object

        if self.tipo == 'freezer':
            self.temp = round(random.triangular(-30, 0, -20))
        elif self.tipo == 'geladeira':
            self.temp = round(random.triangular(-1, 14, 5))
        else:
            print('tipo não identificado')

        self.checkTemp()

temp01F = TempSensor('lj01f01', 'freezer')
temp02F = TempSensor('lj01f02', 'freezer')
temp01G = TempSensor('lj01g01', 'geladeira')
temp02G = TempSensor('lj01g02', 'geladeira')


# Configuração do cliente
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"python_publisher")
# Conecte ao broker
client.connect("localhost", 1891, 60)

try:
    while True:
        data01 = temp01F.generateData()
        data02 = temp02F.generateData()
        data03 = temp01G.generateData()
        data04 = temp02G.generateData()

        temp01F.checkTemp()
        temp02F.checkTemp()
        temp01G.checkTemp()
        temp02G.checkTemp()

        message1 = str(temp01F)
        message2 = str(temp02F)
        message3 = str(temp01G)
        message4 = str(temp02G)
        
        client.publish("sensor/temp", message1, 1)
        time.sleep(1)

        client.publish("sensor/temp", message2, 1)
        time.sleep(1)

        client.publish("sensor/temp", message3, 1)
        time.sleep(1)

        client.publish("sensor/temp", message4, 1)
        time.sleep(1)

except KeyboardInterrupt:
    print("\n Publicação encerrada")

client.disconnect()