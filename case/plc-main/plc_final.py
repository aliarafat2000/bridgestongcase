#create table
import mysql.connector


def create_table():
    try:
        connection = mysql.connector.connect( 
            host="193.203.184.2",
            user="u295327377_madical_user",
            password="5G27zBkBOZ6w",
            database="u295327377_madical_db",
            port=3306
        )
        
        cursor = connection.cursor()        
        
        query = "CREATE TABLE IF NOT EXISTS device_health(time VARCHAR(255), CPU_Temperature FLOAT(8,2) , CPU_Usage FLOAT(8,2), Memory_Usage FLOAT(8,2))"
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
  
if __name__ == "__main__":
    try:
        create_table()
            
    except KeyboardInterrupt:
        print("cleared")
    except Exception as e:
        print("There was above error",e)

