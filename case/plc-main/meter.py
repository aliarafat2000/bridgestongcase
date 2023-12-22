import minimalmodbus
import serial
import time
import struct

instrument = minimalmodbus.Instrument('/dev/ttyUSB0',5)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_EVEN
instrument.serial.stopbits = 1

em1220h_addresses = [3027, 3029, 3031, 3019, 3021, 3023, 3077, 3079, 3081, 3109, 2999, 3001, 3003]

single_entry_buffer = {}


for register in em1220h_addresses:

    data = instrument.read_float(register,functioncode=3)
    single_entry_buffer[str(register)] = data
# leb = bytes([data[1]&0xFF, data[1]>>8, data[1]&0xFF, data[1]>>8])
# f = struct.unpack('<f', leb)[0]
    print(single_entry_buffer)

