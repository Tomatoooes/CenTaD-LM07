# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 01:25:36 2022

@author: spyder
"""
import random as rnd

''' experiment monitor setup and screen settings '''
SECOND_SCREEN = True
FULL_SCREEN = True

''' experiment protocol settings '''
N_TOPIC_SESS = 3 #Like, Dislike, Impromptu
N_BASELINE = 4 #attention, workload, valence, arousal
N_BLOCKS_ATT = 1#6

HAS_TRIAL = True

''' attention block parameters '''
STIM_CS_KEY = 0
STIM_CN_KEY = 1
STIM_IS_KEY = 2
STIM_IN_KEY = 3
RESP_KEYS = ["escape", "left", "num_4", "right", "num_6"]   # keys to be used for attention responses
STIM_DICT = {STIM_CS_KEY:'smile-congruent.jpg', STIM_CN_KEY:'neutral-congruent.jpg', STIM_IS_KEY:'smile-incongruent.jpg', STIM_IN_KEY:'neutral-incongruent.jpg'}
TIME_ATT_INA_BLOCK = 10#20 #seconds
TIME_WN_WAIT = 0.2 #seconds
TIME_FIXATION = 0.8 #seconds
TIME_ISI = 1.2 #seconds
N_TRIALS_PER_BLOCK = round(TIME_ATT_INA_BLOCK/(TIME_FIXATION + TIME_ISI)) + 1 #8+1 to ensure 
N_ATT_BLOCKS = 2#6
DEFAULT_BLOCK_ID = 1#only run single flanker task block

DEFAULT_STIM_ID_PER_BLOCK = list(STIM_DICT.keys()) + list(STIM_DICT.keys())
DEFAULT_STIM_ID_PER_BLOCK.append(rnd.randrange(min(STIM_DICT.keys()), max(STIM_DICT.keys())))
rnd.shuffle(DEFAULT_STIM_ID_PER_BLOCK)

''' workload n-back parameters '''
LOW_WORKLOAD = False
HIGH_WORKLOAD = not LOW_WORKLOAD
#need to be 300
WL_PRE_GEN = 300

#need to be 150
WL_TIMING = 20#150

#need to be 60
WL_TIMING_TRIAL = 20#60

WL_TIMEOUT = 1.2
WL_WAIT_TIME = 0.2

''' topic categories '''
TOPIC_LIKE = 1
TOPIC_DISLIKE = -1
TOPIC_IMPROMPTU = 0

LOG_DIR = '_psychopy_logs'
DIR_MEDIA = "_media"
IMG_EXP_PROTOCOL = "experiment-protocol.png"
# attention task
DIR_ATT = 'attention_task'
VIDEO_WN = "white_noise_video.mp4"
IMG_WN = "white_noise_image.jpg"
IMG_ATT_INST = 'att-instruct.png'
# workload task
DIR_WKL = 'nback_task'
# emotion affect task
DIR_EMO = 'affect_task'
# relax or clam task
DIR_CALM = 'relax_task'
SUBDIR_AROUSE = 'arousal'
SUBDIR_RELAX = 'relax'

''' trial timing and parameters '''
TIME_IMG_AFFECT_WAIT = 3.2
TIME_WAIT_TRANSITION = 2 #seconds
BIOCAL_TIME_S = 30 #seconds
BLANK_DURATION_S = 10#30.0 #seconds default
NOTIFY_TIME_S = 200 #milliseconds
BEEP_FREQ_HZ = [450, #metronome
                850, #notification sound
                ]
TIME_VIDEO_TASK = 150
TIME_REST_BREAK = 120
TIME_REST_BASELINE = 40
TIME_SELF_INTRO = 10#120 #seconds

TIME_SPEECH_PREPARE = 10#120
TIME_SPEECH_TALK = 20#300
TIME_SPEECH_QUEST_REST = 10#180
''' Messages definition '''
MSG_KEY_PRESSED = "\nPress 'any key' to continue when ready..."
MSG_BLK_FIRST = "Preparing for First Trial... \n"
MSG_BLK_START = "Preparing for next Trial... \n"
MSG_WAIT_USER_KEY = "Are you ready to start the tasks...? \n\n" + \
                    "Please clarify with experimenter if any before continuing \n\n"+ \
                    "Press any key to continue..."

MSG_INTRO_BIOCAL = "Preparing Biocal EEG Tasks..."
# MSG_END_SPEECH = "Preparing Hand Open+Close Video Tutorials ..."

MSG_EXP_WELCOME = "Welcome to Public Speaking Anxiety Evaluation experiment! \n\n"+\
                "If you require assistance,please ask the experimenter anytime.\n\n"+\
                     "Otherwise follow on-screen instructions. \n\n" + \
               "Press \"any key\" to start the experiment..."
MSG_EXP_FINISH = "End of the experiment. \n\n"+\
                "Thanks very much for your participation.\n\n"+\
                "Press \"any key\" to exit...."  
                #" Please help us by completing the post-experiment survey.\n\n" + \
MSG_BLOCK_WAIT = "You may take a break as you desired before continuing. \n\n" + \
                 "       Press \"any key\" when ready to begin."

MSG_VIDEO_FINISHED = "Task Finished... You may take a break as you desired. \n\n" + \
                     " Press \"any key\" if ready to continue..."

                    
MSG_EXP_BIOCAL = "Next task is Eyes Open and Closed Calibrication. \n\n"+ \
                        "Press \"any key\" to start..."
MSG_BIOCAL_EC = "Close your eyes before a key pressed and re-open when you hear the beep. \n\n Press any key to start..."                        
MSG_BIOCAL_EO = "Keep your eyes open and look at '+' until hearing the beep. \n\nPress any key to start..."


# MSG_BREAK_REST = "Please take a Resting BREAK of minimum 30 seconds before next task \n"+\
#                  "You can take additional rest or continue next task after hearing Beep \n\n"+\
#                  "and seeing new instructions appeared on the screen...."
# MSG_BREAK_EXTRA = "You may take additional break as you desired before next task. \n\n" + \
#                  "Press \"any key\" once you are ready to begin."                  

             
MSG_AFFECT_TASK = "Affect Task: \n\
Look at the sequence of images shown to induce emotion by experiencing and feeling the image's contexts.\n\n\
Press any key to begin..."

MSG_AROUSAL_VIDEO = "Arousal Video (2 Minutes): \n\
You will watch the video while minimising any head or eyes movement.\n\n\
The video might cause a bit of excitement and discomfort to elicit high emotional arousal.\n\n\
Press any key to watch..."

MSG_RELAX_VIDEO = "Relaxation Video (2 Minutes): \n\
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

MSG_SELF_INTRO = "Self-Introduction (~2 minutes): \n\
Please introduce yourself and your personality about public speaking.\n\
You need to stop speaking after timeout..."

MSG_SPEECH_PREPARE = "Speech Preparation (~3 minutes): \n\
Please prepare to speak reading through scripts and presentation materials.\n\
You only have 3 minutes to prepare your speech before auto-timeout..."

MSG_SPEECH_LIKE = "Speaking Like Topic (~5 minutes): \n\
Please start deilverying your speak. You only have 5 minutes. \n\
You need to stop as soon as seeing the next screen..."

MSG_SPEECH_DISLIKE = "Speaking Dislike Topic (~5 minutes): \n\
Please start deilverying your speak. You only have 5 minutes. \n\
You need to stop as soon as seeing the next screen..."

MSG_SPEECH_IMPROMPTU = "Speaking Impromptu Topic (~5 minutes): \n\
Please start deilverying your speak. You only have 5 minutes. \n\
You need to stop as soon as seeing the next screen..."

MSG_SPEECH_FINISHED = "Finished Speaking: \n\n\
Please continue to answer questionaires from tablet provided. \n\
You can take a rest before next instruction appears on the screen.\n\
Press any key to continue..."

MSG_SPEECH_FEEDBACK = "Feedback and Rest (~3 minutes): \n\
please feedback about your experience on speaking on the public with the selected topic. \n\
Please wait for auto-timeout to continue... "

#-----------Workload Task-----------
# workloadTaskI1 = "In the next part, participants will be shown images of fruits in a random sequence and will be required to memorise the fruits shown.\n\n\
# If the fruits shown currently is the same as the fruits previously, the participant will be required to press the space key"

highWorkloadI1 = "High Workload Task (3-Back Task, 2.5 minutes): \n\
Look at the centre of the screen where a sequence of fruits is presented. Memorise the last 3 fruits shown.\n\n\
Press any key, if the current fruit is the same as the fruit 3 sequence ago.\n\n\
Press any key once you understand this task."

highWorkloadI2old = "If the fruit shown three fruits ago is the same as the fruit currently shown, immediately press any space key.\n\n\
Press any key once you understand this task."

highWorkloadI2 = "Press any key to begin."

lowWorkloadI1dold =  "Low Workload Task (1-Back Task, 2.5 minutes): \n\
A sequence of fruits will be presented to you. You will be required to memorise the previous fruit shown.\n\n\
If the current fruit shown is the same as the fruit shown directly before, immediately press any key\n\n\
Press any key once you understand this task."

lowWorkloadI1 =  "Low Workload Task (1-Back Task, 2.5 minutes): \n\
Look at the centre of the screen where a sequence of fruits is presented. Memorise the previous fruit shown.\n\n\
Press any key, if the current fruit is the same as the previous fruit.\n\n\
Press any key once you understand this task."

lowWorkloadI2 = "If the previous fruit shown is the same as the fruit currently shown, immediately press any key.\n\n\
Press any key once you understand this task."

exampleText = "In the fruit sequence shown below, press any key whenever the {}-back condition is met (Denoted areas)"

workloadTrial = "You will start with a practice trial to experience the test\n\n\
Press any key once to begin."

#-----------Common Message-----------
endofTrial = "End of Trial\n\n\
If you are ready to begin, press any key."

endofCycle = "End of Cycle\n\n\
Press any key to continue."

endofTask = "End of Task\n\n\
If you are ready to begin, press any key."