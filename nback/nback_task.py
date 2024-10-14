from typing import Sequence
from numpy.core.fromnumeric import size
from psychopy import core, visual, gui, data, event, logging, constants as psychopy_constants, sound
import psychtoolbox as ptb
from psychopy.tools.filetools import fromFile, toFile
import time, numpy as np
import random, math, os
from datetime import datetime
#from restSequence import *
from _misc import constants
# import instructionText

def generateWorkloadBuffer(win, isHigh, dirname):
    backword = 1
    if isHigh:
        backword = 3

    #image initiation
    orangeImg = os.path.join(os.getcwd(), "_media", "nback_task", "orange.png")
    appleImg = os.path.join(os.getcwd(), "_media", "nback_task", "apple.png")
    lemonImg = os.path.join(os.getcwd(), "_media", "nback_task", "lemon.png")
    sberryImg = os.path.join(os.getcwd(), "_media", "nback_task", "sberry.png")
    choice = [orangeImg, appleImg, lemonImg, sberryImg]
    name = ["orangeImg", "appleImg", "lemonImg", "sberryImg"]

    #generate list
    seqIndex = 0
    bufferlength = constants.WL_PRE_GEN
    fruitName = [None] * bufferlength
    sequence = [None] * bufferlength
    choiceList = [None] * bufferlength
    responseSequence = [None] * bufferlength 
    index = 0

    #this entire if-else loops determine the entire probe index.
    #1-back task
    if backword == 1:
        for x in range(int(bufferlength/2)):
            #nextcorr is the number of fruit where the next response is required
            nextCorr = random.randint(1,4)
            #seqIndex keeps track of the index
            seqIndex += nextCorr
            responseSequence[x] = seqIndex
            #the minus 4 is so that every set of 4 fruits, 1 will require a response
            extraSeq = 4-nextCorr
            seqIndex += extraSeq
    #3-back task
    elif backword == 3:
        for x in range(int(bufferlength/2)):
            if x == 0:
                #nextcorr is the number of fruit where the next response is required                
                #first cycle for 3-back need to exclude the first 3 fruits
                nextCorr = random.randint(3,6)
                #seqIndex keeps track of the index
                seqIndex += nextCorr
                responseSequence[x] = seqIndex
                #for the first set it uses minus 6 instead as the first 3 fruits is skipped
                extraSeq = 6-nextCorr
                seqIndex += extraSeq
            else:
                #nextcorr is the number of fruit where the next response is required
                nextCorr = random.randint(1,4)
                #seqIndex keeps track of the index
                seqIndex += nextCorr
                responseSequence[x] = seqIndex
                #the minus 4 is so that every set of 4 fruits, 1 will require a response
                extraSeq = 4-nextCorr
                seqIndex += extraSeq

    #this set of if-else loops create the entire sequence that will be shown
    #it fills up the buffer with fruits to be shown
    for y in range (bufferlength):
        #if the current sequence is a probe
        if y == responseSequence[index]:
            index+=1
            sequence[y] = sequence[y-backword]
            fruitName[y] = fruitName[y-backword]
            choiceList[y] = choiceList[y-backword]
        #if the current sequence is not a probe 
        else:
            flag = True
            while flag:
                #randomly generate a fruit that is not the same as N fruits ago
                fruitIndex = random.randint(0,3)
                fruit = name[fruitIndex]
                if fruit != fruitName[y-backword]:
                    sequence[y] = visual.ImageStim(win=win, pos=(0, 0), size=64, image = choice[fruitIndex], units="pix")
                    fruitName[y] = name[fruitIndex]
                    choiceList[y] = choice[fruitIndex]
                    flag = False
    print(fruitName)
    print(responseSequence)
    return sequence, responseSequence, fruitName



def workloadTaskSeq(win, log, highBuffer, lowBuffer):
   


    #high workload buffer
    sequence = highBuffer[0] 
    seqIndex = highBuffer[1] 
    fruitsName = highBuffer[2]
    #Low workload buffer
    lsequence = lowBuffer[0]
    lseqIndex =lowBuffer[1] 
    lfruitsName = lowBuffer[2]

    log.write(str(time.time())+"\tEnd of rest time\n")

    #Initialisation of the variable

    currIndexL = 0
    respondIndexL = 0
    currIndexH = 0
    respondIndexH = 0
   
    #Low workload
    log.write(str(time.time())+"\tDisplay Low Workload Instruction\n")
    workLoadInst(win, False, True)

    #Experiment Trial - Low Workload
    log.write(str(time.time())+"\tStart Low Workload Trial\n")
    # workloadlog.write(str(time.time())+"\tStart Low Workload Trial\n")

    #Start trial
    currIndexL, respondIndexL = workloadTask(win, True, False, lsequence, currIndexL, lseqIndex, lfruitsName, log, respondIndexL)
    # workloadlog.write(str(time.time())+"\tCompleted Low Workload Trial\n")
    log.write(str(time.time())+"\tCompleted Low Workload Trial\n")


    completeInst(win, True)

    log.write(str(time.time())+"\tStart Low Workload Experiment\n")
   

    #Actual experiment
    currIndexL, respondIndexL = workloadTask(win, False, False, lsequence, currIndexL, lseqIndex, lfruitsName, log, respondIndexL)
    log.write(str(time.time())+"\tCompleted Low Workload Experiment\n")
    log.write(str(time.time())+"\tCompleted Low Workload Experiment\n")
   
    #High workload
    log.write(str(time.time())+"\tDisplay High Workload Instruction\n")
    workLoadInst(win, True, True)

    #Experiment Trial - High Workload
    log.write(str(time.time())+"\tStart High Workload Trial\n")
    
    #Start trial
    currIndexH, respondIndexH = workloadTask(win, True, True, sequence, currIndexH, seqIndex, fruitsName, log, respondIndexH)
    log.write(str(time.time())+"\tCompleted High Workload Trial\n")
    log.write(str(time.time())+"\tCompleted High Workload Trial\n")
  
    completeInst(win, True)

    log.write(str(time.time())+"\tStart High Workload Experiment\n")
   

    #Actual experiment
    currIndexH, respondIndexH = workloadTask(win, False, True, sequence, currIndexH, seqIndex, fruitsName, log, respondIndexH)
    log.write(str(time.time())+"\tCompleted High Workload Experiment\n")
    log.write(str(time.time())+"\tCompleted High Workload Experiment\n")


#Instruction for trial only
def workLoadInst(win, isHigh, isTrial):
    #Initialisation of variable
    example1 = os.path.join(os.getcwd(), "_media", "nback_task", "3-Back_resized.png")
    example2 = os.path.join(os.getcwd(), "_media", "nback_task", "1-Back_resized.png")    

    lowWLExmaple = visual.ImageStim(win=win, image = example2, size=(1171, 336), units="pix")
    highWLExmaple = visual.ImageStim(win=win, image = example1, size=(1171, 336), units="pix")
    topMessage = visual.TextStim(win, pos=[0,+7], color="white")
    bottomMessage = visual.TextStim(win, pos=[0,-8], color="white")
    messageP1 = visual.TextStim(win, color="white")
    flag = 1

    #Displaying of instruction
    if isTrial:
        if isHigh:
            messageP1.setText(constants.highWorkloadI1)
            messageP1.draw()
            win.flip()
            event.waitKeys()

            topMessage.setText(constants.exampleText.format(3))
            bottomMessage.setText(constants.highWorkloadI2)
            bottomMessage.setText()
            topMessage.draw()
            highWLExmaple.draw()
            bottomMessage.draw()
            win.flip()
            event.waitKeys()
        else:
            messageP1.setText(constants.lowWorkloadI1)
            messageP1.draw()
            win.flip()
            event.waitKeys()

            topMessage.setText(constants.exampleText.format(1))
            bottomMessage.setText(constants.lowWorkloadI2)
            bottomMessage.setText()
            topMessage.draw()
            lowWLExmaple.draw()
            bottomMessage.draw()
            win.flip()
            event.waitKeys()

        messageP1.setText(constants.workloadTrial)
        messageP1.draw()
        win.flip()
        event.waitKeys()
    #else branch is not used and just used during debugging
    else:
        topMessage.setText("Respond to the prompt according to the image of the fruit shown {} image ago".format("this is a glitch"))
        topMessage.draw()
        bottomMessage.setText("Press space to start a trial")
        bottomMessage.draw()
        win.flip()
        event.waitKeys()

#Completion instruction
def completeInst(win, isTrial):
    messageP1 = visual.TextStim(win, color="white")
    if isTrial:
        messageP1.setText(constants.endofTrial)

    messageP1.draw()
    win.flip()
    event.waitKeys()

#Actual task
def workloadTask(win, isTrial, isHigh, sequence, usedSeq, sequenceIndex, fruitName, WLLog, index):
    currIndex = usedSeq
    respondIndex = index

    topMessage = visual.TextStim(win, pos=[0,+5], color="white")

    if isTrial:
        timing = constants.WL_TIMING_TRIAL
    else:
        timing = constants.WL_TIMING

    timeout = constants.WL_TIMEOUT
    testTimer = core.MonotonicClock()
    count = 0
    while testTimer.getTime() < timing:
        #Drawing of fixation
        fixation = visual.TextStim(win=win, text="+", height=64, units="pix") # Fixation point
        fixation.draw()
        win.flip()
        #randomised wait time
        core.wait(random.randint(50, 100)/100)
        sequence[currIndex].pos=(0,0)
        sequence[currIndex].draw()
        print("sequence = {}".format(currIndex))

        WLLog.write(str(time.time())+"\tCycle {}: {} shown\n".format(count, fruitName[currIndex]))
        win.flip()
        keyPressed = event.waitKeys(maxWait=1.2, keyList=["num_1","num_2","num_3","num_4","num_5","num_6","num_7","num_8","num_9"])
        win.flip()
        core.wait(constants.WL_WAIT_TIME)
        
        #Feedback during trial 
        if isTrial:
            if sequenceIndex[respondIndex] == currIndex:
                respondIndex+=1
                if keyPressed is None:
                    WLLog.write(str(time.time())+"\tTime out - Nothing Pressed\n")
                    if isHigh:
                        topMessage.setText("Timeout - Please respond faster\n\nThe fruit shown is the same as the fruit shown 3 fruit ago. The sequence of the last 4 fruits are as shown. Press any key to continue")
                        topMessage.draw()

                        #show the past 4 sequence to help the subject to continue after missing the current sequence
                        sequence[currIndex-3].pos = (-225,-20)
                        sequence[currIndex-3].draw()

                        sequence[currIndex-2].pos = (-75,-20)
                        sequence[currIndex-2].draw()                    

                        sequence[currIndex-1].pos = (75,-20)   
                        sequence[currIndex-1].draw() 

                        sequence[currIndex].pos = (225,-20)
                        sequence[currIndex].draw()  

                    else:
                        topMessage.setText("Timeout - Please respond faster\n\nThe fruit shown is the same as the previous fruit shown. The sequence of the last 2 fruits are as shown. Press any key to continue")
                        topMessage.draw()

                        #show the past 2 sequence to help the subject to continue after missing the current sequence
                        sequence[currIndex-1].pos = (-75,-20)
                        sequence[currIndex-1].draw()
                        
                        sequence[currIndex].pos = (75,-20)
                        sequence[currIndex].draw() 

                    win.flip()
                    event.waitKeys()
                    timing += 5

                elif "escape" in keyPressed:
                    WLLog.write(str(time.time())+"\tExperiment Abandoned - Escape Pressed\n")
                    return False, 1
                elif "num_1" or "num_2" or "num_3" or "num_4" or "num_5" or "num_6" or "num_7" or "num_8" or "num_9" in keyPressed:
                    WLLog.write(str(time.time())+"\tCorrect Response - Key Pressed\n")
            else:
                if keyPressed is None:
                    pass
                elif "num_1" or "num_2" or "num_3" or "num_4" or "num_5" or "num_6" or "num_7" or "num_8" or "num_9"  in keyPressed:
                    WLLog.write(str(time.time())+"\tIncorrect Space Input\n")
                    if isHigh:
                        topMessage.setText("Incorrect Input\n\nThe fruit shown is NOT the same as the fruit shown 3 fruit ago. The sequence of the last 4 fruits are as shown. Press any key to continue")
                        topMessage.draw()

                        #show the past 4 sequence to help the subject to continue after getting the current sequence wrong
                        sequence[currIndex-3].pos = (-225,-20)
                        sequence[currIndex-3].draw()

                        sequence[currIndex-2].pos = (-75,-20)
                        sequence[currIndex-2].draw()                    

                        sequence[currIndex-1].pos = (75,-20)   
                        sequence[currIndex-1].draw() 

                        sequence[currIndex].pos = (225,-20)
                        sequence[currIndex].draw()  
                    else:
                        topMessage.setText("Incorrect Input\n\nThe fruit shown is NOT the same as the previous fruit. The sequence of the last 2 fruits are as shown. Press any key to continue")
                        topMessage.draw()
                        
                        #show the past 2 sequence to help the subject to continue after getting the current sequence wrong
                        sequence[currIndex-1].pos = (-75,-20)
                        sequence[currIndex-1].draw()
                        
                        sequence[currIndex].pos = (75,-20)
                        sequence[currIndex].draw() 

                    topMessage.draw()
                    win.flip()
                    event.waitKeys()
                    timing += 5
                elif "escape" in keyPressed:
                    WLLog.write(str(time.time())+"\tExperiment Abandoned - Escape Pressed\n")
                    return False, 1

        else:    
            if keyPressed is None:
                WLLog.write(str(time.time())+"\tTime out - Nothing Pressed\n")
            elif "escape" in keyPressed:
                WLLog.write(str(time.time())+"\tExperiment Abandoned - Escape Pressed\n")
                return False
            elif "num_1" or "num_2" or "num_3" or "num_4" or "num_5" or "num_6" or "num_7" or "num_8" or "num_9" in keyPressed:
                if sequenceIndex[respondIndex] == currIndex:
                    WLLog.write(str(time.time())+"\tKey Pressed\n")
                else:
                    WLLog.write(str(time.time())+"\tKey Pressed\n")

            win.flip()
            core.wait(constants.WL_WAIT_TIME)
            WLLog.flush()
        count += 1
        currIndex += 1

    return currIndex, respondIndex

