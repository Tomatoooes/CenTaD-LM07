# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 21:26:44 2022

@author: CIL-SCSE
"""
from psychopy import core, visual#, event
from nback import nback_task
from _misc import constants
import os
from datetime import datetime

IS_TRIAL = True
IS_ACTUAL = not IS_TRIAL

class WorkloadTask:
    def __init__(self, win, media_abs_path):
        self.win = win
        self.stim_file_path = media_abs_path
        self.highBuffer = [None] * 3
        self.lowBuffer = [None] * 3
        self.highBuffer[0], self.highBuffer[1], self.highBuffer[2] = nback_task.generateWorkloadBuffer(win, constants.HIGH_WORKLOAD, media_abs_path)
        self.lowBuffer[0], self.lowBuffer[1], self.lowBuffer[2] = nback_task.generateWorkloadBuffer(win, constants.LOW_WORKLOAD, media_abs_path)
        
        
    def start_workload(self, logger):        
        ''' Low workload trial and actual    '''
        nback_task.workloadTaskSeq(self.win, logger, self.highBuffer, self.lowBuffer)              
# =============================================================================
#         # LWL task instruction
#         nback_task.workLoadInst(self.win, constants.LOW_WORKLOAD)                
#         # Low workload trials
#         index_lwl, trialIndex_lwl = nback_task.workloadTask(self.win, IS_TRIAL, self.sequence_lwl, self.corrAns_lwl, self.probe_lwl, self.probeImg_lwl, constants.LOW_WORKLOAD, 0, 0)
#         nback_task.completeInst(self.win, IS_TRIAL)
#         # Low workload actual        
#         nback_task.workloadTask(self.win, IS_ACTUAL, self.sequence_lwl, self.corrAns_lwl, self.probe_lwl, self.probeImg_lwl, constants.LOW_WORKLOAD, index_lwl, trialIndex_lwl)
#         nback_task.completeInst(self.win, IS_ACTUAL)
# =============================================================================
   
    # def start_highworkload(self, logger):
    #     ''' High workload trial and actual '''
# =============================================================================
#         #HWL task instruction
#         nback_task.workLoadInst(self.win, constants.HIGH_WORKLOAD)
#         # High workload trials
#         index, trialIndex = nback_task.workloadTask(self.win, IS_TRIAL, self.sequence_hwl, self.corrAns_hwl, self.probe_hwl, self.probeImg_hwl, constants.HIGH_WORKLOAD, 0, 0)
#         nback_task.completeInst(self.win, IS_TRIAL)
#         # High workload actual
#         nback_task.workloadTask(self.win, IS_ACTUAL, self.sequence_hwl, self.corrAns_hwl, self.probe_hwl, self.probeImg_hwl, constants.HIGH_WORKLOAD, index, trialIndex)
#         nback_task.completeInst(self.win, IS_ACTUAL)
# =============================================================================

""" parameters """
Logging_Dir = os.path.join(os.getcwd(), constants.LOG_DIR)
if not os.path.exists(Logging_Dir):
    os.makedirs(Logging_Dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")    
logging_filename = os.path.join(Logging_Dir, timestamp + ".log")
logFile = open(logging_filename, "w")    

USE_EXTERNAL_SCREEN = False
FULL_SCREEN_MODE = True


if __name__ == "__main__":
    useSecondaryMonitor = USE_EXTERNAL_SCREEN
    screenToUse = 1 if useSecondaryMonitor else 0
    monitorName = "secondary" if useSecondaryMonitor else "testMonitor"
    win = visual.Window(fullscr=FULL_SCREEN_MODE, monitor=monitorName, color="black", screen=screenToUse, units="pix")
    
    with open("test.log", "w") as log:
        tester = WorkloadTask(win, os.path.join(os.getcwd(), constants.DIR_MEDIA, constants.DIR_WKL))
        tester.start_workload(log)
        # tester.start(log)
        
    win.close()
    core.quit()