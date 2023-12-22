import minimalmodbus
import serial
import time
import struct
import sys
import mysql.connector
import math

instrument = minimalmodbus.Instrument('/dev/ttyUSB0',5)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_EVEN
instrument.serial.stopbits = 1

em1220h_addresses = [3027, 3029, 3031, 3019, 3021, 3023, 3077, 3079, 3081, 3109, 2999, 3001, 3003]



def startReadingRegister():
    
    
    while True:
        
        instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 5)
        instrument.serial.baudrate = 9600
        instrument.serial.bytesize = 8
        instrument.serial.parity = serial.PARITY_EVEN
        instrument.serial.stopbits = 1
        
        single_entry_buffer = {}
        
        for address in em1220h_addresses:
            try:

                data = instrument.read_float(address, functioncode=3)
#                 data = round(data,2)
# 
#                 if math.isnan(data):
#                     data = 0.0
                if math.isnan(data):
                    data = 0.0
                data = round(data,2)
#                 print(data)
                
                single_entry_buffer[str(address)] = data
            except Exception as e:
                single_entry_buffer[str(address)] = None
                print(f"An Error Occurred: {str(e)}")
        single_entry_buffer['time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        print("="*50)
        print(single_entry_buffer)
        insert_into_mysql_2(single_entry_buffer)

        
        single_entry_buffer.clear()
        print("="*50)
#         wait_time_in_sec = 5
#         print(f"Waiting for {wait_time_in_sec} seconds.....")
#         
#         #Waiting
#         for remaining in range(wait_time_in_sec,0,-1):
#             sys.stdout.write("\r")
#             sys.stdout.write("{:2d} seconds remaining for next entry.............".format(remaining))
#             sys.stdout.flush()
#             time.sleep(1)
#         sys.stdout.write("\rComplete!        \n")

 
 



#putting data in mysql in em1220h
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
        
        query = "INSERT INTO energy_em1220h(time, Voltage1, Voltage2, Voltage3, Voltage12, Voltage23, Voltage31, Power_Factor_phase_1, Power_Factor_phase_2, Power_Factor_phase_3, Frequency, Active_Power_Phase_1, Active_Power_Phase_2, Active_Power_Phase_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (single_entry_buffer['time'], single_entry_buffer['3027'] ,single_entry_buffer['3029'] ,single_entry_buffer['3031'] ,single_entry_buffer['3019'] ,single_entry_buffer['3021'] ,single_entry_buffer['3023'] ,single_entry_buffer['3077'] ,single_entry_buffer['3079'] ,single_entry_buffer['3081'] ,single_entry_buffer['3109'] ,single_entry_buffer['2999'] ,single_entry_buffer['3001'] ,single_entry_buffer['3003'])    
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
 
 
if __name__ == '__main__':
    startReadingRegister()  




