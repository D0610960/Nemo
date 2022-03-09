import time
import function


def start():
    while True:
        global moveCnt
        global rnum
        global moveflag
        try:
            walkMode, circleMode, adding = function.getWalkMode(True)
            
            # walking mode: control
            if walkMode == 'control':
                function.control()
            else:                
                # when alarm is ringing or memo is reminding
                if circleMode:
                    function.circle()
                # when user is adding neew member's photos
                elif adding:
                    function.static()
                else:
                    # walking mode: auto
                    if walkMode == 'auto':
                        if moveCnt > rnum:
                            rnum = function.randomMove()
                            moveflag = not moveflag
                            moveCnt = 0
                        else:
                            if moveflag:
                                function.auto()
                            else:
                                function.static()
                    # walking mode: static
                    elif walkMode == 'static':
                        function.static()
                    else:
                        pass

            time.sleep(0.1)
        except Exception as ex:
            print(ex)
            function.static()
        finally:
            function.static()
        continue


def init():
    print("NEMO starting...")
    global moveCnt
    global rnum
    global moveflag

    moveCnt = 0
    rnum = function.randomMove()
    moveflag = True
    function.init()

if __name__ == '__main__':
    init()
    start()
