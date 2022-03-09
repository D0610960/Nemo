import threading
import ctypes
import predict
import walk
import detect
import function
import time

def terminate(thread):
    if not thread.is_alive():
        return
    
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(SystemExit))
    if res == 0:
        raise ValueError('invalis thread id')
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SerAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    
if __name__ == '__main__':
    walk.init()

    try:
        t1 = threading.Thread(target=walk.start)
        t2 = threading.Thread(target=predict.start)
        t3 = threading.Thread(target=detect.start)
        t1.start()
        t2.start()
        t3.start()
        print('total thread: ', threading.active_count())
    except Exception as ex:
        pass
    
        


