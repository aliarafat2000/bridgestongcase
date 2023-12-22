from pymodbus.client import ModbusTcpClient

PLC_IP = "192.168.0.5"
PLC_PORT = 502  # Typically 502 for Modbus TCP
PLC_UNIT_ID = 1  # Modbus unit ID (usually 1)

def read_plc_registers():
    try:
        with ModbusTcpClient(PLC_IP, port=PLC_PORT) as client:
            # Read holding registers starting from address 0, and read 10 registers
            result = client.read_holding_registers(4097, 4352, unit=PLC_UNIT_ID)
            
            if result.isError():
                print(f"Modbus error: {result}")
            else:
                # Process the data from the registers
                data = result.registers
                print(f"Received data from PLC: {data}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_plc_registers()