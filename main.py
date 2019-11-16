from machine import Pin,I2C,RTC
import time
import ssd1306
import socket
import network
import urequests

i2c=I2C(scl=Pin(22),sda=Pin(21),freq=100000) #esp32
oled=ssd1306.SSD1306_I2C(128,64,i2c)

wlan=0

def connectWiFi(ID,password):
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ID, password)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
    oled.fill(0)
    oled.text('connecting WIFI',0,0)
    oled.show()
  oled.fill(0)
  oled.text('WIFI connected',0,0)
  oled.show()
  time.sleep(2)
  return True


def get_time():
  URL="http://quan.suning.com/getSysTime.do"
  res=urequests.get(URL).text
  temp=res.split('"')
  data=temp[7]
  date=[data[:4],data[4:6],data[6:8],data[8:10],data[10:12],data[12:]]
  got_time=[]
  for str in date :
    got_time.append(int(str))
  return got_time
  
  
def set_time():
    time=get_time()
    rtc=RTC()
    rtc.init((time[0], time[1], time[2], 4, time[3], time[4], time[5], 0))
    return rtc
  
def display_time(rtc):
    time=rtc.datetime()
    oled.fill(0)
    oled.text(str(time[0])+' '+str(time[1])+' '+str(time[2]),24,0)
    oled.text(str(time[4])+':'+str(time[5])+':'+str(time[6]),40,16)
    oled.show()
    
connectWiFi('233','123456789')
rtc=set_time()

while True:
    display_time(rtc)
    
  