import threading
import time
from em1220h import data_collection
from plc1 import read_single_register
from RspiHealth import deviceMonitoring

if __name__ == "__main__":
    try:
        thread1 = threading.Thread(target=data_collection)
        thread2 = threading.Thread(target=read_single_register)
        thread3 = threading.Thread(target=deviceMonitoring)
        
        thread1.start()
        thread2.start()
        thread3.start()
            
    except KeyboardInterrupt:
        thread1.join()
        thread2.join()
        thread3.join()
        print("cleared")
    except Exception as e:
        print("There was above error",e)
