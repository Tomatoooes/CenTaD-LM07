# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Aung Aung
"""
from psychopy import core, visual, event
import os
from _misc import constants, utils #from . import constants, from _misc import utils #from . import utils
from attention import attention_task
#import psychopy.constants as psychopy_constants
from rest import rest_break


# Provides overview of experiment
def experiment_welcome_screen(win):
    """Screen to be shown at the very start of the whole experiment."""
    MSG_MAIN_WELCOME = "You will perform random order of color, word or face stroop task while watching video concurrently in this session. \n\n" + \
                "When you are ready to begin, please press any key..."
    start_message_stim = visual.TextStim(win=win, text=MSG_MAIN_WELCOME)
    #start_message_stim = assign_textstim_properties(start_message_stim)
    start_message_stim.draw()
    win.flip()
    #wait for key pressed
    event.waitKeys()

# Starts the end of experiment procedures
def experiment_end_screen(win):
    """Screen to be shown when the whole experiment comes to an end."""
    MSG_MAIN_FINISH = "You have come to the end of the experiment. Please help us by completing the post-experiment survey. Press any key to exit."
    end_message_stim = visual.TextStim(win=win, text=MSG_MAIN_FINISH, height=44, units="pix")
    end_message_stim.draw()
    win.flip()
    #wait for key pressed
    event.waitKeys()

def get_media_files_path():
    MEDIA_PWD_PATH = os.path.join(os.getcwd(), constants.DIR_MEDIA)    
    color_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_COLOR)
    word_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_WORD)
    face_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_FACE)  
    la_files_path = os.path.join(MEDIA_PWD_PATH, constants.DIR_LA)  
 
    return color_files_path, word_files_path, face_files_path, la_files_path

def run_eyeopen_baseline_rest(win, abs_file_path, logger):
    logger.write(utils.get_current_time_micros() + "\t Start EyeOpen Rest \n")
    rest_video = visual.MovieStim3(win, os.path.join(abs_file_path, constants.VIDEO_DB_LA), flipVert=False, flipHoriz=False, loop=True, size=(945,525))
    # wait for user keypressed
    utils.display_wait_keypressed(win, constants.MSG_REST_DB)   
    # display deep breathing audio video
    rest_break.rest_deep_breathing(win, rest_video, logger, constants.TIME_REST_BASELINE)
    # end of video message        
    utils.display_wait_keypressed(win, constants.MSG_VIDEO_FINISHED) 
    logger.write(utils.get_current_time_micros() + "\t Finished EyeOpen Rest \n")

def  run_video_arousal_stroop_block(win, arousal_type, block_id, att_abs_path, logger):
    logger.write(utils.get_current_time_micros() + f"\t Start High Arousal Stimuli with {arousal_type}-{block_id}\n")
    if arousal_type == constants.STROOP_BASE:
        cStroop = attention_task.AttentionTask(win, constants.STROOP_BASE, constants.CSV_PREFIX_MAIN, att_abs_path, None)        
        trials = cStroop.create_trials(os.path.join(att_abs_path, constants.FILE_MAIN_CSTROOP))
        cStroop.running_actual_experiment(trials, logger)
    elif arousal_type == constants.STROOP_WORD:
        wStroop = attention_task.AttentionTask(win, constants.STROOP_WORD, constants.CSV_PREFIX_MAIN, att_abs_path, None)        
        trials = wStroop.create_trials(os.path.join(att_abs_path, constants.FILE_MAIN_WSTROOP))
        wStroop.running_actual_experiment(trials, logger)
    elif arousal_type == constants.STROOP_WORD:
        fStroop = attention_task.AttentionTask(win, constants.STROOP_FACE, constants.CSV_PREFIX_MAIN, att_abs_path, None)        
        trials = fStroop.create_trials(os.path.join(att_abs_path, constants.FILE_MAIN_FSTROOP))
        fStroop.running_actual_experiment(trials, logger)
    # else:
    #    print(f'Unsupport arousal_type: {arousal_type}.... \n')            
    # logging end of task   
    logger.write(utils.get_current_time_micros() + f"\t Finished High Arousal Stimuli with {arousal_type}-{block_id}\n")

    
def main_start(win):    
    """Entry point into the whole experiment."""
    COLOR_ABS_PATH, WORD_ABS_PATH, FACE_ABS_PATH, LA_ABS_PATH = get_media_files_path() #att_files_path, color_files_path, word_files_path, face_files_path, emo_files_path, la_files_path, ha_files_path
    # set default experiment config parameters 
    # exp_para = utils.set_exp_config_para()
    # stroop task to path mapping
    dir_stroop = {constants.STROOP_BASE: COLOR_ABS_PATH, constants.STROOP_WORD: WORD_ABS_PATH, constants.STROOP_FACE: FACE_ABS_PATH}   
    #get timestamp and create log file
    logging_filename = os.path.join(utils.get_log_file_path(), utils.get_current_time_micros() + ".log")

    with open(logging_filename, "w") as logger:
        # Get current time in local timezone
        utils.write_log_header(logger)#, exp_para)               
        ''' start the experiment welcome screen '''
        logger.write(utils.get_current_time_micros() + "\tStart Main experiment\n")
        # exp welcome screen
        experiment_welcome_screen(win)       

        ''' main experiment task '''
        for iSess in range(0, constants.N_MAIN_SESS):
            run_video_arousal_stroop_block(win, constants.HIGH_AROUSAL_TASKID[iSess], iSess+1, dir_stroop[constants.HIGH_AROUSAL_TASKID[iSess]], logger)
            utils.display_wait_keypressed(win, constants.endofCycle)
            run_video_arousal_stroop_block(win, constants.LOW_AROUSAL_TASKID[iSess], iSess+1, logger)
            if iSess is not constants.N_MAIN_SESS-1:
                run_eyeopen_baseline_rest(win, LA_ABS_PATH, logger)
        # finished experiment
        logger.write(utils.get_current_time_micros() + "\tEnd Main experiment\n")
      
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
    
    
###############################################################
# def assign_textstim_properties(tStim):
#     tStim.alignText = 'center'
#     tStim.anchorHoriz = 'center' 
#     tStim.anchorVert='center'
#     tStim.bold = True
#     tStim.height=24
#     return tStim

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
    
def run_color_stroop_task(win, att_file_path, ina_file_path, logger):
    logger.write(utils.get_current_time_micros() + "\t Start Baseline Color Stroop Task \n")
    baseline_stroop = attention_task.AttentionTask(win, constants.STROOP_BASE, None, att_file_path, ina_file_path) 
    
    running_actual_experiment(self, trials, logFile)
    # actual task blocks
    baseline_stroop.start(logger)
    logger.write(utils.get_current_time_micros() + "\t Finished Baseline Color Stroop Task \n")

def run_baseline_emo_word_stroop_task(win, abs_file_path, logger):
    logger.write(utils.get_current_time_micros() + "\t Start Emotional Words Stroop Task \n")
    baseline_emo_word_stroop = attention_task.AttentionTask(win, constants.STROOP_WORD, None, abs_file_path) 
    # start WL trials and task
    baseline_emo_word_stroop.trial(logger)
    # actual task blocks
    baseline_emo_word_stroop.start(logger)
    logger.write(utils.get_current_time_micros() + "\t Finished Emotional Words Stroop Task \n")

def run_baseline_emo_face_stroop_task(win, abs_file_path, logger):
    logger.write(utils.get_current_time_micros() + "\t Start Emotional Faces Stroop Task \n")
    baseline_emo_face_stroop = attention_task.AttentionTask(win, constants.STROOP_FACE, None, abs_file_path) 
    # start WL trials and task
    baseline_emo_face_stroop.trial(logger)
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
        
'''