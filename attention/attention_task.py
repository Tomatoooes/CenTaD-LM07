from psychopy import core, visual, event
from datetime import datetime
from attention import flanker, white_noise
import os #, sys
from _misc import constants, utils
import numpy as np

# message1 = "Attention task: \n\
# A cross will be presented on the screen together with a short *Beep* sound. Focus on the cross. \n\n\
# After a while, the cross will be replaced by 5 arrows that point either left or right. \n\n\
# Find the direction that majority of the arrows are pointing towards. \n\n\
# Use <4> to respond left and <6> to respond right. \n\n\
# Press any key once you understand this task..."
# message2 = "Inattention task: \n\
# A blank screen will be presented to you. \n\n\
# Follow the edge of the screen and look around the blank screen. Try to relax your mind. \n\n\
# Press any key once you understand this task..."
# message3 = "Between each task, a visual cue will be provided for 2 seconds, after which the task will start automatically. \n\n\
# If you are ready to begin, press any key..."

class AttentionTask:
    def __init__(self, win, trials, media_abs_path):
        self.win = win
        self.attTask = flanker.FlankerTask(self.win, trials, media_abs_path=media_abs_path)
        self.inaTask = white_noise.WhiteNoise(self.win, media_abs_path)
        # notification message
        self.transitToAttention = visual.TextStim(win=self.win, text="Attention: Flanker task is starting")
        self.transitToInattention = visual.TextStim(win=self.win, text="Inattention: White Noise video is starting")
        # self.trials_all_blocks = self.generate_random_trials(self)#
        
    # def generate_random_trials(self):
        all_trials = [None]*constants.N_TRIALS_PER_BLOCK*constants.N_ATT_BLOCKS
        n_stim_repeat = int(len(all_trials)/len(constants.STIM_DICT))
        n_stim_extra = len(all_trials) - n_stim_repeat*len(constants.STIM_DICT)
        
        trials_extra = list(np.random.choice(np.array(list(constants.STIM_DICT.keys())), size=n_stim_extra, replace=False))
        all_trials = list(constants.STIM_DICT.keys())*n_stim_repeat + trials_extra
        self.trials_all_blocks = np.array(all_trials).reshape(constants.N_ATT_BLOCKS, constants.N_TRIALS_PER_BLOCK).tolist()
        
        
    def trial(self, logFile):
        logFile.write(utils.get_current_time_micros() + "\t Attention Task Trial Started \n")
        trial_msg = ("trail session", visual.TextStim(self.win, text="This is a flanker trial session\n\nPress 'any key' to continue..."))
        trial_msg[1].draw()
        self.win.flip()        
        event.waitKeys()
        self.win.flip()
        logFile.write(utils.get_current_time_micros() + "\t Flanker Trial,User Key Pressed \n")

        self.attTask.start(logFile, constants.DEFAULT_BLOCK_ID) 
        self.win.flip()

        trial_end_msg = ("trail session", visual.TextStim(self.win, text="This is the end of flanker trial session.\n\nPress 'any key' to continue."))
        trial_end_msg[1].draw()
        self.win.flip()
        event.waitKeys()
        self.win.flip()
        logFile.write(utils.get_current_time_micros() + "\t After keys Pressed, Attention Task Trial Finished \n")
           
    def start(self, log):
        log.write(utils.get_current_time_micros() + "\tStart Attention Task Blocks\n")
        # self.displayStartPrompt() # Display prompt before starting

        for iBlk in range(1, constants.N_ATT_BLOCKS+1): 
            # display 2s of attention task message
            self.displayTransition(attention=True)

            # attention Flanker task
            log.write(utils.get_current_time_micros() + "\tStart flanker task\tblock: " + str(iBlk) + "\n")
            self.attTask.start(log, iBlk, stims_per_blk=self.trials_all_blocks[iBlk-1])
            
            # display 2s of inattention task message
            self.displayTransition(attention=False)

            # Inattention task
            log.write(utils.get_current_time_micros() + "\tStart inattention task\tblock: " + str(iBlk) + "\n")
            self.inaTask.start(log)

        log.write(utils.get_current_time_micros() + "\tEnd Attention Task Blocks\n")

    def displayTransition(self, attention): # this part displays the main experiment
        if attention:
            self.transitToAttention.draw()
        else:
            self.transitToInattention.draw()
        self.win.flip()
        core.wait(constants.TIME_WAIT_TRANSITION)
        self.win.flip() # Show blank screen

# =============================================================================
#     def displayStartPrompt(self): #this part displays the starting part of the programme
#         # First message
#         self.text1.draw()
#         self.win.flip()
#         event.waitKeys()
# 
#         # Second message
#         self.text2.draw()
#         self.win.flip()
#         event.waitKeys()
# 
#         # Third message
#         self.text3.draw()
#         self.win.flip()
#         event.waitKeys()
#         self.win.flip() # show blank screen
# =============================================================================
""" parameters """
Logging_Dir = os.path.join(os.getcwd(), constants.LOG_DIR)
if not os.path.exists(Logging_Dir):
    os.makedirs(Logging_Dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")    
logging_filename = os.path.join(Logging_Dir, timestamp + ".log")
logFile = open(logging_filename, "w")    

USE_EXTERNAL_SCREEN = False
FULL_SCREEN_MODE = False


if __name__ == "__main__":
    useSecondaryMonitor = USE_EXTERNAL_SCREEN
    screenToUse = 1 if useSecondaryMonitor else 0
    monitorName = "secondary" if useSecondaryMonitor else "testMonitor"
    win = visual.Window(fullscr=FULL_SCREEN_MODE, monitor=monitorName, color="black", screen=screenToUse, units="pix")
    
    trialID = [1, 3, 0, 2]#1, 2, 3, 2, 0, 1]
    # random.shuffle(trialID)
    tester = AttentionTask(win, trialID, None)
    with open("test.log", "w") as log:
        tester.trial(log)
        # tester.start(log)
        
    win.close()
    core.exit()