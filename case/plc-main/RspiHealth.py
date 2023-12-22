import psutil
from gpiozero import CPUTemperature
from time import sleep
import time
import mysql.connector



def check_cpu_temperature():
    cpu = CPUTemperature()
    return cpu.temperature

def check_cpu_usage():
    return psutil.cpu_percent(interval=1)

def check_memory_usage():
    return psutil.virtual_memory().percent

    





def insert_into_mysql_2(single_entry_buffer):
    try:
        connection = mysql.connector.connect( 
            host="193.203.184.2",
            user="u295327377_madical_user",
            password="5G27zBkBOZ6w",
            database="u295327377_madical_db",
            port=3306
        )
        
        cursor = connection.cursor()        
        
        query = "INSERT INTO device_health(time, CPU_Temperature, CPU_Usage, Memory_Usage) VALUES (%s, %s, %s, %s)"
        values = (single_entry_buffer['time'], single_entry_buffer['CPU_Temperature'] ,single_entry_buffer['CPU_Usage'] ,single_entry_buffer['Memory_Usage'])    
        print("entering")
        cursor.execute(query, values)
        print("exiting")
        connection.commit()
        print("Data inserted into MySQL successfully")
       
    
    except Exception as e:
        print(str(e))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    

def deviceMonitoring():
    try:
        while True:
            print("Hi")
            temperature = check_cpu_temperature()
            cpu_usage = check_cpu_usage()
            memory_usage = check_memory_usage()
            single_entry_buffer = {}

            single_entry_buffer["CPU_Temperature"] = temperature
            single_entry_buffer["CPU_Usage"] = cpu_usage
            single_entry_buffer["Memory_Usage"] = memory_usage
            single_entry_buffer['time'] = time.strftime("%Y-%m-%d %H:%M:%S")

#             print(single_entry_buffer)
            insert_into_mysql_2(single_entry_buffer)
            print("device health entering done")
            single_entry_buffer.clear()
            sleep(60)
#             print("="*50)
        
        
    except KeyboardInterrupt:
        print("program interrupted in RspiHealth.py file")
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

if __name__ == "__main__":
    try:
        deviceMonitoring()
        
    except KeyboardInterrupt:
        print("program stopped")
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        GPIO.cleanup()
        print("GPIO pins are ready")
