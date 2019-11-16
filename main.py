from machine import Pin,I2C,RTC
import time
import ssd1306
import socket
import network
import urequests
import ujson

i2c=I2C(scl=Pin(22),sda=Pin(21),freq=100000) #esp8266
lcd=ssd1306.SSD1306_I2C(128,64,i2c)

wlan=0
def connectWiFi():
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect('233', '123456789')
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
  return True
H=None
M=None
S=None

def get_time():
  global H, M, S
  global yy,dd,mm
  URL="http://quan.suning.com/getSysTime.do"
  res=urequests.get(URL).text
  j=ujson.loads(res)
  list=j['sysTime2'].split()[1]
  list1=j['sysTime2'].split()[0]
  H=int(list.split(":")[0])
  M=int(list.split(":")[1])
  S=int(list.split(":")[2])

def data(M, S):
  for m in range (M, 50):
    for x in range(S, 60):
      lcd.text(str(H)+":"+str(m)+":"+str(x),20, 40,)
      lcd.show()
      time.sleep(1)
      lcd.fill(0)
      #lcd.fill_rect(18, 40,20, 40, 0)
    S=0
  M=0

connectWiFi()

while True: 
  get_time()
  data(M, S)
  pass

