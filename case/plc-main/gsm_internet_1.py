import serial
import RPi.GPIO as GPIO
import os, time

GPIO.setmode(GPIO.BOARD)

ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

ser.write("AT"+"\r\n")

rcv = ser.read(10)
print(rcv)

time.sleep(1)

ser.write("AT+CPIN?\r")
msg=ser.read(128)
print(msg)
time.sleep(3)

ser.write("AT+CIPSHUT\r")
msg=ser.read(128)
print(msg)
time.sleep(3)

ser.write("AT+CIPMUX=0\r")
msg=ser.read(128)
print(msg)
time.sleep(3)

ser

command="AT+CGDCONT=1"+","+'"IP"'+","'"airtelgprs.com"\r'
ser.write(command.encode())
msg=ser.read(128)
print(msg)
time.sleep(3)

ser.write('AT+CSTT="airtelgprs.com","",""\r')