# In[1]:


import multiprocessing as mp
import virtual_assistant as va
import run_others as ro
import camera as ca
import function as func
import time


# In[2]:

if __name__ == '__main__':
    func.init()
    m = mp.Value('i', 1)
    q = mp.Queue()
    try:
        p1 = mp.Process(target=ro.start, args=(q, m,))
        p2 = mp.Process(target=va.start, args=(q, m,))
        p3 = mp.Process(target=ca.start, args=(m,))
        p1.start()
        p2.start()
        p3.start()
        p2.join()
    except Exception as ex:
         print(ex)
    finally:
        print('Close Program')
        p1.terminate()
        p2.terminate()
        p3.terminate()
        time.sleep(0.1)
        p1.join()
        p2.join()
        p3.join()
