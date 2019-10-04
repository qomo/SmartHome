def sub_cb(topic, msg):
  watering_do = machine.Pin(0, machine.Pin.OUT)
  print((topic, msg))
  if topic == b'cmd_watering':
    print('ESP received message: %s' %msg)
    if msg == b'1':
      watering_do.on()
      client.publish('watering', '1')
    else:
      watering_do.off()
      client.publish('watering', '0')

def connect_and_subscribe():
  global client_id, mqtt_server, mqtt_port, topic_sub, user_name, user_passwd
  client = MQTTClient(client_id, mqtt_server, port=mqtt_port, user=user_name, password=user_passwd)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  global hmd_adc
  try:
    client.check_msg()

    if (time.time() - last_message) > message_interval:
      msg = b'%d' % hmd_adc.read()
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()
