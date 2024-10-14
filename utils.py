# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 19:26:55 2022

@author: spyder
"""
# import pyxid2
import os, sys
from _misc import constants
from typing import NamedTuple
from datetime import datetime
from time import mktime
import time
import winsound as ws
from psychopy import core, visual, event

# all experiment parameters
# class ExpConfigPara(NamedTuple):
#     n_session: int    
#     n_baseline: int
#     n_blocks_att: int
        

def notify_beep():
    ws.Beep(constants.BEEP_FREQ_HZ[1], constants.NOTIFY_TIME_S)

# def rhythm_beep():
#     ws.Beep(constants.BEEP_FREQ_HZ[0], constants.METRONOME_TIME_S)
    
# def set_exp_config_para():
#     return ExpConfigPara(constants.N_TOPIC_SESS, constants.N_BASELINE, constants.N_BLOCKS_ATT)    

# def get_config_file_param():
#     """Get experiment configuration parameters"""
#     return NotImplemented
def display_wait_keypressed(win, disp_msg, txt_height=30):
    emo_message_inst = visual.TextStim(win, disp_msg, height=txt_height, units="pix")
    emo_message_inst.draw()
    win.flip()
    event.waitKeys()

def display_wait_timeout(win, disp_msg, txt_height=30):
    emo_message_inst = visual.TextStim(win, disp_msg, height=txt_height, units="pix")
    emo_message_inst.draw()
    win.flip()
    core.wait(.8)
    win.flip()
    
def get_current_time_micros():
    return datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")
       
def get_log_file_path():
    log_dir = os.path.join(os.getcwd(), constants.LOG_DIR)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    return log_dir

def write_log_header(log):#, exp_para):
    local_dt = datetime.now()
    log.write("Local Time: " + local_dt.strftime("%Y-%m-%d %H:%M:%S.%f") +", TZ:"+ local_dt.astimezone().tzname() +" (GMT"+local_dt.astimezone().strftime("%z")[0:3]+") \n")
    log.write("GMT Time: " + datetime.fromtimestamp(mktime(time.gmtime())).strftime("%Y-%m-%d %H:%M:%S.%f") +"\n")
    log.write("------------\n")
    log.write("Experiment config parameters.\n")
    log.write("============\n")
    
def getBaseTen(binaryVal):
    count = 0
    #reverse the string
    binaryVal = binaryVal[::-1]
    #go through the list and get the value of all 1's
    for i in range(0, len(binaryVal)):
        if(binaryVal[i] == "1"):
            count += 2**i
    return count