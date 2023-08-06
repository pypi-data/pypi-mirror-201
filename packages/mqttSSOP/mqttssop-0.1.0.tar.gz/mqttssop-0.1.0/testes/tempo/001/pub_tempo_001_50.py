import time
# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'C:\Users\pedro\Desktop\Código\Final')
from mqtt_SSOP.clientPublisher import publish


if __name__ == "__main__":

    start_time = time.time()
    
    for i in range(50):
        time.sleep(0.01)
        publish("toAsset/123", "Message " + str(i), "ist190532")


    
    print("--- %s seconds ---" % (time.time() - start_time)) 


