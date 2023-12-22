from pymodbus.client import ModbusTcpClient

# PLC Modbus TCP configuration
PLC_IP = "192.168.0.5"
PLC_PORT = 502  # Default Modbus TCP port is 502
PLC_UNIT_ID = 1  # Modbus unit ID (usually 1)
COIL_ADDRESS = 1280  # The address of the coil (bit) you want to write to

def write_single_bit(value_to_write):
    try:
        with ModbusTcpClient(PLC_IP, port=PLC_PORT) as client:
            # Write a single coil (bit) at the specified address
            result = client.write_coil(COIL_ADDRESS, value_to_write, unit=PLC_UNIT_ID)
            
            if result.isError():
                print(f"Modbus error: {result}")
            else:
                print(f"Successfully wrote {value_to_write} to coil {COIL_ADDRESS}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the value (True or False) you want to write to the coil
    value_to_write = True
    write_single_bit(1)
