# from typing import Sequence
# from numpy.core.fromnumeric import size
from psychopy import core, visual, gui, data, event, logging, constants, sound
import psychtoolbox as ptb
from psychopy.tools.filetools import fromFile, toFile
import time, numpy as np
import random, math, os


def generateBuffer(win, isHigh):
    print('\n Inside generateBuffer()')
    probeSeq = 0
    preset_buffer_count = 100
    sequence = [None] * preset_buffer_count
    corrAns = [None] * preset_buffer_count
    probe = [None] * preset_buffer_count
    probeImg = [None] * preset_buffer_count
    imgList = [None] * preset_buffer_count
    if isHigh:
        backcount = 2
    else:
        backcount = 0
    orangeImg = os.path.join(os.getcwd(), "_media", "nback_task", "orange.png")
    appleImg = os.path.join(os.getcwd(), "_media", "nback_task", "apple.png")
    lemonImg = os.path.join(os.getcwd(), "_media", "nback_task", "lemon.png")
    sberryImg = os.path.join(os.getcwd(), "_media", "nback_task", "sberry.png")
    choice = [orangeImg, appleImg, lemonImg, sberryImg]

    for x in range(preset_buffer_count):
        image = random.choice(choice)
        imgList[x] = image
        sequence[x] = visual.ImageStim(win=win, pos=(0,0), size=64, image = image, units="pix")
        ans = random.randint(0, 1) #if 1 means correct else wrong
        corrAns[x] = ans
        if ans:
            probeImg[x] = sequence[x-backcount]
        else:
            while True:
                wrongImg = random.choice(choice)
                if imgList[x-backcount] != wrongImg:
                    probeImg[x] = visual.ImageStim(win=win, pos=(0,-2), size=64, image = wrongImg, units="pix")
                    break
        
    for x in range(preset_buffer_count):
        probeSeq += random.randint(3,6)
        probe[x] = probeSeq
    return sequence, corrAns, probe, probeImg

def workLoadInst(win, isHigh):
    print('\n Inside workLoadInst()')
    orangeImg = os.path.join(os.getcwd(), "_media", "nback_task", "orange.png")
    appleImg = os.path.join(os.getcwd(), "_media", "nback_task", "apple.png")
    apple1 = visual.ImageStim(win=win, pos=(-150, 10), size=64, image = appleImg, units="pix")
    apple2 = visual.ImageStim(win=win, pos=(0, 10), size=64, image = appleImg, units="pix")
    orange1 = visual.ImageStim(win=win, pos=(150, 10), size=64, image = orangeImg, units="pix")
    orange2 = visual.ImageStim(win=win, pos=(0, 10), size=64, image = orangeImg, units="pix")
    topMessage = visual.TextStim(win, pos=[0,+3], color='#000000', alignText='center', name='topMsg')
    bottomMessage = visual.TextStim(win, pos=[0,-3], color='#000000', alignText='center', name='bottomMsg')
    # flag = 1
    count = "ONE"
    if isHigh:
        count = "THREE"

    topMessage.setText("In the next part, participants will be shown some images of fruits in a random sequence and will be required to memorise the last {} images of fruits shown.".format(count))
    bottomMessage.setText("Press space to continue")
    topMessage.draw()
    bottomMessage.draw()
    win.logOnFlip(level=logging.EXP, msg='Display 3-back instruction')
    win.flip()
    event.waitKeys(keyList='space')

    topMessage.setText("If the images of fruits shown currently is the same as the images of fruits shown {} images of fruits ago, participant will be required to press the space key".format(count))
    bottomMessage.setText("Press space to continue")
    topMessage.draw()
    bottomMessage.draw()
    win.logOnFlip(level=logging.EXP, msg='Display 3-back instruction')
    win.flip()
    event.waitKeys(keyList='space')
    if isHigh:
        topMessage.setText("For example, if the last 3 images of fruits shown are")
        bottomMsg = visual.TextStim(win, pos=[0,-4], color='#000000', alignText='center', name='bMsg')
        bottomMsg.setText("If the probe asks if the fruit THREE images ago was an apple, the participant will be required respond using the left arrow key to indicate YES")
        topMessage.draw()
        apple1.draw()                    
        apple2.draw() 
        orange1.draw()  
        bottomMsg.draw()
        win.logOnFlip(level=logging.EXP, msg='Display 1-back instruction')
        win.flip()
        event.waitKeys(keyList='space')
    else:
        topMessage.setText("For example, if the previous image of fruit shown is")
        bottomMsg = visual.TextStim(win, pos=[0,-4], color='#000000', alignText='center', name='bMsg')
        bottomMsg.setText("If the probe asks if the fruit was an apple, the participant will be required respond using the right arrow key to indicate NO")
        topMessage.draw() 
        orange2.draw()  
        bottomMsg.draw()
        win.logOnFlip(level=logging.EXP, msg='Display 1-back instruction')
        win.flip()
        event.waitKeys(keyList='space')

    topMessage = visual.TextStim(win, pos=[0,+3], color='#000000', alignText='center', name='topMsg')
    bottomMessage = visual.TextStim(win, pos=[0,-3], color='#000000', alignText='center', name='bottomMsg')
    topMessage.setText("End of Instruction")
    topMessage.draw()
    bottomMessage.setText("Press space to start a trial")
    bottomMessage.draw()
    win.logOnFlip(level=logging.EXP, msg='Instruction completed message. Trial commence')
    win.flip()
    event.waitKeys(keyList='space')   

def completeInst(win, isTrial):
    print('\n Inside completeInst()')
    if isTrial:
        topMessage = visual.TextStim(win, pos=[0,+3], color='#000000', alignText='center', name='topMsg')
        bottomMessage = visual.TextStim(win, pos=[0,-3], color='#000000', alignText='center', name='bottomMsg')
        topMessage.setText("Trial Completed")
        topMessage.draw()
        bottomMessage.setText("Press space to start the experiment")
        bottomMessage.draw()
        win.logOnFlip(level=logging.EXP, msg='Trial Completed')
        win.flip()
        event.waitKeys(keyList='space')  
    else:
        topMessage = visual.TextStim(win, pos=[0,+3], color='#000000', alignText='center', name='topMsg')
        bottomMessage = visual.TextStim(win, pos=[0,-3], color='#000000', alignText='center', name='bottomMsg')
        topMessage.setText("Experiment Completed")
        topMessage.draw()
        bottomMessage.setText("1 Minute Break")
        bottomMessage.draw()
        win.logOnFlip(level=logging.EXP, msg='Experiment Completed')
        win.flip()
        event.waitKeys(keyList='space')  

def workloadTask(win, isTrial, sequence, corrAns, probe, probeImg, isHigh, index, trialIndex):
    print('\n Inside workloadTask()')
    if isHigh:
        msgSeq = ["Is this the fruit shown 3 image ago?", "Incorrect key pressed. The last 3 images are as shown below. Press space to continue"]
    else:
        msgSeq = ["Is this the fruit in the previous image?", "Incorrect key pressed. The previous fruit is as shown below. Press space to continue"]

    leftArrowDir = u"\u2190"
    rightArrowDir = u"\u2192"
    topMessage = visual.TextStim(win, pos=[0,+3], color='#000000', alignText='center', name='topMsg')
    bottomMessage = visual.TextStim(win, pos=[0,-3], color='#000000', alignText='center', name='bottomMsg')
    # testTimer = core.MonotonicClock()
    keyList = ["escape", "left", "right", "q"]

    # if isTrial:
    #     timing = 5
    # else:
    #     timing = 5

    timeout = 3

    for x in range(15):
        adjIndex = x+index
        sequence[adjIndex].draw()
        win.flip()
        core.wait(1)
        win.flip()
        core.wait(0.5)
        if(adjIndex == probe[trialIndex]):
            topMessage.setText(msgSeq[0])
            yesSelection = visual.TextStim(win, text="Yes {}".format(leftArrowDir), color='#000000', pos = (-5,-10))
            noSelection = visual.TextStim(win, text="No {}".format(rightArrowDir), color='#000000', pos = (5,-10))
            yesSelection.draw()
            noSelection.draw()
            topMessage.draw()
            probeImg[adjIndex].draw()
            win.flip()
            keyPressed = event.waitKeys(maxWait=timeout, keyList=keyList)
            if isTrial:
                if keyPressed is None:
                    win.logOnFlip(level=logging.EXP, msg='Timeout - Nothing pressed')
                    topMessage.setText("Timeout")
                    bottomMessage.setText("Please press the left or right arrow key faster. Press the spacebar to continue")
                    topMessage.draw()
                    bottomMessage.draw()
                    win.logOnFlip(level=logging.EXP, msg='Trial - Timeout')
                    win.flip()
                    event.waitKeys(keyList='space')
                    # timing += 5
                elif "escape" in keyPressed:
                    win.logOnFlip(level=logging.EXP, msg='Experiment abandoned')
                    return False, 1
                elif "left" in keyPressed:
                    if corrAns[adjIndex] == 1:
                        win.logOnFlip(level=logging.EXP, msg='keypressed - Correct')
                    else:
                        win.logOnFlip(level=logging.EXP, msg='Keypressed - Wrong')
                        topMessage.setText(msgSeq[1])

                        if isHigh:
                            sequence[adjIndex-2].pos = (-150,-20)
                            sequence[adjIndex-1].pos = (0,-20)   
                            sequence[adjIndex].pos = (150,-20)
                            sequence[adjIndex-2].draw()                    
                            sequence[adjIndex-1].draw() 
                            sequence[adjIndex].draw()  
                        else:
                            sequence[adjIndex].pos = (0,-20)
                            sequence[adjIndex].draw()  

                        topMessage.draw()
                        win.logOnFlip(level=logging.EXP, msg='Trial - Wrong key pressed')
                        win.flip()
                        event.waitKeys(keyList='space')
                        # timing += 5
                elif "right" in keyPressed:
                    if corrAns[adjIndex] == 0:
                        win.logOnFlip(level=logging.EXP, msg='Keypressed - Correct')
                    else:
                        win.logOnFlip(level=logging.EXP, msg='Keypressed - Wrong')
                        topMessage.setText(msgSeq[1])
                        if isHigh:
                            sequence[adjIndex-2].pos = (-150,-20)
                            sequence[adjIndex-1].pos = (0,-20)   
                            sequence[adjIndex].pos = (150,-20)
                            sequence[adjIndex-2].draw()                    
                            sequence[adjIndex-1].draw() 
                            sequence[adjIndex].draw()  
                        else:
                            sequence[adjIndex].pos = (0,-20)
                            sequence[adjIndex].draw() 

                        topMessage.draw()
                        win.logOnFlip(level=logging.EXP, msg='Trial - Wrong key pressed')
                        win.flip()
                        event.waitKeys(keyList='space')
                        # timing += 5
            else:    
                if keyPressed is None:
                    win.logOnFlip(level=logging.EXP, msg='Timeout - Nothing pressed')
                elif "escape" in keyPressed:
                    win.logOnFlip(level=logging.EXP, msg='Experiment abandoned')
                    return False
                elif "left" in keyPressed:
                    if corrAns[trialIndex] == 1:
                        win.logOnFlip(level=logging.EXP, msg='Keypressed - Correct')
                    else:
                        win.logOnFlip(level=logging.EXP, msg='Keypressed - Wrong')
                elif "right" in keyPressed:
                    if corrAns[trialIndex] == 0:
                        win.logOnFlip(level=logging.EXP, msg='Keypressed - Correct')
                    else:
                        win.logOnFlip(level=logging.EXP, msg='Keypressed - Wrong')
                elif "escape" in keyPressed:
                    win.logOnFlip(level=logging.EXP, msg='Experiement ended')
                    return False

            trialIndex+=1
            win.flip()
            core.wait(0.5)
    return adjIndex+1, trialIndex

def trial(win, timing):
    print('\n Inside trial()')
    topMessage = visual.TextStim(win, pos=[0,+3], color='#000000', alignText='center', name='topMsg')
    bottomMessage = visual.TextStim(win, pos=[0,-3], color='#000000', alignText='center', name='bottomMsg')
    colorList = ['#6495ED', '#DC143C', '#008B8B', '#EE7600', '#EE1289','#B22222','#00FFFF','#8B2323','#8A3324', '#7AC5CD']
    leftArrowDir = u"\u2190"
    rightArrowDir = u"\u2192"
    leftArr = visual.TextStim(win, text=leftArrowDir, units="pix", pos = (-300, -200), height=100)
    rightArr = visual.TextStim(win, text=rightArrowDir, units="pix", pos = (300, -200), height=100)
    redRect = visual.Rect(win, units="pix", width=300, height=300, fillColor=[1, -1, -1], lineColor=[-1, -1, 1], opacity = 1, pos = (-400, 200))
    blueRect = visual.Rect(win, units="pix", width=300, height=300, fillColor=[-1, -1, 1], lineColor=[-1, -1, 1], opacity = 1, pos = (400, 200))
    selectionRect = visual.Rect(win, units="pix", width=300, height=300, fillColor=[-1, 0, -1], lineColor=[-1, -1, 1], opacity = 1, pos = (0, -200))
    
    testTimer = core.MonotonicClock()

    # if isTrial:
    #     timing = 15
    # else:
    #     timing = 60

    topMessage.setText("The next part of the experiment is requires the participant to evaluate whether the colour of the bottom square is nearer to the square on the top left of the top right")
    bottomMessage.setText("The participant is require to respond by pressing on the arrow key. Press space to continue")
    topMessage.draw()
    bottomMessage.draw()
    win.logOnFlip(level=logging.EXP, msg='Display colour sorting instruction')
    win.flip()
    event.waitKeys(keyList='space')

    topMessage.setText("If the colour is closer to the colour of the top right square, please press the right key. Else, press the left key if the colour is closer to the top left square.")
    bottomMessage.setText("Press space to continue")
    topMessage.draw()
    bottomMessage.draw()
    win.logOnFlip(level=logging.EXP, msg='Display colour sorting instruction')
    win.flip()
    event.waitKeys(keyList='space')

    topMessage.setText("For this part of the experiment, the results is subjective. Thus the participants are encourage to select according to the best fit.")
    bottomMessage.setText("Press space to continue")
    topMessage.draw()
    bottomMessage.draw()
    win.logOnFlip(level=logging.EXP, msg='Display colour sorting instruction')
    win.flip()
    event.waitKeys(keyList='space')

    while testTimer.getTime() < timing:
        colorNo = random.randint(0,9) 
        selectionRect = visual.Rect(win, units="pix", width=300, height=300, fillColor=colorList[colorNo], lineColor=[-1, -1, 1], opacity = 1, pos = (0, -200))
        selectionRect.draw()
        redRect.draw()
        blueRect.draw()
        rightArr.draw()
        leftArr.draw()
        win.flip()
        keyPressed = event.waitKeys(maxWait= 3, keyList=["left", "right", "escape"]) 

        if keyPressed is None:
                pass
                win.logOnFlip(level=logging.EXP, msg='Nothing Pressed')
                redRect.draw()
                blueRect.draw()
                rightArr.draw()
                leftArr.draw()
                win.flip()
                core.wait(0.25)

        elif "escape" in keyPressed:
            win.logOnFlip(level=logging.EXP, msg='Experiment abandoned')
            break
        elif "right" in keyPressed:
            win.logOnFlip(level=logging.EXP, msg='Keypressed - Right')
            redRect.draw()
            blueRect.draw()
            rightArr.draw()
            leftArr.draw()
            win.flip()
            core.wait(0.25)

        elif "left" in keyPressed:
            win.logOnFlip(level=logging.EXP, msg='Keypressed - Left')
            redRect.draw()
            blueRect.draw()
            rightArr.draw()
            leftArr.draw()
            win.flip()
            core.wait(0.25)
            