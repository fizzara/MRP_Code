import cv2
import keyboard
import classes #importing classes of enemies from separate file
from PIL import Image
import tts

#HEY GENIUS, IF IT DOESN'T WORK: DID YOU REMEMBER TO FLIP THE VALUES? (Y,X), (B,G,R)

#  y, x
#453, 173 = fight
#452, 327 = act
#446, 541 = item
#447, 641 = mercy

checker = "none"

def checkYellow(arr):  #used to check if the pixel's BGR value is similar to the yellow we're looking for, meaning it is selected
    if arr[0] < 30 and arr[1] > 245 and arr[2] > 250: 
        return True
    return False

def checkAction(): #can use pyautogui for screen pixel? quicker? 
    if checkYellow(frame[453, 173]) and checker != "fight":
        tts.speak("fight")
        checker = "fight"
    if checkYellow(frame[452, 327]) and checker != "act":
        tts.speak("act")
        checker = "act"
    if checkYellow(frame[446, 541]) and checker != "item":
        tts.speak("item")
        checker = "item"
    if checkYellow(frame[447, 641]) and checker != "mercy":
        tts.speak("mercy")
        checker = "mercy"



capture = cv2.VideoCapture("froggit.mp4") #brings video to capture var

while True:
    ret, frame = capture.read() #assigns each frame of the video to "frame"
    
    if cv2.waitKey(20) & 0xFF==ord('q') or not ret: #check if q pressed or no more frames break
        break

    cv2.imshow("Frame", frame) #shows each frame under the window name "Frame"
    # hold = frame[328, 455]
    checkAction()




capture.release()
cv2.destroyAllWindows()


# frog = classes.Froggit()
# frog.attacks()

# def fightSelector():
#     if 