import time
# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'C:\Users\pedro\Desktop\Código\Final')
from mqtt_SSOP.clientSubscriber import subscribe


qualquercoisa = {
    "lastMessage" : 1,
    "somethingElse" : "Uma String"
}

if __name__ == "__main__":

    start_time = time.time()
    
    subscribe("toAsset/123", qualquercoisa, "ist190533")

    
    print("--- %s seconds ---" % (time.time() - start_time)) 
