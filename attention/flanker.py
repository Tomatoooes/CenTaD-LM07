from psychopy import core, visual, sound, event
#import event
from datetime import datetime
import time, os, random as rnd #, sys #, numpy as np
#from math import sin, pi
#from psychopy.visual.image import ImageStim
from _misc import constants, utils

Exp_Img_Path = os.path.join(os.getcwd(), "_images")


""" parameters """
# keyList = ["escape", "left", "num_4", "right", "num_6"]   # keys to be used for responses
#flankerPos = [-300, -150, 150, 300]
#stimStrDict = {'00':'neutral-congruent.jpg', '01':'smile-congruent.jpg', '10':'neutral-incongruent.jpg', '11':'smile-incongruent.jpg'}
# #RT_TIME_OUT = 1.2 #1.2 s timeout of waiting user keypressed responses
# BLOCK_TIME_OUT = 15.0 #15s for single task block
# #REST_TIME_OUT = 0.8 #800 ms before next fixation
# FIXATION_TIME_OUT = 0.8
# #STIMULUS_TIME_OUT = 0.3
# ISI_TIME_OUT = 1.2
# N_TRIALS = round(BLOCK_TIME_OUT/(FIXATION_TIME_OUT + ISI_TIME_OUT)) + 1 #8+1 to ensure 
# N_IMG = 4



class FlankerTask:
    def __init__(self, win, trials, media_abs_path=None):
        self.win = win
        self.trialNum = 0
        self.fixation = visual.TextStim(win=self.win, text="+", height=64, units="pix") # Fixation point
        self.isCongruency = None#[None] * N_TRIALS #[0,1,0,0,1] = [L,R,L,L,R]  => string[0]
        self.isSmile = None#[None] * N_TRIALS #[1,1,0,1,0] => string[1]
        #self.stimTrials = trials #['01', '11', '00', '01', '10']
        if trials is None:
            self.stimIdx = constants.DEFAULT_STIM_ID_PER_BLOCK    
        else:
            self.stimIdx = trials #[1, 3, 0, 1, 2, 3, 2, 0]
        if media_abs_path is None:
            ATT_DIR = os.path.join(constants.DIR_MEDIA, constants.DIR_ATT)
        else:
            ATT_DIR = media_abs_path
                
        self.stimCS = visual.ImageStim(win=self.win, image=os.path.join(ATT_DIR, constants.STIM_DICT.get(constants.STIM_CS_KEY))) #CS - congruent-smile
        self.stimCN = visual.ImageStim(win=self.win, image=os.path.join(ATT_DIR, constants.STIM_DICT.get(constants.STIM_CN_KEY))) #CN - congruent-neutral
        self.stimIS = visual.ImageStim(win=self.win, image=os.path.join(ATT_DIR, constants.STIM_DICT.get(constants.STIM_IS_KEY))) #IS - incongruent-smile
        self.stimIN = visual.ImageStim(win=self.win, image=os.path.join(ATT_DIR, constants.STIM_DICT.get(constants.STIM_IN_KEY))) #IN - incongruent-neutral
        #self.pause = visual.TextStim(win=self.win, text="Paused")
        self.keyText = visual.TextStim(win=self.win, text=constants.MSG_KEY_PRESSED, pos=(0, -200))
        self.welcomeImg = visual.ImageStim(win=self.win, image=os.path.join(ATT_DIR, constants.IMG_ATT_INST))#, size=self.win.size/2, units="pix")
        self.welcomeTxt = visual.TextStim(win=self.win, text="Starting Flanker Trial \n\n Press 'any key' to continue when ready...")
        self.restTxt = visual.TextStim(win=self.win, text="Get Ready for next trial ...")
       
   
    def start(self, logFile, blkID, stims_per_blk=None):
        # utils.write_log_header(logFile, None)
        #timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        #logging_filename = os.path.join(logDir, timestamp + ".log")
        #logFile = open(logging_filename, "w")
        # Log experiment start
        logFile.write(utils.get_current_time_micros() + "\tStart Flanker task [ATT]\n")
        # Start block             
        # Show initial instruction screen OR simple text depending on block ID
        # outlet.push_sample([str(41)])
        if blkID == constants.DEFAULT_BLOCK_ID:
            logFile.write(utils.get_current_time_micros() + "\t First Block, First Trial \n")
            #Display instruction image screen
            self.welcomeImg.draw()
            self.keyText.draw()
            self.win.flip()
        else:
            logFile.write(str(time.time()) + "\t Subsequent Block, First Trial \n")
            #Display simple text screen
            self.welcomeTxt.text = "Starting Flanker Task (Blk-"+str(blkID)+") \n\n Press 'any key' to continue when ready..."
            self.welcomeTxt.draw()
            self.win.flip()
        # Wait for any key pressed to continue
        event.waitKeys()

        # Start counting the time
        totalPauseTime = 0.0
        testTimer = core.MonotonicClock()
        #for iTrial in range(0, N_TRIALS):
        iTrial = self.trialNum
        curTime = testTimer.getTime()
        while curTime - totalPauseTime <=  constants.TIME_ATT_INA_BLOCK:    
            # out of loop if time is beyond the time out
            #print('Trial '+ str(iTrial+1))
            # Show fixation FIXATION_TIME_OUT s 
            # nextFlip = self.win.getFutureFlipTime(clock="ptb")
            #self.alertSound.play(when=nextFlip)         
            utils.notify_beep()
            self.fixation.draw()
            self.win.flip()            
            # outlet.push_sample([str(42)])
            core.wait(constants.TIME_FIXATION)
            # replace the default stim ids with randomized blocks
            if stims_per_blk is not None:
                self.stimIdx = stims_per_blk
            else:
                # reshuffle the stim ids
                rnd.shuffle(self.stimIdx)
            #self.stimPresent.draw()  
            if iTrial < len(self.stimIdx) and iTrial <= constants.N_TRIALS_PER_BLOCK:
                if self.stimIdx[iTrial] == 0:
                    self.stimCS.draw() #congruent-smile
                    self.isCongruency = True
                    self.isSmile = True
                elif self.stimIdx[iTrial] == 1:
                    self.stimCN.draw() #congruent-neutral
                    self.isCongruency = True
                    self.isSmile = False
                elif self.stimIdx[iTrial] == 2:
                    self.stimIS.draw() #incongruent-smile
                    self.isCongruency = False
                    self.isSmile = True
                else:
                    self.stimIN.draw() #incongurent-neutral
                    self.isCongruency = False
                    self.isSmile = False
                logFile.write(utils.get_current_time_micros() + "\t Trial-"+ str(iTrial+1) + "\t Stimulus: " + constants.STIM_DICT.get(self.stimIdx[iTrial]) + "\n")
            else:
                break
            # update screen        
            self.win.flip()            

            sTime = time.time()           
            keys = event.waitKeys(maxWait=constants.TIME_ISI, keyList=constants.RESP_KEYS)
            self.win.flip() # Reset to blank screen
            # Log based on responses
            if keys is None: # No response collected
                logFile.write(utils.get_current_time_micros()  + "\t Trial-"+ str(iTrial+1)+ "\t Timeout \t fail \n")               
            elif "escape" in keys:
                logFile.write(utils.get_current_time_micros() + "\t exit pressed\n")
                break
            #elif "p" in keys: # Pause
            #    log.write(str(time.time()) + "\tPause\n")
            #    totalPauseTime += self.pauseRoutine(log)
            else:
                #user pressed L/R key to update the trial responses
                # outlet.push_sample([str(43)])
                if self.isKeyResponseCorrect(keys[0], self.isCongruency):
                    logFile.write(utils.get_current_time_micros() + "\t Trial-"+ str(iTrial+1) + "\t keypressed: " + keys[0] + "\t correct\n")
                else:
                    logFile.write(utils.get_current_time_micros() + "\t Trial-"+ str(iTrial+1) + "\t keypressed: " + keys[0] + "\t incorrect\n")

            # response time    
            rt = time.time()  - sTime    
            logFile.write(utils.get_current_time_micros() + "\tTrial-"+ str(iTrial+1) + "\tResponse Time "+str(rt)+"s \n")
            # wait for next trial
            self.restTxt.draw()
            self.win.flip()
            core.wait(constants.TIME_ISI - rt)
            #increment trial counts
            iTrial = iTrial + 1
            curTime =  testTimer.getTime()
        #Reset # trial    
        self.trialNum = 0
        self.win.flip()   
        # Log experiment end and close file
        logFile.write(utils.get_current_time_micros() + "\tEnd Flanker task [ATT]\n")
        #logFile.close()         

    def isKeyResponseCorrect(self, keyPress, congurency):
        if congurency:
            direction = "left"
        else:
            direction = "right"
        return (keyPress == direction or 
        ((keyPress == "num_4" and direction == "left") or 
        (keyPress == "num_6" and direction == "right")))

# =============================================================================
#     def pauseRoutine(self, log):
#         pauseTimer = core.MonotonicClock()
#         # Draw pause screen
#         self.pause.draw()
#         self.win.flip()
#         event.waitKeys(keyList=["q"]) # Wait for unpause
#         self.win.flip() # Draw blank screen
#         log.write(str(time.time()) + "\tUnpause\n")
#         return pauseTimer.getTime()
# =============================================================================

###### end of Class #########

""" parameters """
Logging_Dir = os.path.join(os.getcwd(), constants.LOG_DIR)
if not os.path.exists(Logging_Dir):
    os.makedirs(Logging_Dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")    
logging_filename = os.path.join(Logging_Dir, timestamp + ".log")
logFile = open(logging_filename, "w")    

USE_EXTERNAL_SCREEN = False
FULL_SCREEN_MODE = False

#lsl stream
# info = StreamInfo('Muse2MarkerStream', 'Markers', 1, 0, 'string', 'muse2event')
# outlet = StreamOutlet(info)

if __name__ == "__main__":
    useSecondaryMonitor = USE_EXTERNAL_SCREEN#len(sys.argv) > 1 and sys.argv[1] == "-s"
    screenToUse = 1 if useSecondaryMonitor else 0
    monitorName = "secondary" if useSecondaryMonitor else "testMonitor"
    win = visual.Window(fullscr=FULL_SCREEN_MODE, monitor=monitorName, color="black", screen=screenToUse, units="pix")
    #tester = FlankerTask(win, ['00','10','11','01','11'])
    trialID = [1, 3, 0, 2]#1, 2, 3, 2, 0, 1]
    random.shuffle(trialID)
    tester = FlankerTask(win, trialID)
    
    tester.start(logFile, 1)
    win.close()
    