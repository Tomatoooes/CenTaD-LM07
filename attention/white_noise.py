from psychopy import visual, core #, event
from psychopy.hardware import keyboard
import os #, sys
from _misc import constants

# Movie_Dir = os.path.join(os.getcwd(), "White_Noise", "Media", "clip.mp4")
# Image_Dir = os.path.join(os.getcwd(), "White_Noise", "Media", "Still_Image.jpg")
# kb = keyboard.Keyboard()

class WhiteNoise:
    def __init__(self, win, media_abs_path=None):
        self.win = win
        if media_abs_path is None:
            ATT_DIR = os.path.join(constants.DIR_MEDIA, constants.DIR_ATT)
        else:
            ATT_DIR = media_abs_path 
        self.movie_dir = ATT_DIR
        self.clip = visual.MovieStim3(win=self.win, filename=os.path.join(ATT_DIR, constants.VIDEO_WN))
        self.image1 = visual.ImageStim(win=self.win, image=os.path.join(ATT_DIR, constants.IMG_WN), opacity=0.1)
        self.image2 = visual.ImageStim(win=self.win, image=os.path.join(ATT_DIR, constants.IMG_WN), opacity=0.3)
        self.image3 = visual.ImageStim(win=self.win, image=os.path.join(ATT_DIR, constants.IMG_WN), opacity=0.6)
        self.image4 = visual.ImageStim(win=self.win, image=os.path.join(ATT_DIR, constants.IMG_WN), opacity=0.9)
        # self.pause = visual.TextStim(win=self.win, text="Paused")

    def start(self, logger, duration_sec=None):
        kb = keyboard.Keyboard()
        if duration_sec is not None:
            TIME_OUT = duration_sec
        else:
            TIME_OUT = constants.TIME_ATT_INA_BLOCK
        totalPauseTime = 0.0
        timer = core.MonotonicClock()
        self.fadeIn()
        while timer.getTime() - totalPauseTime < TIME_OUT:
            kb.getKeys() # Clear keyboard buffer
            self.clip.draw()
            self.win.flip()
            keys = kb.getKeys(keyList=["escape"], waitRelease=False)
            if keys and "escape" in keys:
                break
# =============================================================================
#             elif keys and keys[0] == "q":
#                 self.clip.pause() # Pause sound
#                 pauseTimeStart = timer.getTime()
#                 # Draw pause screen
#                 self.pause.draw()
#                 self.win.flip()
# 
#                 event.waitKeys(keyList=["q"]) # Wait for unpause
#                 totalPauseTime += timer.getTime() - pauseTimeStart
#                 self.fadeIn() # Fade in and start video
#                 self.clip.play()
# =============================================================================
        self.clip.stop() # Stop sound
        self.win.flip() # Stop display
        self.fadeOut()
        self.clip.loadMovie(os.path.join(self.movie_dir, constants.VIDEO_WN)) # Reset movie for next block

    def fadeIn(self):
        # draw image 1, wait 0.2s
        self.image1.draw()
        self.win.flip()
        core.wait(constants.TIME_WN_WAIT)

        # draw image 2, wait 0.2s
        self.image2.draw()
        self.win.flip()
        core.wait(constants.TIME_WN_WAIT)

        # draw image 3, wait 0.2s
        self.image3.draw()
        self.win.flip()
        core.wait(constants.TIME_WN_WAIT)

        # draw image 4, wait 0.2s
        self.image4.draw()
        self.win.flip()
        core.wait(constants.TIME_WN_WAIT)

    def fadeOut(self):
        # draw image 4, wait 0.2s
        self.image4.draw()
        self.win.flip()
        core.wait(constants.TIME_WN_WAIT)

        # draw image 3, wait 0.2s
        self.image3.draw()
        self.win.flip()
        core.wait(constants.TIME_WN_WAIT)

        # draw image 2, wait 0.2s
        self.image2.draw()
        self.win.flip()
        core.wait(constants.TIME_WN_WAIT)

        # draw image 1, wait 0.2s
        self.image1.draw()
        self.win.flip()
        core.wait(constants.TIME_WN_WAIT)

        self.win.flip() # fade to blank screen

''' experiment monitor setup and screen settings '''
SECOND_SCREEN = False
FULL_SCREEN = False

if __name__ == "__main__":
    # Redefine directories as cwd is different
    Movie_Dir = os.path.join(constants.DIR_MEDIA, constants.DIR_ATT, constants.VIDEO_WN)
    Image_Dir = os.path.join(constants.DIR_MEDIA, constants.DIR_ATT, constants.IMG_WN)
    # screen settings
    screenToUse = 1 if SECOND_SCREEN else 0
    monitorName = "secondary" if SECOND_SCREEN else "testMonitor"
    win = visual.Window(fullscr=FULL_SCREEN, monitor=monitorName, color="black", screen=screenToUse, units="pix")
    tester = WhiteNoise(win)
    tester.start()
    win.close()
        
