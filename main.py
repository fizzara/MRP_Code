import cv2
import keyboard
import classes #importing classes of enemies from separate file


capture = cv2.VideoCapture("froggit.mp4") #brings video to capture var

while True:
    ret, frame = capture.read() #assigns each frame of the video to "frame"
    
    if cv2.waitKey(2) & 0xFF==ord('q') or not ret: #check if q pressed or no more frames break
        break

    cv2.imshow("Frame", frame) #shows each frame under the window name "Frame"
    

capture.release()
cv2.destroyAllWindows()


frog = classes.Froggit()
frog.attacks()