# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Aung Aung
"""
from psychopy import core, visual, event
import os
from _misc import constants #from . import constants
from _misc import utils #from . import utils
from biocal import EEGBiocal
from attention import attention_task
from nback import workload
from emotion import affect_task
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

# def run_baseline_tasks(win, logger):

def get_media_files_path():
    MEDIA_PWD_PATH = os.path.join(os.getcwd(), constants.DIR_MEDIA)    
    att_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_ATT)
    wkl_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_WKL)
    emo_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_WKL)
    calm_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_CALM)    
    return att_files_path, wkl_files_path, emo_files_path, calm_files_path

def run_baseline_attention_task(win, abs_file_path, logger):
    baseline_att = attention_task.AttentionTask(win, None, abs_file_path) 
    # start trial for 1 block
    baseline_att.trial(logger)
    # actual task blocks
    baseline_att.start(logger)

def run_baseline_workload_task(win, abs_file_path, logger):
    baseline_workload = workload.WorkloadTask(win, abs_file_path)
    # start WL trials and task
    baseline_workload.start_workload(logger)
   

def run_baseline_affect_task(win, abs_file_path, logger):    
    print('\n Inside run_baseline_affect_task() \n')
    baseline_emo = affect_task.AffectImage(win, abs_file_path)
    # instruction page
    utils.display_wait_keypressed(win, constants.MSG_AFFECT_TASK)    
    # + image sets
    baseline_emo.elicit_high_valence(logger)
    # neutral image sets
    baseline_emo.elicit_neutral(logger)
    # - image sets
    baseline_emo.elicit_low_valence(logger)
    
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

def run_eyeclosed_rest_break(win, abs_file_path, logger):
    rest_video = visual.MovieStim3(win, os.path.join(abs_file_path, "breathing.mp4"), flipVert=False, flipHoriz=False, loop=True, size=(945,525))
    # wait for user keypressed
    utils.display_wait_keypressed(win, constants.MSG_BREAK_DB)   
    # display deep breathing audio video
    rest_break.rest_deep_breathing(win, rest_video, logger, constants.TIME_REST_BREAK)
    # end of video message        
    utils.display_wait_keypressed(win, constants.MSG_VIDEO_FINISHED) 

def run_eyeopen_baseline_rest(win, abs_file_path, logger):
    rest_video = visual.MovieStim3(win, os.path.join(abs_file_path, "breathing.mp4"), flipVert=False, flipHoriz=False, loop=True, size=(945,525))
    # wait for user keypressed
    utils.display_wait_keypressed(win, constants.MSG_REST_DB)   
    # display deep breathing audio video
    rest_break.rest_deep_breathing(win, rest_video, logger, constants.TIME_REST_BASELINE)
    # end of video message        
    utils.display_wait_keypressed(win, constants.MSG_VIDEO_FINISHED) 

def  run_public_speech_task(win, abs_file_path, logger):
    utils.display_wait_keypressed(win, "Press any key to begin Public speaking task\n")
    # 2min self-introduction
    rest_break.start_auto_timeout(win, constants.MSG_SELF_INTRO, constants.TIME_SELF_INTRO, None, logger)   
    # 5 cycle eye closed rest
    run_eyeopen_baseline_rest(win, abs_file_path, logger)
    # like-topic preparation
    run_topic_block(win, logger, constants.TOPIC_LIKE)
    # like topic presentation
    run_topic_block(win, logger, constants.TOPIC_DISLIKE)
    # like optic questions
    run_topic_block(win, logger, constants.TOPIC_IMPROMPTU)
                      
def run_topic_block(win, logger, topic_type):
    if topic_type is not constants.TOPIC_IMPROMPTU:
        #preparation step
        rest_break.start_auto_timeout(win, constants.MSG_SPEECH_PREPARE, constants.TIME_SPEECH_PREPARE, None, logger)
        #actual presentation step
        if topic_type is constants.TOPIC_LIKE:
            rest_break.start_auto_timeout(win, constants.MSG_SPEECH_LIKE, constants.TIME_SPEECH_TALK, constants.MSG_SPEECH_FINISHED, logger)
        else:
            rest_break.start_auto_timeout(win, constants.MSG_SPEECH_DISLIKE, constants.TIME_SPEECH_TALK, constants.MSG_SPEECH_FINISHED, logger)
        # survey and rest
        rest_break.start_auto_timeout(win, constants.MSG_SPEECH_FEEDBACK, constants.TIME_SPEECH_QUEST_REST, None, logger)
    else:
        utils.display_wait_keypressed(win, "Press any key to start Impromptu talk\n")
        #random topic presentation step
        rest_break.start_auto_timeout(win, constants.MSG_SPEECH_IMPROMPTU, constants.TIME_SPEECH_TALK, constants.MSG_SPEECH_FINISHED, logger)
    
def main_start(win):
    
    """Entry point into the whole experiment."""
    ATT_ABS_PATH, WKL_ABS_PATH, EMO_ABS_PATH, CALM_ABS_PATH = get_media_files_path()
    # set default experiment config parameters 
    exp_para = utils.set_exp_config_para()
    #get timestamp and create log file
    logging_filename = os.path.join(utils.get_log_file_path(), utils.get_current_time_micros() + ".log")

    with open(logging_filename, "w") as logger:
        # Get current time in local timezone
        utils.write_log_header(logger, exp_para)               
        ''' start the experiment welcome screen '''
        logger.write(utils.get_current_time_micros() + "\tStart experiment\n")
        # exp welcome screen
        experiment_welcome_screen(win)       
        ''' biocal tasks  '''
        # run_biocal_tasks(win, logger)
        ''' baseline tasks '''
        # attention tasks
        # run_baseline_attention_task(win, ATT_ABS_PATH, logger)
        # 40s rest, 5 db cycle
        # run_eyeopen_baseline_rest(win, CALM_ABS_PATH, logger)
        # workload tasks
        # run_baseline_workload_task(win, WKL_ABS_PATH, logger)
        # 40s rest, 5 db cycle
        # run_eyeopen_baseline_rest(win, CALM_ABS_PATH, logger)
        # visual affect task
        run_baseline_affect_task(win, EMO_ABS_PATH, logger)
        # 40s rest, 5 db cycle
        # run_eyeopen_baseline_rest(win, CALM_ABS_PATH, logger)
        # arousal+relax videos task
        # run_baseline_calm_task(win, CALM_ABS_PATH, logger)
        ''' eye-closed break before public speaking '''
        # run_eyeclosed_rest_break(win, CALM_ABS_PATH, logger)
        ''' public speaking task '''
        # run_public_speech_task(win, CALM_ABS_PATH, logger)
        # finished experiment
        logger.write(utils.get_current_time_micros() + "\tEnd experiment\n")
      
    # Complete end of experiment procedures 
    experiment_end_screen(win)
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
    win = visual.Window(fullscr=constants.FULL_SCREEN, monitor=monitorName, color="black", screen=screenToUse, units="pix")
    # Start experiment
    main_start(win)