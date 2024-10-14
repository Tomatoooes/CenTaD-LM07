# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Aung Aung
"""
from psychopy import core, visual, event
import os
from _misc import constants, utils #from . import constants, from _misc import utils #from . import utils
from biocal import EEGBiocal
from attention import attention_task
from emotion import affect_task
# from stroop import *
import psychopy.constants as psychopy_constants
from rest import rest_break

def assign_textstim_properties(tStim):
    tStim.alignText = 'center'
    tStim.anchorHoriz = 'center' 
    tStim.anchorVert='center'
    tStim.bold = True
    tStim.height=24
    return tStim

# Provides overview of experiment
def experiment_welcome_screen(win):
    """Screen to be shown at the very start of the whole experiment."""
    #message = "Welcome to the experiment! \n\nIf at any time you require assistance, feel free to ask the experimenter.\n\nOtherwise the experiment is completely automated. \n\n" + \
    #            "When you are ready to begin, please press any key..."
    start_message_stim = visual.TextStim(win=win, text=constants.MSG_EXP_WELCOME)
    #start_message_stim = assign_textstim_properties(start_message_stim)
    start_message_stim.draw()
    win.flip()
    #wait for key pressed
    event.waitKeys()

# Starts the end of experiment procedures
def experiment_end_screen(win):
    """Screen to be shown when the whole experiment comes to an end."""
    #end_message = "You have come to the end of the experiment. Please help us by completing the post-experiment survey. Press any key to exit."
    end_message_stim = visual.TextStim(win=win, text=constants.MSG_EXP_FINISH, height=44, units="pix")
    end_message_stim.draw()
    win.flip()
    #wait for key pressed
    event.waitKeys()

def run_biocal_tasks(win, logger):
    ''' biocal Preparation Screen auto-timeout '''
    rest_break.start_auto_timeout(win, constants.MSG_INTRO_BIOCAL, constants.TIME_WAIT_TRANSITION, None, logger)
    win.flip()    
    ''' actual biocal EEG calibration   '''
    logger.write(utils.get_current_time_micros() + "\tStart Biocal\n")
            # biocal task
    biocal_eeg = EEGBiocal.EEGBiocal(win, constants.BIOCAL_TIME_S, logger)
    biocal_eeg.start()
    logger.write(utils.get_current_time_micros() + "\tFinished Biocal\n")

def get_media_files_path():
    MEDIA_PWD_PATH = os.path.join(os.getcwd(), constants.DIR_MEDIA)    
    att_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_INA)
    color_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_COLOR)
    word_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_WORD)
    face_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_FACE)
    emo_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_EMO)
    la_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_LA)  
    ha_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_HA)  
    return att_files_path, color_files_path, word_files_path, face_files_path, emo_files_path, la_files_path, ha_files_path

''' 4 baseline tasks: cstrop, wstroop, fstroop, emotion '''
def run_baseline_color_stroop_task(win, att_file_path, ina_file_path, logger):
    logger.write(utils.get_current_time_micros() + "\t Start Baseline Color Stroop Task \n")
    baseline_stroop = attention_task.AttentionTask(win, constants.STROOP_BASE, constants.CSV_PREFIX_BASELINE, att_file_path, ina_file_path) 
    # start trial for 1 block
    baseline_stroop.trial(logger)
    # actual task blocks
    baseline_stroop.start(logger)
    logger.write(utils.get_current_time_micros() + "\t Finished Baseline Color Stroop Task \n")

def run_baseline_emo_word_stroop_task(win, att_file_path, ina_file_path, logger):
    logger.write(utils.get_current_time_micros() + "\t Start Emotional Words Stroop Task \n")
    baseline_emo_word_stroop = attention_task.AttentionTask(win, constants.STROOP_WORD, constants.CSV_PREFIX_BASELINE, att_file_path, ina_file_path) 
    # start WL trials and task
    baseline_emo_word_stroop.trial(logger)
    # actual task blocks
    baseline_emo_word_stroop.start(logger)
    logger.write(utils.get_current_time_micros() + "\t Finished Emotional Words Stroop Task \n")

def run_baseline_emo_face_stroop_task(win, att_file_path, ina_file_path, logger):
    logger.write(utils.get_current_time_micros() + "\t Start Emotional Faces Stroop Task \n")
    baseline_emo_face_stroop = attention_task.AttentionTask(win, constants.STROOP_FACE, constants.CSV_PREFIX_BASELINE, att_file_path, ina_file_path) 
    # start WL trials and task
    # baseline_emo_face_stroop.trial(logger)
    # actual task blocks
    baseline_emo_face_stroop.start(logger)
    logger.write(utils.get_current_time_micros() + "\t Finished Emotional Faces Stroop Task \n")

def run_baseline_affect_task(win, abs_file_path, logger):    
    logger.write(utils.get_current_time_micros() + "\t Start Affect Images Task \n")
    baseline_emo = affect_task.AffectImage(win, abs_file_path)
    # instruction page
    utils.display_wait_keypressed(win, constants.MSG_AFFECT_TASK)    
    # + image sets
    baseline_emo.elicit_high_valence(logger)
    # neutral image sets
    baseline_emo.elicit_neutral(logger)
    # - image sets
    baseline_emo.elicit_low_valence(logger)
    logger.write(utils.get_current_time_micros() + "\t Finished Affect Images Task \n")
    
def run_eyeclosed_rest_break(win, abs_file_path, logger):
    logger.write(utils.get_current_time_micros() + "\t Start EyeClosed Rest \n")
    rest_video = visual.MovieStim3(win, os.path.join(abs_file_path, "breathing.mp4"), flipVert=False, flipHoriz=False, loop=True, size=(945,525))
    # wait for user keypressed
    utils.display_wait_keypressed(win, constants.MSG_BREAK_DB)   
    # display deep breathing audio video
    rest_break.rest_deep_breathing(win, rest_video, logger, constants.TIME_REST_BREAK)
    # end of video message        
    utils.display_wait_keypressed(win, constants.MSG_VIDEO_FINISHED) 
    logger.write(utils.get_current_time_micros() + "\t Finished EyeClosed Rest \n")

def run_eyeopen_baseline_rest(win, abs_file_path, logger):
    logger.write(utils.get_current_time_micros() + "\t Start EyeOpen Rest \n")
    rest_video = visual.MovieStim3(win, os.path.join(abs_file_path, "breathing.mp4"), flipVert=False, flipHoriz=False, loop=True, size=(945,525))
    # wait for user keypressed
    utils.display_wait_keypressed(win, constants.MSG_REST_DB)   
    # display deep breathing audio video
    rest_break.rest_deep_breathing(win, rest_video, logger, constants.TIME_REST_BASELINE)
    # end of video message        
    utils.display_wait_keypressed(win, constants.MSG_VIDEO_FINISHED) 
    logger.write(utils.get_current_time_micros() + "\t Finished EyeOpen Rest \n")

def main_start(win):
    
    """Entry point into the whole experiment."""
    INA_ABS_PATH, COLOR_ABS_PATH, WORD_ABS_PATH, FACE_ABS_PATH, EMO_ABS_PATH, LA_ABS_PATH, HA_ABS_PATH = get_media_files_path() #att_files_path, color_files_path, word_files_path, face_files_path, emo_files_path, la_files_path, ha_files_path
    # set default experiment config parameters 
    # exp_para = utils.set_exp_config_para()
    #get timestamp and create log file
    logging_filename = os.path.join(utils.get_log_file_path(), utils.get_current_time_micros() + ".log")

    with open(logging_filename, "w") as logger:
        # Get current time in local timezone
        utils.write_log_header(logger)#, exp_para)               
        ''' start the experiment welcome screen '''
        logger.write(utils.get_current_time_micros() + "\tStart baselline experiment\n")
        # exp welcome screen
        experiment_welcome_screen(win)       
        ''' biocal tasks  '''
        run_biocal_tasks(win, logger)
        ''' baseline tasks '''
        # color stroop tasks
        run_baseline_color_stroop_task(win, COLOR_ABS_PATH, INA_ABS_PATH, logger)
        # # 40s rest, 5 db cycle
        run_eyeopen_baseline_rest(win, LA_ABS_PATH, logger)
        # # emotion word stroop tasks
        run_baseline_emo_word_stroop_task(win, WORD_ABS_PATH, INA_ABS_PATH, logger)
        # # 40s rest, 5 db cycle
        run_eyeopen_baseline_rest(win, LA_ABS_PATH, logger)
        # # emotion face stroop task
        run_baseline_emo_face_stroop_task(win, FACE_ABS_PATH, INA_ABS_PATH, logger)
        # # 40s rest, 5 db cycle
        run_eyeopen_baseline_rest(win, LA_ABS_PATH, logger)
        # visual affect task
        run_baseline_affect_task(win, EMO_ABS_PATH, logger)    
        ''' REST: eye-closed break before main experiment '''
        # run_eyeopen_baseline_rest(win, LA_ABS_PATH, logger)
        run_eyeclosed_rest_break(win, LA_ABS_PATH, logger)
        # finished experiment
        logger.write(utils.get_current_time_micros() + "\tEnd baseline experiment\n")
      
    # Complete end of experiment procedures 
    # experiment_end_screen(win) 
    #logger.write(utils.get_current_time_micros() + "\t Final Key Pressed from User. Thanks for your participation.... \n")
    logger.close()
    win.close()    
    core.quit()
        
if __name__ == "__main__":
    # Set up monitor
    useSecondaryMonitor = constants.SECOND_SCREEN
    #useSecondaryMonitor = len(sys.argv) > 2 and sys.argv[2] == "-s"
    screenToUse = 1 if useSecondaryMonitor else 0 
    monitorName = "secondary" if useSecondaryMonitor else "testMonitor"
    # Create window
    win = visual.Window(fullscr=constants.FULL_SCREEN, monitor=monitorName, color="black", screen=screenToUse) #, units="pix"
    # Start experiment
    main_start(win)
    
    
###############################################################
'''
def run_baseline_calm_task(win, abs_file_path, logger):       
    arousal_video = visual.MovieStim3(win, os.path.join(abs_file_path, constants.SUBDIR_AROUSE, "loud_musicvideo.mp4"), flipVert=False, flipHoriz=False)
    relax_video = visual.MovieStim3(win, os.path.join(abs_file_path, constants.SUBDIR_RELAX, "flower_nature.mp4"), flipVert=False, flipHoriz=False)
    # display arousal video instruction
    utils.display_wait_keypressed(win, constants.MSG_AROUSAL_VIDEO)     
    #start playing arousal video
    testTimer = core.MonotonicClock()
    while arousal_video.status != psychopy_constants.FINISHED:
            arousal_video.draw()
            win.flip()
            if testTimer.getTime()>constants.TIME_VIDEO_TASK:
                arousal_video.stop()
                break 
    # stop the video
    arousal_video.stop()
    # end of video message        
    utils.display_wait_keypressed(win, constants.MSG_VIDEO_FINISHED)        
    # display relaxation video instruction
    utils.display_wait_keypressed(win, constants.MSG_RELAX_VIDEO)  
    #start playing relax video
    testTimer = core.MonotonicClock()
    while relax_video.status != psychopy_constants.FINISHED:
            relax_video.draw()
            win.flip()
            if testTimer.getTime()>constants.TIME_VIDEO_TASK:
                relax_video.stop()
                break
    # stop the video
    relax_video.stop()
    # end of video message        
    utils.display_wait_keypressed(win, constants.MSG_VIDEO_FINISHED)        
'''