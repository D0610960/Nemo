import time
import function


def start():
    uploadFlag = True
    while True:
        try:
            walkMode = function.getWalkMode(False)
            if walkMode != 'control':
                function.modifySensorData()
                
                # sensor detect and upload data per 10 minutes             
                if (int(time.strftime('%M')) % 10 == 0) and (uploadFlag == True):
                    function.uploadSensor()
                    uploadFlag = False
                elif (int(time.strftime('%M')) % 10 != 0) and (uploadFlag == False):
                    uploadFlag = True
            
        except Exception as ex:
            print(ex)
        finally:
            pass
        continue


if __name__ == '__main__':
    start()

