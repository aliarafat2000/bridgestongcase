from pymodbus.client import ModbusTcpClient
from time import sleep
import mysql.connector

# PLC Modbus TCP configuration
PLC_IP = "192.168.7.5"
PLC_PORT = 502  # Default Modbus TCP port is 502
PLC_UNIT_ID = 1  # Modbus unit ID (usually 1)
# REGISTER_ADDRESS = 4096  # The address of the register you want to read

register_addresses = [4096, 4097, 4098, 4099]
float_addresses = []

def read_single_register(register):
    while True:
        single_entry_buffer = {}
        try:
            with ModbusTcpClient(PLC_IP, port=PLC_PORT) as client:
                # Read a single holding register at the specified address
                for register_address in register_addresses:
                    result = client.read_holding_registers(register, 1, unit=PLC_UNIT_ID)
                    
                    if result.isError():
#                         print(f"Modbus error: {result}")
                        single_entry_buffer[str(register_address)] = None
                    else:
                        # Process the data from the register
                        data = result.registers[0]
    #                     print(f"{register}: {data}", end=' ')
                        single_entry_buffer[str(register_address)] = data
                        
                for register_address in float_addresses:
                    result = client.read_holding_registers(register, 2, unit=PLC_UNIT_ID)
                    
                    if result.isError():
#                         print(f"Modbus error: {result}")
                        single_entry_buffer[str(register_address)] = None
                    else:
                    # Process the data from the register
                        combined_value = (result.registers[0] << 16) + result.registers[1]
                        float_value = struct.unpack('>f', struct.pack('>I', combined_value))[0]
    #                     print(f"Recieved float value from PLC: {float_value}")
                        single_entry_buffer[str(register_address)] = float_value

        except Exception as e:
            print(f"Error: {e}")
        single_entry_buffer['time'] = time.strftime("%Y-%m-%d %H:%M:%S")
#         print("="*50)
#         print(single_entry_buffer)
        insert_into_mysql_2(single_entry_buffer)
    
        single_entry_buffer.clear()
        print("plc entery done!")
        
        

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




if __name__ == "__main__":
    try:
#         while True:
#             for register_address in register_addresses:
#                 read_single_register(register_address)
            
            
            
            print("\n")
            sleep(1)
    except KeyboardInterrupt:
        print("cleared")
    except Exception as e:
        print("There was above error")
