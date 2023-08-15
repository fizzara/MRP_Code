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
    #TODO: Need to make it so this only works while in the dialogue box, not in act
    #TODO: bring act checker into here? technically finding heart

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

# fightList("hollup.png")

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
    

# asterisk("torieltalking.png", "asterisk.png")

# exists("frog243.jpg", "heartback.png", 0.515)

#* y, x
#* b, g, r
#453, 173 = fight
#452, 327 = act
#446, 541 = item
#447, 641 = mercy

#299, 344 < small box
#304, 141 < large box

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
    # print(checker)
    # print(frame[int(h*0.95), int(w*0.3125)])
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

#314, 142
#301, 707   
#34, 280
# 0.05, 0.6
# 0.94375

def interactionType(frame): #true = in fight, false = not in fight  
    # frame = cv2.imread(frame)
    h, w, _ = frame.shape
    convCol = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    im = Image.fromarray(convCol)
    pix = im.load()
    # print(f"{pix[w*0.05, h*0.6]}; {pix[w*0.94375, h*0.6]}; {pix[w*0.371875, h*0.6]}; {pix[w*0.621875, h*0.6]}")
    # try:
    #     checkCol(pix[299, 503], "white")
    # except:
    #     frame = frame[299:503, 299:344]
    #     cv2.imwrite("problemcrop.png", frame)
    #     print(pix[503, 299])
    # print(pix[w*0.05, h*0.6], pix[w*0.94375, h*0.6], pix[w*0.371875, h*0.6], pix[w*0.621875, h*0.6])
    if checkCol(pix[w*0.05, h*0.6], "white") and checkCol(pix[w*0.94375, h*0.6], "white"):  #not fighting
        return False
    elif checkCol(pix[w*0.371875, h*0.6], "white") and checkCol(pix[w*0.621875, h*0.6], "white"): #fighting
        return True
    # return True

#287, 168
#262, 149 - 381, 701 (y,x)




# def tester(frame):
#     h = 480
#     w = 640
#     # im = Image.open(frame)
#     frame = cv2.imread(frame)
#     crop2 = frame[(int(h*0.525)):(int(h*0.80625)), (int(w*0.3734375)):(int(w*0.6234375))] 
#     templ = cv2.imread("undertaleHeart.png")
#     match2 = cv2.matchTemplate(crop2, templ, cv2.TM_CCOEFF_NORMED)
#     _, _, _, maxLoc = cv2.minMaxLoc(match2)
#     print(maxLoc)
#     # match2 = np.where(match2 >= 0.8)
#     # match2 = list(zip(*match2[::-1]))
#     # print(match2)

#     cv2.rectangle(crop2, (maxLoc[0]-10, maxLoc[1]-10), (maxLoc[0]+templ.shape[1]+10, maxLoc[1]+templ.shape[0]+10), 255, 1)
#     cv2.imshow("C", crop2)
#     cv2.waitKey(0)

# tester("fightbox.png")


# def depr_fightTalk(image):
#     global frameNum 
#     frameNum = frameNum + 1
#     convCol = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
#     img = Image.fromarray(convCol)
#     pix = img.load()
#     # if(checkCol(pix[169, 286], "white")):
#     run = True
#     global readHold
#     # im = cv2.imread(image)
#     # print(f"int = {interactionType(image)}, col = {checkCol(pix[286, 168], 'white')}")
#     # print(pix[168, 286])
#     if not interactionType(image) and checkCol(pix[169, 286], "white"):
#         # crop = im.crop((149, 262), (701, 381))
#         crop = image[262:381, 149:701]
#         # cv2.imread(crop)
#         reading = tts.read(crop)
#         # print(reading + "$")
#         if len(reading) > 3: #TODO: Need to add somewhere "if not str[-1].isalpha(), str = str[:-1]
#             reading = reading[:-2] #TODO: cont: maybe remove it from readhold? to ensure that the word in tbs isnt cut off? S
#         # print("r=", reading) #TODO: ok that seems to be solved but now you need to figure out why sometimes readhold has too many characters
#         if len(readHold) > 1:
#             readHold = readHold[:-1]
#         # print("rh=", readHold)
#         # with open('readme.txt', 'w') as f:
#         #     f.write(reading)
#         if len(reading) > 1 and not reading[-1].isalpha(): #if at a non alpha
#             # print(f"hold={readHold}, reading={reading}")
#             tbs = reading[len(readHold):]
#             # print("tbs=", tbs)
#             # for i in tbs:
#             #     if i.isalpha():
#             #         run = True
#             # if run:
#             #     tts.speak(tbs, "tbs.mp3")
#             # # print(tbs)
#             tts.speak(tbs, "tbs.mp3")
#             readHold = reading
#             # print(readHold)
            
#         # tts.speak(tts.read(crop), "reading")

        
# def depr_talk(image):
#     global readHold
#     global frameNum
#     global run
#     convCol = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
#     img = Image.fromarray(convCol)
#     pix = img.load()
#     # if(checkCol(pix[169, 286], "white")):
#     # im = cv2.imread(image)
#     # print(f"int = {interactionType(image)}, col = {checkCol(pix[286, 168], 'white')}")
#     # print(pix[168, 286])
#     if not checkCol(pix[169, 286], "white"):
#         run = True
#     if frameNum % 10 == 0: #wait until is the same after 10 frames, to make sure text isn't just taking a pause
#         if not interactionType(image) and checkCol(pix[169, 286], "white"):
#             crop = image[262:381, 149:701]
#             reading =  tts.read(crop)
#             if reading == readHold:
#                 tts.speak(reading)
#                 run = False
#             elif run:
#                 readHold = reading
#     frameNum += 1    


# fightTalk("talking.png")
# interactionType("fight.png")