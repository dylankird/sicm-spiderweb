#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
import random

correctPressed=False

touch_sensor = 0

buttons = [7, 1, 2, 3, 4]

motors = [5, 6, 16, 17, 22]

lights = [23, 24, 25, 26, 27]

GPIO.setmode(GPIO.BCM)

#Initialize GPIO:

for x in buttons:
    GPIO.setup(x, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for x in motors:
    GPIO.setup(x, GPIO.OUT)

for x in lights:
    GPIO.setup(x, GPIO.OUT)

GPIO.setup(touch_sensor, GPIO.IN)

#Start looping the ambient sound

os.system('nohup mpg123 --loop -1 /home/pi/audio/001.MP3 &')


def randomize(number):
    #This function creates a random sequence for flashing the bugs and buzzing the strings
    for x in range(number):
        new = random.randrange(0,5)
        if(x > 0):
            while(new == sequence[x-1]): 
                new = random.randrange(0,5)
        sequence.append(new)
        print(sequence[x])

def buzz_randomly(number):
    #Randomly buzz the motor of 'number' for 30 seconds
    buzzTime = 0
    while((buzzTime < 30) and (correctPressed == False)):
        newTime = random.uniform(0.1, 0.5)
        buzzTime += newTime
        GPIO.output(motors[number], GPIO.HIGH)
        time.sleep(newTime)
        newTime = random.uniform(0.3, 0.8)
        buzzTime += newTime
        GPIO.output(motors[number], GPIO.LOW)
        time.sleep(newTime)


def correct_callback(channel):
    #Callback for when the correct button was pushed
    print("CORRECT")
    global correctPressed
    correctPressed=True

   

def wrong_callback(channel):
    #Callback for when the wrong button was pushed
    print("WRONG")
    #Play "Not over here...":
    os.system('pkill mpg123')
    os.system('nohup mpg123 audio/006.MP3 &')

def start_interrupts(number):
    #Starts the interrupts with 'number' being the button number that is the correct choice
    GPIO.add_event_detect(buttons[number], GPIO.FALLING, callback=correct_callback, bouncetime=200)
    for x in range(5):
        if(x != number):
            GPIO.add_event_detect(buttons[x], GPIO.FALLING, callback=wrong_callback, bouncetime=200)

def stop_interrupts():
    #Stops the interrupts
    for x in range(5):
        GPIO.remove_event_detect(buttons[x])

#Main loop:
while True:
    if(GPIO.input(touch_sensor) == 1): #If web is touched
        correctPressed=False    #Initialize variable that tells if correct button was pressed
        os.system('pkill mpg123') #Stops ambient sounds
        print("Button touched")
        sequence = [] #Initializes empty global array to hold random sequence of buzzes/flashes
        randomize(15) #Create random sequence 15 long

        for x in sequence:  #Flash lights and buzz strings accordingly
            GPIO.output(motors[x], GPIO.HIGH)
            GPIO.output(lights[x], GPIO.HIGH)
            time.sleep(0.25)
            GPIO.output(motors[x], GPIO.LOW)
            GPIO.output(lights[x], GPIO.LOW)
        os.system('nohup mpg123 audio/002.MP3 &')   #Play the "Something touched my web..." line

        bugNum = random.randrange(0,5)  #Decide which bug is "caught" in the web
        start_interrupts(bugNum)
        buzz_randomly(bugNum)
        if(not correctPressed):
            #Play "I still can't find my dinner..." (003) 
            os.system('pkill mpg123')
            os.system('nohup mpg123 audio/003.MP3 &')
        buzz_randomly(bugNum)
        stop_interrupts()
        if(correctPressed):
            #Play "Thanks for helping me..."
            os.system('pkill mpg123')
            os.system('nohup mpg123 audio/004.MP3 &')
            for x in range(10):
                GPIO.output(lights[bugNum], GPIO.HIGH)
                time.sleep(0.25)
                GPIO.output(lights[bugNum], GPIO.LOW)
                time.sleep(0.25)
            time.sleep(3)
        else:
            #Play "Let's play again..."
            os.system('pkill mpg123')
            os.system('nohup mpg123 audio/005.MP3 &')
            time.sleep(6)
        os.system('nohup mpg123 --loop -1 /home/pi/audio/001.MP3 &')

    time.sleep(0.05)


