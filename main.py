
#* Fizza Ahmed Main File for TMU MDM MRP, SUMMER 2023
# * Using computer vision and TTS to make 'Undertale' more accessible for players with visual impairments

#libraries
import cv2
import keyboard
import numpy as np
#python files
import tts #importing tts function to keep code clean
import findCheck
from PIL import Image

#* HEY GENIUS, IF IT DOESN'T WORK: DID YOU REMEMBER TO FLIP THE VALUES? (Y,X), (B,G,R)


player_status = True #False when in the world, True when in a fight

#*the following is to allow the player to choose their demo video
chosen = False
while not chosen:
    chosenNum = int(input("Please select your choice of demo: \n 1: Game Introduction \n 2: Conversation \n 3: Dummy Fight \n 4: Froggit Fight \n"))
    match chosenNum:
        case 1:
            capture = cv2.VideoCapture("videos/flowey-save.mp4")
            chosen = True
        case 2:
            capture = cv2.VideoCapture("videos/toriel_intro.mp4")
            chosen = True
        case 3:
            capture = cv2.VideoCapture("videos/dummy.mp4")
            chosen = True
        case 4:
            capture = cv2.VideoCapture("videos/froggit1.mp4")
            chosen = True
            

frameNum = 0

# run = True

while True:
    
    ret, frame = capture.read() #assigns each frame of the video to "frame"
    
    if cv2.waitKey(15) & 0xFF==ord('q') or not ret: #check if q pressed or no more frames break
        break


    
    if frameNum % 10==0:
        h, w, _ = frame.shape
        crop = frame[int(h*0.615625):(int(h*0.615625)+34), int(w*0.05):(int(w*0.05)+101)] 
        template = cv2.imread("playername.png")
        # cv2.imshow("t", template)
        # cv2.waitKey(0)
        # cv2.imshow("c", crop)
        # cv2.waitKey(0)
        match = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(match >= 0.9)
        matches = list(zip(*matches[::-1]))
        if matches: #check if crop is identical to template
            player_status = False #if player isnt moving/is in a fight
        else:
            player_status = True #if player is moving

    
    

    if keyboard.is_pressed("s"): #for saving frames for testing
        cv2.imwrite("tester.png", frame)



    if player_status:
        if frameNum %15 == 0:
            findCheck.asterisk(frame)
    
    if not player_status:
        findCheck.checkAction(frame)
        if findCheck.interactionType(frame):
            findCheck.run = True
            cv2.rectangle(frame, (int(w*0.3734375), int(h*0.525)), (int(w*0.6234375), int(h*0.80625)), 255, 5)
            crop2 = frame[(int(h*0.525)):(int(h*0.80625)), (int(w*0.3734375)):(int(w*0.6234375))] 
            templ = cv2.imread("undertaleHeart.png")
            match2 = cv2.matchTemplate(crop2, templ, cv2.TM_CCOEFF_NORMED)
            _, _, _, maxLoc = cv2.minMaxLoc(match2)
            crop2 = frame[int(h*0.525):int(h*0.80625), int(w*0.3734375):(int(w*0.6234375))] 
            cv2.rectangle(crop2, (maxLoc[0]-10, maxLoc[1]-10), (maxLoc[0]+templ.shape[1]+10, maxLoc[1]+templ.shape[0]+10), (0, 0, 255), 1)
        if not findCheck.interactionType(frame):
            if findCheck.checkCol(frame[int(h*0.6666666667), int(w*0.09375)], "green"):
                if findCheck.checkCol(frame[int(h*0.6666666667), int(w*0.4046875)], "white"):
                    print("attack now")

        # crop2 = np.asarray(crop2)
        # templ = cv2.imread("undertaleHeart.png")
        # match2 = cv2.matchTemplate(crop2, templ, cv2.TM_CCOEFF_NORMED)
        # match2 = np.where(match2 >= 0.6)
        # match2 = list(zip(*match2[::-1]))
        # print(match2)
        # cv2.imshow("c", crop2)
        if frameNum % 10==0 and not findCheck.interactionType(frame):
            findCheck.fightList(frame)

    frameNum += 1
    cv2.imshow("Frame", frame) #shows each frame under the window name "Frame"
    


capture.release()
cv2.destroyAllWindows()
