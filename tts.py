import pyttsx3
from playsound import playsound
import os
from gtts import gTTS
import time

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# engine = pyttsx3.init() 

# engine.setProperty("volume", 1.0)

def speak(text, filename="output.mp3"):
    if filename[-4:] != ".mp3": #so i don't have to add .mp3 to the end of every file
        filename = filename + ".mp3"
    
    # try: #in case the file  doesnt exist, to prevent errors
    #     os.remove(filename) #in case the file exists, to prevent errors
    # except:
    #     pass

    if not os.path.isfile(filename): #check if file doesnt exist to save time and errors
        audio = gTTS(text) #convert text parameter to audio
        audio.save(filename) #save converted audio
    else: #if the file does exist, delete it and write a new one
        os.remove(filename)
        audio = gTTS(text)
        audio.save(filename)
    # time.sleep(0.1)
    playsound(filename)

    
    
    # engine.say(text)
    # engine.runAndWait()
    
def read(img):
    text = pytesseract.image_to_string((img), lang="eng.undertale")
    if text[0] == "*":
        text = text[1:]
    return text


# speak(read("text.png"))

# speak("test")
# speak("test again")
# print(read("text.png"))
# print(read("vege.png"))
# speak(read("vege.png"))
# speak(read("text.png"))


