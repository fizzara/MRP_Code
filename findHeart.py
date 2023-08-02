import cv2
import numpy as np
import threading
import tts

#!depreciated, only shows heart
def findHeart(image, template="undertaleHeart.png"): #template is image of heart, image is the frame the heart should be found in
    img = cv2.imread(image) #load image
    template = cv2.imread(template) #load template
    height, width, _ = template.shape #find height+width of template and save as var

    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF) #run the image search to find the template
    _, _, minL, _ = cv2.minMaxLoc(result) #return location coord of the heart
    #!minL = x, y

    botR = (minL[0] + height, minL[1] + width) #set the bottom right of the coordinates we want.
    #!botR = x, y

    # cv2.rectangle(img2, minL, botR, 255, 2)
    # cv2.imshow("match.png", img2)
    # cv2.waitKey(0)
    print(minL, botR) #print coords for knowledges sake

    cropped = img[minL[1]:botR[1], minL[0]:botR[0]] #create a cropped image from the original image using the coords
    cv2.imshow("test", cropped) 
    cv2.waitKey(0)

def heartText(image, template="undertaleHeart.png"):
    #*Actual one to use, finds heart, shows text beside it, returns image of text and says text
    #TODO: Need to make it so this only works while in the dialogue box, not in act
    #TODO: bring act checker into here? technically finding heart

    img = cv2.imread(image)
    template = cv2.imread(template)
    height, width, _ = template.shape

    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)
    _, _, minL, _ = cv2.minMaxLoc(result)
    minL = (minL[0] + width, minL[1])

    crop = img[minL[1]:minL[1]+height+10, minL[0]:minL[0]+215] #crop the word right past the heart
    t = threading.Thread(target=tts.speak, args=[tts.read(crop), "cropped.mp3"]) #in a thread, read the cropped image and save/speak it
    t.start()
    cv2.imshow("text", crop)
    cv2.waitKey(0)

findHeart("saved2.png")


