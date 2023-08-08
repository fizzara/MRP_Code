
#* Fizza Ahmed Main File for TMU MDM MRP, SUMMER 2023
# * Using computer vision and TTS to make 'Undertale' more accessible for players with visual impairments

#libraries
import cv2
import time
import keyboard
import threading
start = time.time()
#python files
import classes #importing classes of enemies from separate file
import tts #importing tts function to keep code clean
import findCheck
from PIL import Image

#* HEY GENIUS, IF IT DOESN'T WORK: DID YOU REMEMBER TO FLIP THE VALUES? (Y,X), (B,G,R)

#TODO: if box == text box and checker = "none", check actions
#TODO: figure out fight sequence (detect one of the colours and then ping when bar in right location)
#TODO: 

#? Should I extract mp3 as separate file and play alongside videos? 


capture = cv2.VideoCapture("froggit.mp4") #brings video to capture var
ct = 0
while True:
    ct = ct + 1
    ret, frame = capture.read() #assigns each frame of the video to "frame"
    
    if cv2.waitKey(30) & 0xFF==ord('q') or not ret: #check if q pressed or no more frames break
        break

    if keyboard.is_pressed("s"): #for saving frames for testing
        cv2.imwrite("talking.png", frame)
        print(ct)

    
    
    if not findCheck.interactionType(frame):
        findCheck.checkAction(frame)
        findCheck.fightTalk(frame)

    cv2.imshow("Frame", frame) #shows each frame under the window name "Frame"
    # findCheck.interactionType(frame)
    




capture.release()
cv2.destroyAllWindows()
print(time.time()-start)



#299, 344 < small box
# and 299, 503
#304, 141 < large box

#end fight func
    #checker = "none"


# frog = classes.Froggit()
# frog.attacks()

# def fightSelector():
#     if 