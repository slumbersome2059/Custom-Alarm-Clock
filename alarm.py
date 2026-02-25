#!/home/raspberrypi/alarmProj/alarmProj/bin/python3
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from threading import Thread
import time
import os
import datetime
import RPi.GPIO as GPIO
RoAPin = 11    # CLK Pin
RoBPin = 12    # DT Pin
BtnPin = 13    # Button Pin

globalCounter = 0

flag = 0
lastUserInp = None
GPIO.setup(RoAPin, GPIO.IN)    # input mode
GPIO.setup(RoBPin, GPIO.IN)
GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
Last_RoB_Status = 0
Current_RoB_Status = 0
def rotaryDeal():
        global flag
        global Last_RoB_Status
        global Current_RoB_Status
        global globalCounter
        global userInp
        Last_RoB_Status = GPIO.input(RoBPin)
        while(not GPIO.input(RoAPin)):
                Current_RoB_Status = GPIO.input(RoBPin)
                flag = 1
        if flag == 1:
                flag = 0
                if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
                        globalCounter = globalCounter - 1
                elif(Last_RoB_Status == 1) and (Current_RoB_Status == 0):
                        globalCounter = globalCounter + 1
tmp = 0
def rotLoop():
        global globalCounter
        global userInp
        tmp = 0 # Rotary Temperary
        # no loop for next time
        while True:
                t1 = Thread(target=newWayRotary)
                t1.start()
                timing()
                print ('globalCounter = %d' % globalCounter)
                time.sleep(0.1)
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
                                manageUserInp("w")
                                break
                        elif(modCount%2 == 0):
                                globalCounter-=1
                                print(globalCounter)
                                manageUserInp("s")
                                break
                        modCount+=1
                elif(askButton()==True):
                        manageUserInp("d")
                        break
                else:
                        userInp = None
                aLastState = aState
def askButton():
    val = GPIO.input(BtnPin)
    if(val == 0):
            return True
    return False
def play_alarm(hour, minute, second):
    alarm_time = datetime.datetime.now().replace(hour=hour, minute=minute, second=second)
    # Get the current time and set the alarm time to 7:00 AM
    print(alarm_time)
    while True:
        current_time = datetime.datetime.now()
        # Get the current time

        if current_time >= alarm_time:
            print("Wake up!")  # Print "Wake up!" to the console
            #Play the WWMC file
            break

        else:
            time.sleep(1)  # Wait for 1 second before checking the time again

userInp = None
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
            print("Not entered quick enough")
            hour = timeArr[0]*10 + timeArr[1]
            minute = timeArr[2]*10 + timeArr[3]
            second = timeArr[4]*10 + timeArr[5]
            play_alarm(hour, minute, second)
            break
        time.sleep(0.001)

#Turn timing into the loop function but with the loop now
#set timeArrCount as a global variable instead of passing it in as a parameter
#Make more functions so a display function and so on


# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Use for SPI
# spi = board.SPI()
# oled_cs = digitalio.DigitalInOut(board.D5)
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
timeArr = [0, 0, 0, 0, 0, 0]
timeArrCount = 0
#Manage user input
def manageUserInp(userInp):#Make sure to remove the
    global timeArrCount, timeArr
    if(userInp == "d"):
        timeArrCount += 1
        timeArrCount = timeArrCount % 6
        print("Moved right")
    elif(userInp == "w"):
        timeArr[timeArrCount] += 1
        print(timeArr[timeArrCount])
    elif(userInp == "s"):
        timeArr[timeArrCount] -= 1
        if(timeArr[timeArrCount] < 0):
            if(timeArrCount == 0):
                timeArr[timeArrCount] = 2
            elif(timeArrCount % 2 == 0):
                timeArr[timeArrCount] = 5
            else:
                timeArr[timeArrCount] = 9
    if(timeArrCount == 0):
        timeArr[timeArrCount] %= 3
    elif(timeArrCount % 2 == 0):
        timeArr[timeArrCount] %= 6
    else:
        timeArr[timeArrCount] %= 10

#Sorting out the set input after a 30 second delay
userInp = None
#Loop function
def loop():
    global timeArr, timeArrCount, userInp

    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    # Draw a smaller inner rectangle
    draw.rectangle(
        (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
        outline=0,t1 = Thread(target=newWayRotary)
                t1.start()
                timing()
                print ('globalCounter = %d' % globalCounter)
                time.sleep(0.1)
        fill=0,
    )
    font = ImageFont.load_default()
    # Draw Some Text
    hours1Str = str(timeArr[0])
    hours2Str = str(timeArr[1])
    minutes1Str = str(timeArr[2])
    minutes2Str = str(timeArr[3])
    seconds1Str = str(timeArr[4])
    seconds2Str = str(timeArr[5])
    text = hours1Str + hours2Str + ":" + minutes1Str + minutes2Str + ":" + seconds1Str + seconds2Str
    bbox = font.getbbox(text)
    (font_width, font_height) = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )
    #display image
    oled.image(image)
    oled.show()
    #Asking for the input
    userInp = None
    t1 = Thread(target=newWayRotary)
    t1.start()
    timing()
    print('globalCounter = %d' % globalCounter)
    #print(userInp)
    #print(timeArr)

# Draw a white background
def destroy():
    oled.fill(0)
    oled.show()
    print("Destroyed")
if __name__ == "__main__":
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        destroy()


