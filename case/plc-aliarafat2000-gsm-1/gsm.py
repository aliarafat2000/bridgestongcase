import serial
import time

def send_at_command(command, timeout=1):
    ser.write(command.encode() + b'\r\n')
    time.sleep(timeout)
    response = ser.read(ser.in_waiting).decode('utf-8')
    return response

# Configure serial port
ser = serial.Serial("/dev/ttyS0", 9600, timeout=1)

# Check if the module is responding
response = send_at_command("AT")
print("Response to AT command:", response)

# Set up the module for making a call
send_at_command("AT+CMGF=1")  # Set SMS mode to text
send_at_command('AT+CMGS="9170900601"')  # Replace PHONE_NUMBER with the desired phone number
send_at_command("Hello from Raspberry Pi!")  # Your message
ser.write(bytes([26]))  # Send Ctrl+Z to send the SMS

# Close the serial port
ser.close()
