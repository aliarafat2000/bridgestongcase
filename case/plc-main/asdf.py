import mysql.connector





def insert_into_mysql_2():
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
        values = ("ad",1.6,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1)    
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
 
insert_into_mysql_2()