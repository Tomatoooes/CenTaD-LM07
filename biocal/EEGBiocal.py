from psychopy import core, visual, event
#from math import sin, pi
import os #, numpy as np

from datetime import datetime

from _misc import constants, utils

class EEGBiocal:
    def __init__(self, win, task_duration, log):
        self.win = win       
        self.task_duration = task_duration
        self.fixation = visual.TextStim(win=self.win, text="+", height=64, units="pix")  # Fixation point
        self.log = log
        # Set up variables
        self.prompts = self.getPrompts()

    def getPrompts(self):
        eyes_closed = ('Biocal_eyes_closed', visual.TextStim(self.win, text=constants.MSG_BIOCAL_EC))
        eyes_opened = ('Biocal_eyes_open', visual.TextStim(self.win, text=constants.MSG_BIOCAL_EO))
        return [eyes_closed, eyes_opened]    
        
    def start(self):
        # Started calibration
        self.log.write(utils.get_current_time_micros() + "\t------ Starting Biocal EEG -------\n")

        # show prompts for each biocal tasks
        for event_logger, prompt in self.prompts:
            ''' Show Biocal Instruction Prompt on the screen '''
            # Draw text prompt on screen
            prompt.draw()
            self.win.flip()
            ''' Wait for user responses '''
            # Wait for user any key pressed then proceed
            event.waitKeys()   
            ''' notify start of biocal task '''
            #log messages
            self.log.write(utils.get_current_time_micros() + "\t" + event_logger + "\n")
            ''' clear the screen and show fixation point '''
            # clear screen
            self.win.flip()
            # draw fixation & update the screen
            self.fixation.draw()
            self.win.flip()
            
            event.waitKeys(maxWait=self.task_duration, keyList=["escape"])
            ''' notify beep for ending biocal task '''
            # end notification beep
            utils.notify_beep()
            #end of task            
            self.log.write(utils.get_current_time_micros() + "\tEnd " + event_logger + "\n")
            # clear the screen, update windows    
            self.win.flip()        
        # Finished biocal EEG tasks
        self.log.write(utils.get_current_time_micros() + "\t====== Finished Biocal EEG =========\n")

if __name__ == "__main__":   
    # Set up monitor
    useSecondaryMonitor = constants.SECOND_SCREEN #len(sys.argv) > 1 and sys.argv[1] == "-s"
    screenToUse = 1 if useSecondaryMonitor else 0
    monitorName = "secondary" if useSecondaryMonitor else "testMonitor"

    # Create window
    win = visual.Window(fullscr=constants.FULL_SCREEN, monitor=monitorName, color="black", screen=screenToUse, units="pix")
   
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    logging_filename = os.path.join(utils.get_log_file_path(), timestamp + ".log")

    with open(logging_filename, "w") as log:
        tester = EEGBiocal(win, task_duration=5., log=log)
        tester.start()
    
    log.close() 
    win.close()
    core.quit()