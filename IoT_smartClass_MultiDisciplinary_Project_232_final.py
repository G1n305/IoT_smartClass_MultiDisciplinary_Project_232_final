from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from mqtt import *
from machine import RTC
import ntptime
import time
from aiot_hcsr04 import HCSR04
from event_manager import *
from machine import Pin, SoftI2C
from aiot_dht20 import DHT20
from aiot_lcd1602 import LCD1602
from aiot_rgbled import RGBLed
import music

event_manager.reset()

aiot_dht20 = DHT20(SoftI2C(scl=Pin(22), sda=Pin(21)))

aiot_lcd1602 = LCD1602()

def on_event_timer_callback_G_Y_v_S_L():
  global th_C3_B4ng_tin, light, temp, humid, fanspeed, ledstat
  aiot_dht20.read_dht20()
  light = round(translate((pin2.read_analog()), 0, 4095, 0, 100))
  temp = aiot_dht20.dht20_temperature()
  humid = aiot_dht20.dht20_humidity()
  aiot_lcd1602.move_to(0, 0)
  aiot_lcd1602.putstr((round(translate((pin2.read_analog()), 0, 4095, 0, 100))))
  aiot_lcd1602.move_to(0, 1)
  aiot_lcd1602.putstr((aiot_dht20.dht20_temperature()))
  aiot_lcd1602.move_to(7, 1)
  aiot_lcd1602.putstr((aiot_dht20.dht20_humidity()))
  mqtt.publish('light', light)
  mqtt.publish('temp', temp)
  mqtt.publish('humid', humid)

event_manager.add_timer_event(30000, on_event_timer_callback_G_Y_v_S_L)

def on_event_timer_callback_f_d_G_q_z():
  global th_C3_B4ng_tin, light, temp, humid, fanspeed, ledstat
  if (int(temp)) > 40:
    display.set_pixel(0, 0, '#ff0000')
  else:
    display.set_pixel(0, 0, '#00ff00')
  if (int(light)) > 75:
    display.set_pixel(1, 0, '#ff0000')
  else:
    display.set_pixel(1, 0, '#00ff00')

event_manager.add_timer_event(5000, on_event_timer_callback_f_d_G_q_z)

tiny_rgb = RGBLed(pin16.pin, 4)

def on_mqtt_message_receive_callback__led2_(th_C3_B4ng_tin):
  global light, temp, humid, fanspeed, ledstat
  if th_C3_B4ng_tin == '1':
    display.set_pixel(0, 1, '#ffffff')
    tiny_rgb.show(0, hex_to_rgb('#ffffff'))
  else:
    display.set_pixel(0, 1, '#000000')
    tiny_rgb.show(0, hex_to_rgb('#000000'))

def on_mqtt_message_receive_callback__led_(th_C3_B4ng_tin):
  global light, temp, humid, fanspeed, ledstat
  if ledstat == 1:
    display.set_brightness((int(th_C3_B4ng_tin)))
    if (int(th_C3_B4ng_tin)) == 0:
      mqtt.publish('led2', '0')
    if (int(th_C3_B4ng_tin)) > 0 and (int(th_C3_B4ng_tin)) < 25:
      tiny_rgb.show(1, hex_to_rgb('#ffffff'))
      tiny_rgb.show(2, hex_to_rgb('#000000'))
      tiny_rgb.show(3, hex_to_rgb('#000000'))
      tiny_rgb.show(4, hex_to_rgb('#000000'))
    if (int(th_C3_B4ng_tin)) >= 25 and (int(th_C3_B4ng_tin)) <= 50:
      tiny_rgb.show(1, hex_to_rgb('#ffffff'))
      tiny_rgb.show(2, hex_to_rgb('#ffffff'))
      tiny_rgb.show(3, hex_to_rgb('#000000'))
      tiny_rgb.show(4, hex_to_rgb('#000000'))
    if (int(th_C3_B4ng_tin)) > 50 and (int(th_C3_B4ng_tin)) <= 75:
      tiny_rgb.show(1, hex_to_rgb('#ffffff'))
      tiny_rgb.show(2, hex_to_rgb('#ffffff'))
      tiny_rgb.show(3, hex_to_rgb('#ffffff'))
      tiny_rgb.show(4, hex_to_rgb('#000000'))
    if (int(th_C3_B4ng_tin)) > 75 and (int(th_C3_B4ng_tin)) < 100:
      tiny_rgb.show(0, hex_to_rgb('#ffffff'))
    if (int(th_C3_B4ng_tin)) == 100:
      mqtt.publish('led2', '1')

def on_mqtt_message_receive_callback__fan_(th_C3_B4ng_tin):
  global light, temp, humid, fanspeed, ledstat
  fanspeed = int(th_C3_B4ng_tin)
  pin1.write_analog(round(translate((int(th_C3_B4ng_tin)), 0, 100, 0, 1023)))

def on_mqtt_message_receive_callback__Welcome_Feed_(th_C3_B4ng_tin):
  global light, temp, humid, fanspeed, ledstat
  if th_C3_B4ng_tin == '1':
    pin4.servo_write(90)
    time.sleep_ms(1000)
  else:
    pin4.servo_write(0)
    time.sleep_ms(1000)
    pin4.servo_release()

# Mô tả hàm này...
def dangky():
  global th_C3_B4ng_tin, light, temp, humid, fanspeed, ledstat, aiot_dht20, aiot_ultrasonic, tiny_rgb, aiot_lcd1602
  mqtt.on_receive_message('led2', on_mqtt_message_receive_callback__led2_)
  mqtt.on_receive_message('led', on_mqtt_message_receive_callback__led_)
  mqtt.on_receive_message('fan', on_mqtt_message_receive_callback__fan_)
  mqtt.on_receive_message('Welcome Feed', on_mqtt_message_receive_callback__Welcome_Feed_)

def on_event_timer_callback_g_J_g_L_w():
  global th_C3_B4ng_tin, light, temp, humid, fanspeed, ledstat
  if (int(light)) < 40 and ledstat == 1:
    mqtt.publish('led2', '1')
  if (int(light)) >= 80 and ledstat == 1:
    mqtt.publish('led2', '0')
  if (int(temp)) >= 35 and fanspeed < 50:
    mqtt.publish('fan', '50')

event_manager.add_timer_event(10000, on_event_timer_callback_g_J_g_L_w)

def on_event_timer_callback_u_r_r_W_I():
  global th_C3_B4ng_tin, light, temp, humid, fanspeed, ledstat
  if aiot_ultrasonic.distance_cm() < 5:
    pin4.servo_write(90)
    music.play(['F5:1'], wait=True)
    music.play(['C5:1'], wait=True)
    time.sleep_ms(2000)
    pin4.servo_write(0)
    time.sleep_ms(1000)
    pin4.servo_release()

event_manager.add_timer_event(500, on_event_timer_callback_u_r_r_W_I)

def on_event_timer_callback_Q_v_M_Q_Q():
  global th_C3_B4ng_tin, light, temp, humid, fanspeed, ledstat
  if (int(temp)) >= 40:
    mqtt.publish('fan', '50')
  if (int(temp)) >= 80:
    music.play(['F5:1'], wait=True)
    music.play(['A4:1'], wait=True)

event_manager.add_timer_event(10000, on_event_timer_callback_Q_v_M_Q_Q)

if True:
  display.scroll('ctrl')
  mqtt.connect_wifi('Hong them', 'quang1234')
  mqtt.connect_broker(server='io.adafruit.com', port=1883, username='1zy', password='')
  ntptime.settime()
  (year, month, mday, week_of_year, hour, minute, second, milisecond) = RTC().datetime()
  RTC().init((year, month, mday, week_of_year, hour+7, minute, second, milisecond))
  aiot_ultrasonic = HCSR04(trigger_pin=pin10.pin, echo_pin=pin13.pin)
  ledstat = 1
  dangky()
  display.scroll('OK!')

while True:
  event_manager.run()
  mqtt.check_message()
  time.sleep_ms(1000)
