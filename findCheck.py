import cv2
import numpy as np
import threading
import tts
from PIL import Image

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

def exists(image, template):
    image = cv2.imread(image)
    template = cv2.imread(template)
    match = cv2.matchTemplate(image, template, cv2.TM_SQDIFF)
    match2 = cv2.minMaxLoc(match)
    for x in match:
        if x.all() > 0.95:
            print(x.all())
            break

# exists("text.png", "undertaleHeart.png")

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
        if arr[0] < 10 and arr[1] < 10 and arr[2] > 230: 
            return True
        else:
            return False
    if col.lower() == "white":
        if arr[0] == 255 and arr[1] == 255 and arr[2] == 255:
            return True
        else:
            return False

checker = "none"

def checkAction(frame):     #?can use pyautogui for screen pixel? quicker? /// probably for actual gameplay
    global checker
    if checkCol(frame[454, 155], "red") and checker != "fight":
        t = threading.Thread(target=tts.speak, args=["fight", "fight"])
        t.start()
        # tts.speak("fight", "fight")
        checker = "fight"
    elif checkCol(frame[454, 308], "red") and checker != "act":
        t = threading.Thread(target=tts.speak, args=["act", "act"])
        t.start()
        # tts.speak("act", "act")
        checker = "act"
    elif checkCol(frame[454, 465], "red") and checker != "item":
        t = threading.Thread(target=tts.speak, args=["item", "item"])
        t.start()
        # tts.speak("item", "item")
        checker = "item"
    elif checkCol(frame[454, 619], "red") and checker != "mercy":
        t = threading.Thread(target=tts.speak, args=["mercy", "mercy"])
        t.start()
        # tts.speak("mercy", "mercy")
        checker = "mercy"
    elif not checker == "none" and not checkCol(frame[454, 155], "red") and not checkCol(frame[454, 308], "red") and not \
        checkCol(frame[454, 465], "red") and not checkCol(frame[454, 619], "red"): #for some reason elif statements were ruining the code
        checker="none"

def interactionType(frame): #true = in fight, false = not in fight  
    convCol = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    im = Image.fromarray(convCol)
    pix = im.load()
    if checkCol(pix[299, 344], "white") and checkCol(pix[299, 503], "white"):
        return True
    else:
        return False

#287, 168
#262, 149 - 381, 701 (y,x)
readHold = "Froggit "
punctuation = (" ", ",", ".", "!", "?", "\n")
def fightTalk(image):
    global readHold
    # im = cv2.imread(image)
    convCol = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    img = Image.fromarray(convCol)
    pix = img.load()
    if checker == "none" and not interactionType(image) and checkCol(pix[169, 286], "white"):
        # crop = im.crop((149, 262), (701, 381))
        crop = image[262:381, 149:701]
        # cv2.imread(crop)
        reading = tts.read(crop)
        # with open('readme.txt', 'w') as f:
        #     f.write(reading)
        if reading[-1] in punctuation: #if at a punctuation or space:
            tbs = reading[len(readHold):]
            tts.speak(tbs, "tbs.mp3")
            # print(tbs)
            readHold = reading
            # print(readHold)
            
        # tts.speak(tts.read(crop), "reading")

# fightTalk("talking.png")
# interactionType("talking.png")