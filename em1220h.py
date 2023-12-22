import minimalmodbus
import datetime
import time
import csv
import os
import pymysql
import math

# Define Your Serial Port, Connection Details, Parameters, And Address
serial_port = '/dev/ttyUSB0'
slave_address = 5
baud_rate = 9600
parity = minimalmodbus.serial.PARITY_EVEN

parameters = ['Date', 'V1', 'V2', 'V3', 'V12', 'V23', 'V31', 'PF1', 'PF2', 'PF3', 'F', 'A1', 'A2', 'A3']
address = ['3027', '3029', '3031', '3019', '3021', '3023', '3077', '3079', '3081', '3109', '2999', '3001', '3003']

byte_size = 8

def replace_nan_with_zero(value):
    return 0.0 if math.isnan(value) else value

def get_current_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_to_csv(data, file_name):
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if not file_exists:
            csvwriter.writerow(parameters)
        csvwriter.writerows(data)

def save_to_mysql(data):
    try:
        connection = pymysql.connect(
            host="193.203.185.104",
            user="u295327377_ems_user",
            password="EmsDB@123!@#",
            database="u295327377_ems_db",
            port=3306
        )

        cursor = connection.cursor()

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS s1r2 (
            {', '.join([f'{param} FLOAT' for param in parameters])}
        )
        """
        cursor.execute(create_table_query)

        for row_data in data:
            row_data[1:] = [float(value) for value in row_data[1:]]
            placeholders = ', '.join(['%s'] * 14)
            sql = f"INSERT INTO s1r2 (Date, V1, V2, V3, V12, V23, V31, PF1, PF2, PF3, F, A1, A2, A3) VALUES ({placeholders})"
            cursor.execute(sql, row_data)

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("MySql Error:", str(e))

def initialize_instrument():
    try:
        instrument = minimalmodbus.Instrument(serial_port, slave_address)
        instrument.serial.baudrate = baud_rate
        instrument.serial.bytesize = byte_size
        instrument.serial.parity = parity
        return instrument
    except Exception as e:
        print("Failed To Initialize Instrument:", str(e))
        return None

def read_instrument_data(instrument):
    row_data = [get_current_datetime()]
    try:
        for i in address:
            register_value = instrument.read_float(int(i), functioncode=3)
            row_data.append(replace_nan_with_zero(register_value))
        return row_data
    except Exception as e:
        print("Error Reading Meter Data:", str(e))
        return None

def data_collection():
    instrument = initialize_instrument()

    while True:
        try:
            if instrument:
                row_data = read_instrument_data(instrument)
                if row_data:
                    save_to_csv([row_data], 'em1220h.csv')
                    save_to_mysql([row_data])
                    print("Data Inserted Into Database and File Successfully")

            print('*' * 50)
            time.sleep(1)
        except Exception as e:
            print("Data Collection Error:", str(e))
            time.sleep(1)

if __name__ == "__main__":
    data_collection()
