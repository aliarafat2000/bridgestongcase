from pymodbus.client import ModbusTcpClient

# PLC Modbus TCP configuration
PLC_IP = "192.168.0.5"
PLC_PORT = 502  # Default Modbus TCP port is 502
PLC_UNIT_ID = 1  # Modbus unit ID (usually 1)
REGISTER_ADDRESS = 4100  # The address of the register you want to write to

def write_to_register(value_to_write):
    try:
        with ModbusTcpClient(PLC_IP, port=PLC_PORT) as client:
            # Write to a single holding register at the specified address
            result = client.write_registers(REGISTER_ADDRESS, [value_to_write], unit=PLC_UNIT_ID)
            
            if result.isError():
                print(f"Modbus error: {result}")
            else:
                print(f"Successfully wrote {value_to_write} to register {REGISTER_ADDRESS}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the value you want to write to the register
    value_to_write = 123
    write_to_register(value_to_write)