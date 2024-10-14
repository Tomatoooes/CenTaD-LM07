# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 17:00:56 2023

@author: CIL-SCSE
"""
from psychopy import event, core, data, visual
from _misc import fileHandling, constants, utils 
from datetime import datetime
import os#, time
# import glob
from stroop import fstroopy

''' Testing the Class '''
Logging_Dir = os.path.join(os.getcwd(), constants.LOG_DIR)
if not os.path.exists(Logging_Dir):
    os.makedirs(Logging_Dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")    
logging_filename = os.path.join(Logging_Dir, timestamp + "_runfstroop.log")
logFile = open(logging_filename, "w") 

if __name__ == "__main__":
    background = "Black"
    back_color = (0, 0, 0)
    textColor = "White"
    color_profile = {"background": "Black", "text":  "Red"}
    para_trials = {'num_blocks':  4,
                        'num_trials': 5,
                        'block_duration': 90,
                        'stroop_main': True,
                        }   
    # text_color = (1, 1, 1)
    experiment = fstroopy.Stroop(para_trials, color_profile, os.path.join(constants.DIR_MEDIA,constants.DIR_FACE))

    # experiment settings
    settings = {'Subid': '10', 'Experiment Version': 0.1,
                        'Sex': 'Male',
                        'Language': 'English', u'date':
                            data.getDateStr(format="%Y-%m-%d_%H:%M:%S")}

    settings[u'DataFile'] = u'' + os.getcwd() + os.path.sep + constants.LOG_DIR + os.path.sep + u'emo-face-stroop_' + data.getDateStr(format="%Y-%m-%d_%H-%M-%S") + u'.csv'
 

    instructions = fileHandling.read_instructions_file(os.path.join(constants.DIR_MEDIA, constants.DIR_FACE,"INSTRUCTIONS"), settings['Language'], settings['Language'] + "End")
    instructions_dict = experiment.create_instructions_dict(instructions)
    instruction_stimuli = {}

    window =  visual.Window(monitor="FaceStroopTask", size=[900, 500],  color=experiment.win_color, fullscr=False, units='pix', pos=[100,100])

    for inst in instructions_dict.keys():
        instruction, START, END = inst, instructions_dict[inst][0], instructions_dict[inst][1]
        instruction_stimuli[instruction] = experiment.create_instructions(window, instructions, START, END, color=textColor)

    # We don't want the mouse to show:
    event.Mouse(visible=False)
    # Practice Trials
    # display_instructions(start_instruction='Practice')
    # utils.display_wait_keypressed(window, 'Ready to practice emotional face stroop test, \n\n Press anykey to continue.....')
    utils.display_wait_timeout(window, 'Wait for 800 ms \n')
    # practice = experiment.create_trials(os.path.join(constants.DIR_MEDIA, constants.DIR_FACE,"practice_list.csv"))
    # experiment.running_practice_experiment(window, instruction_stimuli, logFile)
    # Test trials
    # experiment.display_instructions(logFile, instruction_stimuli, start_instruction='Test')
 #   utils.display_wait_keypressed(window, 'Ready to start actual emotional face stroop test, \n\n Press anykey to continue....')
    ''' Playing with High-arousal Video '''  
    experiment.running_actual_experiment(window, logFile)
    # Wait for user keypre
    utils.display_wait_timeout(window, 'Next Task with New Video is coming... Pls wait about 0.5 s.... \n')
    ''' Playing with Low-arousal video '''
    experiment.running_actual_experiment(window, logFile)
    # End experiment but first we display some instructions
    # experiment.display_instructions(logFile, start_instruction='End')
    window.close()
    logFile.close()
    core.quit()

