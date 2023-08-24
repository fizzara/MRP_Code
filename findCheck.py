import cv2
import numpy as np
import threading
import tts
import pygame as pg
from PIL import Image

pg.init()
# joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
def joy():
    global fightRun
    joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
    for event in pg.event.get():
        if event.type == pg.JOYAXISMOTION:
            fightRun = True
            # print(fightRun)
        elif event.type == pg.JOYBUTTONDOWN:
            fightRun = True
            # print(fightRun)

def heartText(image, template="undertaleHeart.png"): #template is image of heart, image is the frame the heart should be found in   
#*finds heart, crops text next to it, returns text

    img = cv2.imread(image) #load image
    template = cv2.imread(template) #load template
    height, width, _ = template.shape #find height+width of template and save as var

    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF) #run the image search to find the template
    _, _, minL, _ = cv2.minMaxLoc(result) #return location coord of the heart
    minL = (minL[0] + width, minL[1]) #move x coord of minL to cut out heart

    crop = img[minL[1]:minL[1]+height+10, minL[0]:minL[0]+215] #crop the word right past the heart
    return tts.read(crop)
    # t = threading.Thread(target=tts.speak, args=[tts.read(crop), "cropped.mp3"]) #in a thread, read the cropped image and save/speak it
    # t.start()
    # cv2.imshow("text", crop)
    # cv2.waitKey(0)


readHold = ""
punctuation = (" ", ",", ".", "!", "?", "\n")
run = True
fightRun = True
checkHold = "None"
checker = "none"

def fightList(image, template="heartasterisk.png", threshold=0.7):
    global run
    global checker
    global checkHold
    global fightRun
    holdLoc = []
    if checker != checkHold:
        checkRun = True
        checkHold = checker
    # try:
    # image = cv2.imread(image)
    # except:
    #     pass
    template = cv2.imread(template)
    match = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(match >= threshold) #when a threshold is needed
    locations = list(zip(*locations[::-1])) #to make the locations into pleasing arrays // ::-1 reverses list, * unpacks the list, list(zip creates new lists off matching indexes  
    
    joy()

    if locations:
        # print(holdLoc, locations)
        if fightRun:
            crop = image[locations[0][1]:locations[0][1]+34, locations[0][0]+template.shape[1]:locations[0][0]+template.shape[1]+225]
            holdLoc = locations
            tts.speak(tts.read(crop))
            run = True
            fightRun = False
    elif run:
        global readHold
        template = cv2.imread("asterisk.png")
        match = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(match >= threshold) #when a threshold is needed
        locations = list(zip(*locations[::-1])) #to make the locations into pleasing arrays // ::-1 reverses list, * unpacks the list, list(zip creates new lists off matching indexes  
        if locations:
            crop = image[locations[0][1]:locations[0][1]+110, locations[0][0]+template.shape[1]:image.shape[1]]
            reading = tts.read(crop)
            if reading == readHold:
                tts.speak(reading)
                readHold = reading
                run = False
            else:
                readHold = reading
                run = True
        else:
            run = True


def asterisk(image, template="asterisk.png", threshold=0.9): #currently specifically for checking if player in fight
    global readHold
    global run
    template = cv2.imread(template)
    match = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # _, _, minLoc, maxLoc = cv2.minMaxLoc(match) #only useful for exact match
    # print(minLoc, maxLoc)
    locations = np.where(match >= threshold) #when a threshold is needed
    locations = list(zip(*locations[::-1])) #to make the locations into pleasing arrays // ::-1 reverses list, * unpacks the list, list(zip creates new lists off matching indexes  
    if locations:
        crop = image[locations[0][1]:locations[0][1]+110, locations[0][0]+template.shape[1]:image.shape[1]]
        reading = tts.read(crop)
        if readHold != reading:
            run = True
        if run and reading == readHold:
            tts.speak(reading)
            readHold = reading
            run = False
        else:
            readHold = reading
    else:
        run = True
    

#* y, x
#* b, g, r

def checkCol(arr, col):  #used to check if the pixel's BGR value is similar to the yellow we're looking for, meaning it is selected
    if col.lower() == "red":
        if arr[0] < 25 and arr[1] < 10 and arr[2] > 225: 
            return True
        else:
            return False
    if col.lower() == "white":
        if arr[0] > 240 and arr[1] > 240 and arr[2] > 240:
            return True
        else:
            return False
    if col.lower() == "green":
        if arr[0] < 50 and arr[1] > 240 and arr[2] > 180:
            return True
        else:
            return False


def checkAction(frame):
    global checker
    h, w, _ = frame.shape
    if checkCol(frame[int(h*0.95), int(w*0.075)], "red") and checker != "fight":
        # t = threading.Thread(target=tts.speak, args=["fight", "fight"])
        # t.start()
        tts.speak("fight", "fight")
        checker = "fight"
    elif checkCol(frame[int(h*0.95), int(w*0.3125)], "red") and checker != "act":
        # t = threading.Thread(target=tts.speak, args=["act", "act"])
        # t.start()
        tts.speak("act", "act")
        checker = "act"
    elif checkCol(frame[int(h*0.95), int(w*0.5625)], "red") and checker != "item":
        # t = threading.Thread(target=tts.speak, args=["item", "item"])
        # t.start()
        tts.speak("item", "item")
        checker = "item"
    elif checkCol(frame[int(h*0.95), int(w*0.8046875)], "red") and checker != "mercy":
        # t = threading.Thread(target=tts.speak, args=["mercy", "mercy"])
        # t.start()
        tts.speak("mercy", "mercy")
        checker = "mercy"
    elif not checker == "none" and not checkCol(frame[int(h*0.95), int(w*0.075)], "red") and not checkCol(frame[int(h*0.95), int(w*0.3125)], "red") and not \
        checkCol(frame[int(h*0.95), int(w*0.5625)], "red") and not checkCol(frame[int(h*0.95), int(w*0.8046875)], "red"): #for some reason elif statements were ruining the code
        checker="none"


def interactionType(frame): #true = in fight, false = not in fight  
    # frame = cv2.imread(frame)
    h, w, _ = frame.shape
    convCol = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    im = Image.fromarray(convCol)
    pix = im.load()
    if checkCol(pix[w*0.05, h*0.6], "white") and checkCol(pix[w*0.94375, h*0.6], "white"):  #not fighting
        return False
    elif checkCol(pix[w*0.371875, h*0.6], "white") and checkCol(pix[w*0.621875, h*0.6], "white"): #fighting
        return True
    # return True
