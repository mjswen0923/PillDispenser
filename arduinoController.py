from bs4 import BeautifulSoup
import requests
import serial
import datetime
import time
import os

# Will communicate to the Arduino using the serial library over usb
arduinoSerialData = serial.Serial('/dev/ttyUSB0', 9600)

# Send a preliminary number to turn make sure the Arduino is reading it correctly
# Should not actually dispense a pill
arduinoSerialData.write('1')

# We in this for the long haul
while True:

    pill1_hour_list = []
    pill1_minute_list = []
    pill1_numpills = []
    pill2_hour_list = []
    pill2_minute_list = []
    pill2_numpills = []
    pill3_hour_list = []
    pill3_minute_list = []
    pill3_numpills = []

    # Get the website data from the URL
    r = requests.get("http://0.0.0.0:80")
    
    # Grab and transcribe the raw html using Beautiful Soup
    data = r.content
    page_soup = BeautifulSoup(data, "html.parser")

    # Find and store all the time elements on the web page
    pill1 = page_soup.findAll("td", {"class": "pill1Time"})
    pill2 = page_soup.findAll("td", {"class": "pill2Time"})
    pill3 = page_soup.findAll("td", {"class": "pill3Time"})
    numpill1 = page_soup.findAll("td", {"class": "pill1num"})
    numpill2 = page_soup.findAll("td", {"class": "pill2num"})
    numpill3 = page_soup.findAll("td", {"class": "pill3num"})

    # Loop through all elements in the list of pill times and store them in lists
    for x in range(len(pill1)):
        # Add the number of pills in the list
        pill1_numpills.append(int(numpill1[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill1[x].text.split()
        pill1_hour_list.append(this_time[0])
        pill1_minute_list.append(this_time[2])

    for x in range(len(pill2)):
        # Add the number of pills in the list
        pill2_numpills.append(int(numpill2[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill2[x].text.split()
        pill2_hour_list.append(this_time[0])
        pill2_minute_list.append(this_time[2])

    for x in range(len(pill3)):
        # Add the number of pills in the list
        pill3_numpills.append(int(numpill3[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill3[x].text.split()
        pill3_hour_list.append(this_time[0])
        pill3_minute_list.append(this_time[2])

    # Update the current time
    now = datetime.datetime.now()
    print(now)

    # This is where the signal gets sent to the Arduino to actually turn on the motors
    # The way it is sent is a little interesting
    # Essentially, you have three motors and you have the number of pills that need to be dispensed for each motor
    # So what gets sent is a string with the corresponding pill motor and the number of pills with it
    # For example, 11 would mean turn on motor 1 for 1 rotation
    # This means you cannot have more than 9 pills

    for x in range(len(pill1_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill1_hour_list[x]) and now.minute == int(pill1_minute_list[x]):
            arduinoSerialData.write(str(10 + pill1_numpills[x]))
            # Allows you to see it actually working
            print("Dispensing Pill")
    for x in range(len(pill2_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill2_hour_list[x]) and now.minute == int(pill2_minute_list[x]):
            arduinoSerialData.write(str(20 + pill2_numpills[x]))
            # Allows you to see it actually working
            print("Dispensing Pill")
    for x in range(len(pill3_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list\
        if now.hour == int(pill3_hour_list[x]) and now.minute == int(pill3_minute_list[x]):
            arduinoSerialData.write(str(30 + pill3_numpills[x]))
            # Allows you to see it actually working
            print("Dispensing Pill")

    # This is dependent on how fast the machine is. For us it would generally take a second to run through the code
    time.sleep(59)
