#!/home/raspberrypi/alarmProj/alarmProj/bin/python3
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from threading import Thread
import time
import os

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
# oled_dc = digitalio.DigitalInOut(board.D6)
# oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
timeArr = [0, 0, 0, 0, 0, 0]
timeArrCount = 0
#Sorting out the set input after a 30 second delay
userInp = None
def ask():
	global startTime, answer
	startTime = time.time()
#Loop function
def loop(timeArrCount):

	draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

	# Draw a smaller inner rectangle
	draw.rectangle(
		(BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
		outline=0,
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
	userInp = input("d to move right, w to move time value up, s to move time value down")
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
	print(timeArr[timeArrCount])
	return timeArrCount
# Draw a white background
def destroy():
	oled.fill(0)
	oled.show()
	print("Destroyed")
if __name__ == "__main__":
	try:
		while True:
			timeArrCount = loop(timeArrCount)
	except KeyboardInterrupt:
		destroy()




