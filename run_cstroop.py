# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 09:31:34 2023

@author: CIL-SCSE
"""
from psychopy import event, core, data, visual
from _misc import fileHandling, constants, utils 
from datetime import datetime
import os, time
from stroop import cstroopy

''' Testing the Class '''
Logging_Dir = os.path.join(os.getcwd(), constants.LOG_DIR)
if not os.path.exists(Logging_Dir):
    os.makedirs(Logging_Dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")    
logging_filename = os.path.join(Logging_Dir, timestamp + "_runcstroop.log")
logFile = open(logging_filename, "w") 

if __name__ == "__main__":
    background = "Black"
    back_color = (0, 0, 0)
    textColor = "White"
    color_profile = {"background": "Black", "text":  "White"}
    # para_trials = {'num_blocks':  3,
    #                     'num_trials': 60,
    #                     'block_duration': 200,
    #                     }   
    para_trials = {'num_blocks':  2,
                        'num_trials': 5,
                        'block_duration': 15,
                        } 
    # text_color = (1, 1, 1)
    experiment = cstroopy.Stroop(para_trials, color_profile, constants.DIR_COLOR)

    # experiment settings
    settings = {'Subid': '10', 'Experiment Version': 0.1,
                        'Sex': 'Male',
                        'Language': 'English', u'date':
                            data.getDateStr(format="%Y-%m-%d_%H:%M:%S")}

    settings[u'DataFile'] = u'' + os.getcwd() + os.path.sep + constants.LOG_DIR + os.path.sep + u'color-stroop_' + data.getDateStr(format="%Y-%m-%d_%H-%M-%S") + u'.csv'
    # language = settings['Language']

    window =  visual.Window(monitor="ColorStroopTask",   color=experiment.win_color, fullscr=False)

    instructions = fileHandling.read_instructions_file(os.path.join(constants.DIR_MEDIA, constants.DIR_COLOR,"INSTRUCTIONS"), settings['Language'], settings['Language'] + "End")
    instructions_dict = experiment.create_instructions_dict(instructions)
    instruction_stimuli = {}
    for inst in instructions_dict.keys():
        instruction, START, END = inst, instructions_dict[inst][0], instructions_dict[inst][1]
        instruction_stimuli[instruction] = experiment.create_instructions(window, instructions, START, END, color=textColor)

    # We don't want the mouse to show:
    event.Mouse(visible=False)
    
    ''' Baseline Experiment '''
    # Practice Trials
# =============================================================================
#     experiment.display_instructions(window, instruction_stimuli, logFile, start_instruction='Practice')
#     practice = experiment.create_trials(os.path.join(constants.DIR_MEDIA, constants.DIR_COLOR,"colour_practice.csv"))
#     experiment.running_practice_experiment(window, practice, logFile)
#     experiment.display_instructions(window, instruction_stimuli, logFile, start_instruction='Test')#(self, window, instruction_stimuli, logFile, start_instruction=''):
#     ha_trials = experiment.create_trials(os.path.join(constants.DIR_MEDIA, constants.DIR_COLOR,"colour_main.csv"))
#     experiment.running_actual_experiment(ha_trials, logFile)
#     experiment.run_eyeopen_baseline_rest(window, os.path.join(constants.DIR_MEDIA, constants.DIR_LA) , logFile)
# =============================================================================
    # wait for keypressed
    utils.display_wait_keypressed(window, 'Ready to start color stroop test, \n\n Press anykey to continue....')
    ''' main experiment '''
    # High Arousal Video
    # experiment.display_instructions(window, instruction_stimuli, logFile, start_instruction='Test')#(self, window, instruction_stimuli, logFile, start_instruction=''):
    ha_trials = experiment.create_trials(os.path.join(constants.DIR_MEDIA, constants.DIR_COLOR,"colour_main.csv"))
    experiment.running_actual_experiment(window, ha_trials, logFile)
    # wait for keypressed
    # utils.display_wait_keypressed(window, constants.endofCycle)
    # wait for 500ms to automatiicaly proceed to next task
    utils.display_wait_timeout(window, 'Next Task with New Video is coming... Pls wait about 0.5 s.... \n')
    # Low Arousal Video
    la_trials = experiment.create_trials(os.path.join(constants.DIR_MEDIA, constants.DIR_COLOR,"colour_main.csv"))
    experiment.running_actual_experiment(window, la_trials, logFile)
    
    # End experiment but first we display some instructions
    #experiment.display_instructions(window, instruction_stimuli, logFile, start_instruction='End')
    window.close()
    logFile.close()
    core.quit()
