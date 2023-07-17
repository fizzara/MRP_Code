
#* Fizza Ahmed Main File for TMU MDM MRP, SUMMER 2023
# * Using computer vision and TTS to make 'Undertale' more accessible for players with visual impairments

import cv2
import time
import keyboard
import threading
import classes #importing classes of enemies from separate file
import tts #importing tts function to keep code clean
# from PIL import Image

#* HEY GENIUS, IF IT DOESN'T WORK: DID YOU REMEMBER TO FLIP THE VALUES? (Y,X), (B,G,R)

#TODO: if box == text box and checker = "none", check actions
#TODO: figure out fight sequence (detect one of the colours and then ping when bar in right location)
#TODO: 

#? Should I extract mp3 as separate file and play alongside videos? 


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

def checkAction():     #?can use pyautogui for screen pixel? quicker? /// probably for actual gameplay
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

def interactionType():
    if checkCol(frame[299, 344], "white") and checkCol(frame[299, 503], "white"):
        print("In Fight")
    else:
        print("Not Fighting")

capture = cv2.VideoCapture("froggit.mp4") #brings video to capture var

while True:
    ret, frame = capture.read() #assigns each frame of the video to "frame"
    
    if cv2.waitKey(0) & 0xFF==ord('q') or not ret: #check if q pressed or no more frames break
        break

    if keyboard.is_pressed("s"): #for saving frames for testing
        cv2.imwrite("saved2.png", frame)

    cv2.imshow("Frame", frame) #shows each frame under the window name "Frame"
    interactionType()
    checkAction()




capture.release()
cv2.destroyAllWindows()



#299, 344 < small box
# and 299, 503
#304, 141 < large box

#end fight func
    #checker = "none"


# frog = classes.Froggit()
# frog.attacks()

# def fightSelector():
#     if 