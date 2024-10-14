# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 01:25:36 2022

@author: spyder
"""
import random as rnd

''' experiment monitor setup and screen settings '''
SECOND_SCREEN = True
FULL_SCREEN = False#True

''' experiment protocol settings '''
N_MAIN_SESS = 2 #High vs Low arousal
N_BASELINE = 4 #cstroop, wstroop, fstroop, emotion

HAS_TRIAL = True

''' strrop type parameters '''
STROOP_BASE = 'baseline-stroop'
STROOP_WORD = 'emoword-stroop'
STROOP_FACE = 'emoface-stroop'

RESP_KEYS = ["escape", "x", "m", "X", "M"] #["escape", "left", "num_4", "right", "num_6"]   # keys to be used for attention responses

TIME_ATT_INA_BLOCK_BASELINE = 25 #seconds
TIME_ATT_BLOCK_MAIN = 200 #seconds = 1.67min

N_BLOCKS_ATT_BASELINE = 5
N_BLOCKS_ATT_MAIN = 3

CSV_PREFIX_BASELINE = 'baseline'
CSV_PREFIX_MAIN = 'main'

TIME_WN_WAIT = 0.2 #seconds
TIME_FIXATION = 0.8 #seconds
TIME_ISI = 1.2 #seconds
N_TRIALS_PER_BLOCK_BASELINE = 25# round(TIME_ATT_INA_BLOCK_BASELINE/(TIME_FIXATION + TIME_ISI)) + 1 #8+1 to ensure 
N_TRIALS_PER_BLOCK_MAIN = round(TIME_ATT_BLOCK_MAIN/(TIME_FIXATION + TIME_ISI)) + 1 #8+1 to ensure 
# N_ATT_BLOCKS = 5
# DEFAULT_BLOCK_ID = 1#only run single flanker task block

HIGH_AROUSAL_TASKID = [STROOP_BASE, STROOP_WORD, STROOP_FACE]
rnd.shuffle(HIGH_AROUSAL_TASKID)
LOW_AROUSAL_TASKID = [STROOP_BASE, STROOP_WORD, STROOP_FACE]
rnd.shuffle(LOW_AROUSAL_TASKID)

STROOP_COLOR = {"background": "Black", "text":  "White"}

# inattention task stimuli
VIDEO_WN = "white_noise_video.mp4"
IMG_WN = "white_noise_image.jpg"
VIDEO_DB_LA = "breathing.mp4"

# folders for stimuli, images and videos
LOG_DIR = '_logs'
DIR_MEDIA = "_media"
DIR_INA = 'attention_task'
# stroop variants
DIR_COLOR = 'stroop_color_task'
DIR_WORD = 'stroop_words_task'
DIR_FACE = 'stroop_faces_task'
# emotion affect task
DIR_EMO = 'affect_task'
# relax or clam task
DIR_HA = 'high_arousal_video'
DIR_LA = 'low_arousal_video'

FILE_MAIN_CSTROOP = 'colour_main.csv'


''' trial timing and parameters '''
TIME_IMG_AFFECT_WAIT = 3.2
TIME_WAIT_TRANSITION = 2 #seconds
BIOCAL_TIME_S = 30 #seconds
BLANK_DURATION_S = 10#30.0 #seconds default
NOTIFY_TIME_S = 200 #milliseconds
BEEP_FREQ_HZ = [450, #metronome
                850, #notification sound
                ]
# TIME_VIDEO_TASK = 150
TIME_REST_BREAK = 120
TIME_REST_BASELINE = 40

''' Messages definition '''
MSG_EXP_WELCOME = "Welcome to Emotional Intelligence Evaluation experiment! \n\n"+\
                "If you require assistance,please ask the experimenter anytime.\n\n"+\
                     "Otherwise follow on-screen instructions. \n\n" + \
               "Press \"any key\" to start the experiment..."
MSG_EXP_FINISH = "End of the experiment. \n\n"+\
                "Thanks very much for your participation.\n\n"+\
                "Press \"any key\" to exit...."  
                #" Please help us by completing the post-experiment survey.\n\n" + \
                    
MSG_EXP_BIOCAL = "Next task is Eyes Open and Closed Calibrication. \n\n"+ \
                        "Press \"any key\" to start..."
MSG_INTRO_BIOCAL = "Preparing Biocal EEG Tasks..."                        
MSG_BIOCAL_EC = "Close your eyes before a key pressed and re-open when you hear the beep. \n\n Press any key to start..."                        
MSG_BIOCAL_EO = "Keep your eyes open and look at '+' until hearing the beep. \n\nPress any key to start..."
             
MSG_AFFECT_TASK = "Affect Task: \n\
Look at the sequence of images shown to induce emotion by experiencing and feeling the image's contexts.\n\n\
Press any key to begin..."
MSG_HIGH_AROUSAL_VIDEO = "Arousal Video (2 Minutes): \n\
You will watch the video while minimising any head or eyes movement.\n\n\
The video might cause a bit of excitement and discomfort to elicit high emotional arousal.\n\n\
Press any key to watch..."
MSG_LOW_AROUSAL_VIDEO = "Relaxation Video (2 Minutes): \n\
You will watch the video while minimising any head or eyes movement.\n\n\
and enjoying both beautiful scenery and soothing music to induce relaxation.\n\n\
Press any key to watch..."

MSG_REST_DB = "Deep Breathing Task (~5 breaths): \n\
Follow the deep breathing animation and audio guidance.\n\n\
Relax and regulate your breathing according to the visual and audio guide.\n\n\
Press any key to begin."
MSG_BREAK_DB = "Deep Breathing Task (~2 minutes): \n\
Please close eyes, relax and slow down breathing according to the audio guide.\n\n\
Press any key to begin."

#-----------Common Message-----------
endofTrial = "End of Trial\n\n\
If you are ready to begin, press any key."

endofCycle = "End of Block\n\n\
Press any key to continue."

endofTask = "End of Task\n\n\
If you are ready to begin, press any key."

MSG_KEY_PRESSED = "\nPress 'any key' to continue when ready..."
MSG_BLK_FIRST = "Preparing for First Trial... \n"
MSG_BLK_START = "Preparing for next Trial... \n"
MSG_WAIT_USER_KEY = "Are you ready to start the tasks...? \n\n" + \
                    "Please clarify with experimenter if any before continuing \n\n"+ \
                    "Press any key to continue..."
MSG_BLOCK_WAIT = "You may take a break as you desired before continuing. \n\n" + \
                 "       Press \"any key\" when ready to begin."

MSG_VIDEO_FINISHED = "Task Finished... You may take a break as you desired. \n\n" + \
                     " Press \"any key\" if ready to continue..."

# MSG_BREAK_REST = "Please take a Resting BREAK of minimum 30 seconds before next task \n"+\
#                  "You can take additional rest or continue next task after hearing Beep \n\n"+\
#                  "and seeing new instructions appeared on the screen...."
# MSG_BREAK_EXTRA = "You may take additional break as you desired before next task. \n\n" + \
#                  "Press \"any key\" once you are ready to begin."        