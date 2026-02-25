#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from threading import Thread
import time
import os

RoAPin = 11   # CLK Pin
RoBPin = 12    # DT Pin
BtnPin = 13    # Button Pin

globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0
userInp = None
def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(RoAPin, GPIO.IN)    # input mode
	GPIO.setup(RoBPin, GPIO.IN)
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def rotaryDeal():
	global flag
	global Last_RoB_Status
	global Current_RoB_Status
	global globalCounter
	global userInp
	global startTime
	startTime = time.time()
	prevCount = globalCounter
	while prevCount == globalCounter:
		Last_RoB_Status = GPIO.input(RoBPin)
		while(not GPIO.input(RoAPin)):
			Current_RoB_Status = GPIO.input(RoBPin)
			flag = 1
			userInp = None
		if flag == 1:
			flag = 0
			if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
				globalCounter = (globalCounter - 1)
				userInp = "s"
			elif(Last_RoB_Status == 1) and (Current_RoB_Status == 0):
				globalCounter = (globalCounter + 1)
				userInp = "w"
			else:
				userInp = None
	time.sleep(0.2)
def newWayRotary():
	global aLastState
	global startTime
	global userInp
	global globalCounter
	startTime = time.time()
	aLastState = GPIO.input(RoAPin)
	aState = GPIO.input(RoAPin)
	modCount = 0
	while True:
		aState = GPIO.input(RoAPin)
		if(aState != aLastState):
		#this shows that the shaft is moving
			if(aState != GPIO.input(RoBPin) and modCount % 2 == 0):
				#basically the BPin or APin will always be 90 degrees out of phase behind
				#determining the order allows you to determine direction
				globalCounter+=1
				print(globalCounter)
				userInp = "w"
				break
			elif(modCount%2 == 0):
				globalCounter-=1
				print(globalCounter)
				userInp = "s"
				break
			modCount+=1
		elif(askButton()==True):
			userInp = "d"
		else:
			userInp = None
		aLastState = aState
def askButton():
	global globalCounter
	val = GPIO.input(BtnPin)
	if(val == 0):
		globalCounter = 0
		return True
	else:
		return False
def ask():
    global startTime, userInp
    startTime = time.time()
    rotaryDeal()
    time.sleep(0.001)
def timing():
    global timeArr, userInp
    timeLim = 30
    while True:
        timeTaken = time.time() - startTime
        if userInp is not None:
            print("Entered input")
            break
        if timeTaken > 10:
            print("Too much time taken")
            break
        time.sleep(0.001)
def rotLoop():
	global globalCounter
	global userInp
	tmp = 0	# Rotary Temperary
	# no loop for next time
	while True:
		t1 = Thread(target=newWayRotary)
		t1.start()
		timing()
		print ('globalCounter = %d' % globalCounter)
		time.sleep(0.1)
def destroy():
	GPIO.cleanup()             # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		rotLoop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
