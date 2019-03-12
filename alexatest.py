# Called alexatest.py in RPI, this program creates a text file 'alexa_output' and writes
import logging
import os
import time
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO
import subprocess
import sys
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on','high']
STATUSOFF = ['off','low']
STATUSDRIVE = ['go', 'start', 'drive']
STATUSSTOP = ['stop', 'end', 'pause']
STATUSORIENTATION = ['left', 'right']
STATUSMODE = ['local', 'user', 'autonomous']
LOCALANGLE = ['local_angle','local angle','cyborg']
model_proc = None

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text) #keeps session open

@ask.intent('GpioIntent', mapping={'light_status':'light_status'})
def Gpio_Intent(light_status,room):
        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(21,GPIO.OUT)
    if light_status in STATUSON:
            #GPIO.output(21,GPIO.HIGH)
            #print("light turned on")
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('GPIO.HIGH\n')
        f.flush()
        f.close
        return statement('turning {} lights'.format(light_status))
    elif light_status in STATUSOFF:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('GPIO.LOW\n')
        f.flush()
        f.close
        return statement('turning {} lights'.format(light_status))
    else:
        return statement('Sorry not possible.')

@ask.intent('DriveIntent', mapping={'drive_status':'drive_status', 'time_status':'time_status'})
def Drive_Intent(drive_status, time_status, room):
    print("Got here")
    if drive_status in STATUSDRIVE:
        if time_status:
            f = open('alexa_output', 'w',os.O_NONBLOCK)
            f.seek(0)
            f.write('DRIVEMODE1 {}\n'.format(time_status))
            f.flush()
            f.close
                    # self.time_elapsed = time_status
                    # self.time_start = time.clock()
        else:
            f = open('alexa_output', 'w',os.O_NONBLOCK)
            f.seek(0)
            f.write('DRIVEMODE1\n')
            f.flush()
            f.close
                    #     self.time_elapsed = 5
                    #     self.time_start = time.clock()
        print("Donkey starting to drive")
                    #sleep(1)
        return statement('car moving')
    elif drive_status in STATUSSTOP:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('STOP\n')
        f.flush()
        f.close
                #self.emergency_stop()
        return statement('car stopping')
    else:
        return statement('Sorry not possible.')
@ask.intent('OrientationIntent', mapping={'orientation_status':'orientation_status'})
def Orientation_Intent(orientation_status, room):
    print("Got here")
    if orientation_status == "you":
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('ORIENT {}\n'.format("left"))
        f.flush()
        f.close
        return statement('car turning {}'.format("u-turn"))
    elif orientation_status in STATUSORIENTATION:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('ORIENT {}\n'.format(orientation_status))
        f.flush()
        f.close
        return statement('car turning {}'.format(orientation_status))
    else:
        return statement('Sorry not possible.')
@ask.intent('ModeIntent', mapping={'mode_status':'mode'})
def Mode_Intent(mode_status, room):
    print(mode_status)
    if mode_status in STATUSMODE:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('MODE {}\n'.format(mode_status))
        f.flush()
        f.close
        return statement('Mode switched to {}'.format(mode_status))
    elif mode_status in LOCALANGLE:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('MODE {}\n'.format("local_angle"))
        f.flush()
        f.close
        return statement('Mode switched to {}'.format("local_angle"))
    else:
        return statement('Sorry not possible.')
@ask.intent('EraseRecordsIntent', mapping={'number':'number', 'all':'all'})
def Erase_Records_Intent(number, all, room):
    print(number)
    if number:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('ERASERECORDS {}\n'.format(number))
        f.flush()
        f.close
        return statement('{} records erased'.format(number))
    elif all:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('ERASERECORDS ALL')
        f.flush()
        f.close
        return statement('All records erased')
    else:
        return statement('Sorry not possible.')
@ask.intent('ModelIntent', mapping={'model':'model'})
def Model_Intent(model):
    print("In Model_intent")
    model_file = None
    if model == 'outdoors':
        model_file = '20190225_outdoor_v2.h5'
    elif model == 'indoors':
        model_file = '20190213_indoors.h5'
    elif model == 'fancy':
        model_file = '20190213_indoors.h5'
    else:
        return statement('Sorry not possible.')
    #model_proc.kill()
    #model_proc = subprocess.Popen( ['python','manage.py','drive', '--model=models/' + model_file], stdout=subprocess.PIPE)
    return statement('Model switched to {}'.format(model))
@ask.intent('ThrottleIntent', mapping={'modifier':'modifier','number':'number'})
def Throttle_Intent(modifier, number):
    if modifier:
        if modifier == "toggle constant" or modifier == "set constant":
            modifier = "constant"
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write(modifier)
        f.flush()
        f.close
        return statement('Throttle ' + modifier)
    elif number:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('THROTTLE {}\n'.format(number))
        f.flush()
        f.close
        return statement('Throttle set to '+number)
    else:
        return statement('Sorry not possible')
@ask.intent('RecordingIntent', mapping={'status':'status'})
def Recording_Intent(status):
    if status in STATUSON:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write("RECORDING on")
        f.flush()
        f.close
        return statement('recording turned on')
    elif status in STATUSOFF:
        f = open('alexa_output', 'w',os.O_NONBLOCK)
        f.seek(0)
        f.write('RECORDING off')
        f.flush()
        f.close
        return statement('recording turned off')
    else:
        return statement('Sorry not possible')  
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ: #checks OS "environment" to verify what is happening
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(host = '0.0.0.0')
    #model_proc = subprocess.Popen( ['python','manage.py','drive', '--model=models/20190213_indoors.h5'], shell=True,stdout=subprocess.PIPE)   
