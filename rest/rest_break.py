from psychopy import core, visual, event, constants as psychopy_constants
from _misc import constants, utils
import os
from datetime import datetime

def rest_deep_breathing(win, mov, log, time_out):
    #initialise the variables
   
    log.write(utils.get_current_time_micros()+"\tStart Deep Breathing Task\n")   
    
    #start playing the deep breathing video
    testTimer = core.MonotonicClock()
    while mov.status != psychopy_constants.FINISHED:
        mov.draw()
        win.flip()
        if testTimer.getTime() > time_out:
            #will end when the timing runs out
            break
    mov.stop()    
    log.write(utils.get_current_time_micros()+"\tCompleted Deep Breathing Task\n")
   


def start_auto_timeout(win, tStr, durationS, secondaryStr, log):
    #monotonic clock timer    
    timer = core.MonotonicClock()
    totalPauseTime = 0.0
    if durationS is None:
        durationS = 1.0
    ''' first message on screen '''
    log.write(utils.get_current_time_micros() + f"\t display and wait {durationS} seconds \n")  
    # Draw pause screen
    if tStr is not None:
        pause = visual.TextStim(win=win, text=tStr)
        pause.draw() # Draw text screen
        win.flip()   # flip the screen
    else:
        win.flip()    
    ''' wait for specified duration (# sec) '''    
    keys = event.waitKeys(maxWait=durationS, keyList=["escape"]) 
    while keys is not None: # and keys[0] == "q": # Pause
        pauseTimeStart = timer.getTime() 
        # Calculate remainder time for task
        totalPauseTime += timer.getTime() - pauseTimeStart
        remainder = durationS - (timer.getTime() - totalPauseTime)
        # Wait out remainder time for task
        keys = event.waitKeys(maxWait=remainder, keyList=["escape"])
    ''' second message on screen '''    
    if secondaryStr is not None:
        log.write(utils.get_current_time_micros() + f"\t display and wait {durationS} seconds \n") 
        cont = visual.TextStim(win=win, text=secondaryStr)
        cont.draw()
        win.flip()
        ''' wait for auto-timeout '''    
        event.waitKeys(maxWait=durationS)

def start_wait_keypressed(win, tStr, tDelayS, log):
    ''' Wait for specified seconds before next screen '''
    if tDelayS is not None and tDelayS > 0:
        core.wait(tDelayS)    
    ''' display message on screen '''
    if tStr is not None:
        pause = visual.TextStim(win=win, text=tStr)
        pause.draw() # Draw text screen
        win.flip()   # flip the screen
    else:
        win.flip() 
    ''' wait for keypressed forever '''
    event.waitKeys()

''' testing code '''        
Logging_Dir = os.path.join(os.getcwd(), constants.LOG_DIR)
if not os.path.exists(Logging_Dir):
    os.makedirs(Logging_Dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")    
logging_filename = os.path.join(Logging_Dir, timestamp + ".log")
logFile = open(logging_filename, "w")    

USE_EXTERNAL_SCREEN = False
FULL_SCREEN_MODE = False
if __name__ == "__main__":
    useSecondaryMonitor = USE_EXTERNAL_SCREEN #len(sys.argv) > 1 and sys.argv[1] == "-s"
    screenToUse = 1 if useSecondaryMonitor else 0
    monitorName = "secondary" if useSecondaryMonitor else "testMonitor"
    
    win = visual.Window(fullscr=FULL_SCREEN_MODE, monitor=monitorName, color="black", screen=screenToUse, units="pix")
    #start(win, "Press any key to continue...", None) 
    # start(win, "REST", 20.0)
    # start(win, "+")
    # start_auto_timeout(win, "BREAK", 10.0, "Press any key to continue...", logFile)
    
    rest_video = visual.MovieStim3(win, os.path.join(os.getcwd(), "_media", "relax_task", "breathing.mp4"), flipVert=False, flipHoriz=False, loop=True, size=(945,525))
    rest_deep_breathing(win, rest_video, logFile, 24)
    
    win.close()
    