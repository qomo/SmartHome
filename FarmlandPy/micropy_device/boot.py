

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = 'HUAWEI-BAYNPM'
password = 'jiayou110'
mqtt_server = '78.141.194.186'

mqtt_port = 8883
user_name = 'qomoliao'
user_passwd = 'zong07882462'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = 'cmd_watering'
topic_pub = 'humidity'
hmd_adc = machine.ADC(0)

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


