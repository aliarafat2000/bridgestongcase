import psutil
from gpiozero import CPUTemperature
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import LCD1602
import time

outPin = 40
GPIO.setup(outPin,GPIO.OUT)
GPIO.output(outPin,0)
LCD1602.init(0x27, 1)



def check_cpu_temperature():
    cpu = CPUTemperature()
    return cpu.temperature

def check_cpu_usage():
    return psutil.cpu_percent(interval=1)

def check_memory_usage():
    return psutil.virtual_memory().percent

def main():
    temperature = check_cpu_temperature()
    cpu_usage = check_cpu_usage()
    memory_usage = check_memory_usage()
    
    if temperature < 60.0:
        LCD1602.clear()
        LCD1602.write(0,0, f"Temp: {temperature:.2f}°C")
        LCD1602.write(0,1, f"CPU: {cpu_usage}%")
        print("Raspberry Pi Health Check:")
        print(f"CPU Temperature: {temperature:.2f}°C")
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_usage}%")
    else:
        LCD1602.clear()
        LCD1602.write(0,0, f"Temp: {temperature:.2f}°C")
        LCD1602.write(0,1, "    DANGER!!!")
        GPIO.output(outPin,1)
        sleep(1)
        GPIO.output(outPin,0)

if __name__ == "__main__":
    try:
        while True:
            main()
            sleep(1)
            print("="*50)
        
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        LCD1602.clear()
        print("GPIO pins are ready")
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        GPIO.cleanup()
        LCD1602.clear()
        print("GPIO pins are ready")
