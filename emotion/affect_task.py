# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 00:05:09 2022

@author: CIL-SCSE

"""
from psychopy import core, visual, event
import glob, os
from _misc import constants, utils
from datetime import datetime

class AffectImage:
    def __init__(self, win, media_abs_path):
        self.win = win
        dirname = os.path.dirname(__file__)
        self.imgHVHA = glob.glob(os.path.join(media_abs_path, "HVHA")+"\\*")
        self.imgHVLA = glob.glob(os.path.join(media_abs_path, "HVLA")+"\\*")
        # imgHVHA = glob.glob(dirname+"_images/HVHA/*")
        # imgHVLA = glob.glob(dirname+"_images/HVLA/*")
        # print(dirname)
        # print("path "+os.path.join(media_abs_path, constants.DIR_EMO, "HVHA")+"\\*")
        # print(f"No of HVHA images: {len(imgHVHA)}\n")
        # self.emoPosImages = [imgHVHA, imgHVLA]
        
        # self.emoNeuImages = glob.glob(os.path.join(media_abs_path, "NEU")+"\\*")
        self.emoNeuImages = glob.glob(dirname+"_images/NEU/*")
        
        self.imgLVHA = glob.glob(os.path.join(media_abs_path, "LVHA")+"\\*")
        self.imgLVLA = glob.glob(os.path.join(media_abs_path, "LVLA")+"\\*")
        # self.imgLVHA = glob.glob(dirname+"_images/HVHA/*")
        # self.imgLVLA = glob.glob(dirname+"_images/HVLA/*")
        # self.emoNegImages = [imgLVHA, imgLVLA]
        
    def elicit_high_valence(self, logger):
        logger.write(utils.get_current_time_micros() + "\t Eliciting High Valence Affect\n")
        self.display_image_sequences(self.imgHVHA, logger)
        core.wait(constants.TIME_IMG_AFFECT_WAIT)
        self.display_image_sequences(self.imgHVLA, logger)
        
    def elicit_low_valence(self, logger):
        logger.write(utils.get_current_time_micros() + "\t Eliciting Low Valence Affect\n")
        self.display_image_sequences(self.imgLVHA, logger)
        core.wait(constants.TIME_IMG_AFFECT_WAIT)
        self.display_image_sequences(self.imgLVLA, logger)
        
    def elicit_neutral(self, logger):
        logger.write(utils.get_current_time_micros() + "\t Eliciting Neutral Affect\n")
        self.display_image_sequences(self.emoNeuImages, logger)
        
    def display_image_sequences(self, img_list, logger):
        logger.write(utils.get_current_time_micros() + "\tStart Displaying Image Sequences\n")
        #loop for HAHV images
        count = 0
        #run through the images and log each image
        for x in img_list:
            logger.write(utils.get_current_time_micros() + f"\t Image {count+1}\n")
            stim= visual.ImageStim(self.win, image=x, size=(750,500), units="pix")
            stim.draw()
            self.win.flip()
            count = count + 1            
            core.wait(constants.TIME_IMG_AFFECT_WAIT)
        logger.write(utils.get_current_time_micros() + "\tFinished Displaying Image Sequences\n")
           
""" parameters """
Logging_Dir = os.path.join(os.getcwd(), constants.LOG_DIR)
if not os.path.exists(Logging_Dir):
    os.makedirs(Logging_Dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")    
logging_filename = os.path.join(Logging_Dir, timestamp + ".log")
logFile = open(logging_filename, "w")    

USE_EXTERNAL_SCREEN = False
FULL_SCREEN_MODE = False


if __name__ == "__main__":
    useSecondaryMonitor = USE_EXTERNAL_SCREEN
    screenToUse = 1 if useSecondaryMonitor else 0
    monitorName = "secondary" if useSecondaryMonitor else "testMonitor"
    win = visual.Window(fullscr=FULL_SCREEN_MODE, monitor=monitorName, color="black", screen=screenToUse, units="pix")
    
    trialID = [1, 3, 0, 2]#1, 2, 3, 2, 0, 1]
    # random.shuffle(trialID)
    tester = AffectImage(win, os.path.join(os.getcwd(), constants.DIR_MEDIA, constants.DIR_EMO))
    with open("test.log", "w") as log:
        tester.elicit_high_valence(log)
        # tester.start(log)
        
    win.close()
    core.quit()