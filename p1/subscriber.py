import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado com código de resultado "+str(rc))
    client.subscribe("sensor/temp")

def on_message(client, userdata, message):
    print(f"Mensagem Recebida:\n {message.payload.decode()}\nNo tópico {message.topic}\n")

# Configuração do cliente
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "python_subscriber")
client.on_connect = on_connect
client.on_message = on_message

# Conecte ao broker
client.connect("localhost", 1891, 60)

# Loop para manter o cliente executando e escutando por mensagens
client.loop_forever()