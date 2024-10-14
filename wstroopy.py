# -*- coding: utf-8 -*-
from psychopy import event, core, data, visual
from _misc import fileHandling, constants, utils 
from datetime import datetime
import os, time
from rest import rest_break

class Stroop:
    def __init__(self, para_profile, color_profile, abs_file_path):
        self.name = 'Emo Word Stroop'
        self.stimuli_positions = [[-.4, 0], [.4, 0], [0, 0]]
        self.win_color = color_profile['background']
        self.txt_color = color_profile['text']
        self.para_exp = para_profile
        self.settings = {'Subid': '10', 'Experiment Version': 0.1,
                            'Sex': 'Male',
                            'Language': 'English', u'date':
                                data.getDateStr(format="%Y-%m-%d_%H:%M:%S")}

        self.settings[u'DataFile'] = u'' + os.getcwd() + os.path.sep + constants.LOG_DIR + os.path.sep + f'{self.name}_' + data.getDateStr(format="%Y-%m-%d_%H-%M-%S") + u'.csv'

        

    def create_text_stimuli(self, window, text=None, pos=[0.0, 0.0], name='', color=None):
        '''Creates a text stimulus,
        '''
        if color is None:
            color = self.txt_color
        text_stimuli = visual.TextStim(win=window, ori=0, name=name,
                                       text=text, font=u'Arial',
                                       pos=pos,
                                       color=color, colorSpace=u'rgb')
        return text_stimuli

    def create_trials(self, trial_file, randomization='random'):
        '''Doc string'''
        data_types = ['Response', 'Accuracy', 'RT', 'Sub_id', 'Sex']
        trials = fileHandling.read_csv_file(trial_file, data)
        # with open(trial_file, 'r') as stimfile:
        #     _stims = csv.DictReader(stimfile)
        #     trials = data.TrialHandler(list(_stims), 1,
        #                                method="random")
        [trials.data.addDataType(data_type) for data_type in data_types]

        return trials

    def present_stimuli(self, color, text, position, stim):
        _stimulus = stim
        color = color
        position = position
        text = text
        _stimulus.pos = position
        _stimulus.setColor(color)
        _stimulus.setText(text)
        return _stimulus

    def running_actual_experiment(self, window, trials, logFile):
        _trials = trials
        restTxt = visual.TextStim(win=window, text="Get Ready for next trial ...")
        stimuli = [self.create_text_stimuli(window) for _ in range(4)]
        
        iTrial = 1
        blk_counts = 0;
        # monotonic timer
        testTimer = core.MonotonicClock() 
        logFile.write(utils.get_current_time_micros()  + f'Started {self.name} trials.... \n')
        for trial in _trials:                      
            # Start counting the time
            totalPauseTime = 0.0
            # curTime = testTimer.getTime()
            # while curTime - totalPauseTime <=  self.para_exp['block_duration']:                          
            # Fixation cross
            fixation = self.present_stimuli(self.txt_color, '+', self.stimuli_positions[2],
                                            stimuli[3])
            fixation.draw()
            window.flip()
            utils.notify_beep()  
            #wait for timeout
            core.wait(constants.TIME_FIXATION)
            # present stimuli: 3 words on screen & update the screen
            # Target word
            target = self.present_stimuli(trial['colour'], trial['stimulus'],
                                          self.stimuli_positions[2], stimuli[0])
            target.draw()
            # alt1
            alt1 = self.present_stimuli(self.txt_color, trial['alt1'],
                                        self.stimuli_positions[0], stimuli[1])
            alt1.draw()
            # alt2
            alt2 = self.present_stimuli(self.txt_color, trial['alt2'],
                                        self.stimuli_positions[1], stimuli[2])
            alt2.draw()
            window.flip()
            sTime = time.time()           
            keys = event.waitKeys(maxWait=constants.TIME_ISI, keyList=constants.RESP_KEYS)
            window.flip() # Reset to blank screen
            # Log based on responses
            if keys is None: # No response collected
                logFile.write(utils.get_current_time_micros()  + "\t Trial-"+ str(iTrial)+ "\t Timeout \t fail \n")  
                resp_time = 0
                trial['Response'] = None
                trial['Accuracy'] = -1
            elif "escape" in keys:
                logFile.write(utils.get_current_time_micros() + "\t exit pressed\n")
                break
            else:
                #user pressed L/R key to update the trial responses
                # response time    
                resp_time = time.time()  - sTime    
                logFile.write(utils.get_current_time_micros() + "\t Trial-"+ str(iTrial) + "\t keypressed: " + keys[0] + "RT=\t"+ str(resp_time) +" ms\n")
            if keys is not None:
                trial['Response'] = keys[0]
                if keys[0] == trial['correctresponse']:
                    trial['Accuracy'] = 1
                else:
                    trial['Accuracy'] = 0
                
            # update trial status log
            trial['RT'] = resp_time                
            trial['Sub_id'] = self.settings['Subid']
            trial['Sex'] = self.settings['Sex']
            fileHandling.write_csv(self.settings[u'DataFile'], trial)
            # wait for next trial
            restTxt.draw()
            window.flip()
            core.wait(constants.TIME_ISI - resp_time)    
            # increment trial counter
            iTrial = iTrial+1
            curTime =  testTimer.getTime()
            if curTime - totalPauseTime >  self.para_exp['block_duration']:
                logFile.write(utils.get_current_time_micros() + f'Finished Block-{blk_counts+1}')
                curTime = 0
                testTimer = core.MonotonicClock()
                blk_counts = blk_counts + 1
                #Reset # trial  
                event.clearEvents()
                # wait for user response to go through next blocks
                if self.para_exp['stroop_main']:
                    utils.display_wait_keypressed(window, constants.MSG_KEY_PRESSED)
                else:
                    break
                # break            
                window.flip()              
            #check met the # blocks to run
            if blk_counts >=  self.para_exp['num_blocks']:
                logFile.write(utils.get_current_time_micros() + f'Reached total # blocks: {blk_counts} with total trials {iTrial-1}')
                break
        # Log experiment end and close file
        logFile.write(utils.get_current_time_micros() + f"\tEnd {self.name} task [ATT]\n")
        
    def running_practice_experiment(self, window, trials, instruction_stimuli, logFile):
        _trials = trials
        timer = core.Clock()
        stimuli = [self.create_text_stimuli(window) for _ in range(4)]
        logFile.write(utils.get_current_time_micros() + f"\t Start {self.name} practice trial \n")
        for trial in _trials:
            # Fixation cross
            fixation = self.present_stimuli(self.txt_color, '+', self.stimuli_positions[2],
                                            stimuli[3])
            fixation.draw()
            window.flip()
            utils.notify_beep()  
            
            core.wait(.6)
            timer.reset()

            # Target word
            target = self.present_stimuli(trial['colour'], trial['stimulus'],
                                          self.stimuli_positions[2], stimuli[0])
            target.draw()
            # alt1
            alt1 = self.present_stimuli(self.txt_color, trial['alt1'],
                                        self.stimuli_positions[0], stimuli[1])
            alt1.draw()
            # alt2
            alt2 = self.present_stimuli(self.txt_color, trial['alt2'],
                                        self.stimuli_positions[1], stimuli[2])
            alt2.draw()
            window.flip()

            keys = event.waitKeys(maxWait=constants.TIME_ISI, keyList=constants.RESP_KEYS)
            resp_time = timer.getTime()
            # check correct resonse or not
            if keys is not None:
                if keys[0] != trial['correctresponse']:
                    instruction_stimuli['incorrect'].draw()
    
                else:
                    instruction_stimuli['right'].draw()

            window.flip()
            core.wait(constants.TIME_ISI - resp_time)
            event.clearEvents()
            print(f"keys: {keys}")
            # if 'q' in keys:
            #     print(f"breaking because keys: {keys}")
            #     break
        logFile.write(utils.get_current_time_micros() + f"\t Finished {self.name} practice trial \n")

    def create_instructions_dict(self, instr):
        start_n_end = [w for w in instr.split() if w.endswith('START') or w.endswith('END')]
        keys = {}
        keys = fileHandling.get_keys_from_word(keys, start_n_end)
        return keys
        
    
    def create_instructions(self, window, input1, START, END, color=constants.STROOP_COLOR['background']):
        instruction_text = fileHandling.parse_instructions(input1, START, END)
        print(instruction_text)
        text_stimuli = visual.TextStim(window, text=instruction_text, wrapWidth=1.2,
                                       alignHoriz='center', color=color,
                                       alignVert='center', height=0.06)
        return text_stimuli
    
    
    def display_instructions(self, window, instruction_stimuli, logFile, start_instruction=''):
        # Display instructions
        logFile.write(utils.get_current_time_micros() + f"\t Display instruction {self.name} ----\t")
        if start_instruction == 'Practice':
            logFile.write('Practice \n')
            instruction_stimuli['instructions'].pos = (0.0, 0.5)
            instruction_stimuli['instructions'].draw()
    
            positions = [[-.4, 0], [.4, 0], [0, 0]]
            examples = [self.create_text_stimuli(window) for pos in positions]
            example_words = ['green', 'blue', 'happy']
     
            for i, pos in enumerate(positions):
                examples[i].pos = pos
                if i == 0:
                    examples[0].setText(example_words[i])
                elif i == 1:
                    examples[1].setText(example_words[i])
                elif i == 2:
                    examples[2].setColor('Green')
                    examples[2].setText(example_words[i])
    
            [example.draw() for example in examples]
    
            instruction_stimuli['practice'].pos = (0.0, -0.5)
            instruction_stimuli['practice'].draw()
    
        elif start_instruction == 'Test':
            logFile.write('Test \n')
            instruction_stimuli['test'].draw()
    
        elif start_instruction == 'End':
            logFile.write('End \n')
            instruction_stimuli['done'].draw()
    
        window.flip()
        event.waitKeys(keyList=['space'])
        event.clearEvents()

''' Testing the Class '''
Logging_Dir = os.path.join(os.getcwd(), constants.LOG_DIR)
if not os.path.exists(Logging_Dir):
    os.makedirs(Logging_Dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")    
logging_filename = os.path.join(Logging_Dir, timestamp + ".log")
logFile = open(logging_filename, "w") 

if __name__ == "__main__":
    background = "Black"
    back_color = (0, 0, 0)
    textColor = "White"
    color_profile = {"background": "Black", "text":  "White"}
    para_trials = {'num_blocks':  2,
                        'num_trials': 3,
                        'block_duration': 10,
                        }   
    # text_color = (1, 1, 1)
    experiment = Stroop(para_trials, color_profile, constants.DIR_COLOR)

    # experiment settings
    settings = {'Subid': '10', 'Experiment Version': 0.1,
                        'Sex': 'Male',
                        'Language': 'English', u'date':
                            data.getDateStr(format="%Y-%m-%d_%H:%M:%S")}

    settings[u'DataFile'] = u'' + os.getcwd() + os.path.sep + constants.LOG_DIR + os.path.sep + u'word-stroop_' + data.getDateStr(format="%Y-%m-%d_%H-%M-%S") + u'.csv'
    # language = settings['Language']

    instructions = fileHandling.read_instructions_file(os.path.join(constants.DIR_MEDIA, constants.DIR_COLOR,"INSTRUCTIONS"), settings['Language'], settings['Language'] + "End")
    instructions_dict = experiment.create_instructions_dict(instructions)
    instruction_stimuli = {}

    window =  visual.Window(monitor="WordStroopTask",   color=experiment.win_color, fullscr=False)

    for inst in instructions_dict.keys():
        instruction, START, END = inst, instructions_dict[inst][0], instructions_dict[inst][1]
        instruction_stimuli[instruction] = experiment.create_instructions(window, instructions, START, END, color=textColor)

    # We don't want the mouse to show:
    event.Mouse(visible=False)
    # Practice Trials
    # experiment.display_instructions(window, instruction_stimuli, logFile, start_instruction='Practice')
    # practice = experiment.create_trials(os.path.join(constants.DIR_MEDIA, constants.DIR_WORD,"word_practice.csv"))
    # experiment.running_practice_experiment(window, practice, logFile)
    # Test trials
    experiment.display_instructions(window, instruction_stimuli, logFile, start_instruction='Test')#(self, window, instruction_stimuli, logFile, start_instruction=''):
    trials = experiment.create_trials(os.path.join(constants.DIR_MEDIA, constants.DIR_WORD,"word_main.csv"))
    experiment.running_actual_experiment(trials, logFile)

    # End experiment but first we display some instructions
    experiment.display_instructions(window, instruction_stimuli, logFile, start_instruction='End')
    window.close()
    logFile.close()
    core.quit()
