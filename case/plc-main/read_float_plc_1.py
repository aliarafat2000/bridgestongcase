from pymodbus.client import ModbusTcpClient
from time import sleep
import struct
# PLC Modbus TCP configuration
PLC_IP = "192.168.7.5"
PLC_PORT = 502  # Default Modbus TCP port is 502
PLC_UNIT_ID = 1 # Modbus unit ID (usually 1)
# REGISTER_ADDRESS = 4096  # The address of the register you want to read

register_addresses = [4097]


def read_single_register(register):
    try:
        with ModbusTcpClient(PLC_IP, port=PLC_PORT) as client:
            # Read a single holding register at the specified address
            result = client.read_holding_registers(register, 2, unit=PLC_UNIT_ID)
            
            if result.isError():
                print(f"Modbus error: {result}")
            else:
                # Process the data from the register
                combined_value = (result.registers[0] << 16) + result.registers[1]
                float_value = struct.unpack('>f', struct.pack('>I', combined_value))[0]
                print(f"Recieved float value from PLC: {float_value}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        while True:
            for register_address in register_addresses:
                read_single_register(register_address)
            
            
            
            print("\n")
            sleep(1)
    except KeyboardInterrupt:
        print("cleared")
    except Exception as e:
        print("There was above error")

