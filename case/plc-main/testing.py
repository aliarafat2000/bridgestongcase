#create table
import mysql.connector


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
        
        query = "CREATE TABLE IF NOT EXISTS energy_em1220h(time, id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT, email VARCHAR(255)) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        print("entering")
        cursor.execute(query)
        print("exiting")
        connection.commit()
        print("Data Table created MySQL successfully")
       
    
    except Exception as e:
        print(str(e))
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
