import pyttsx3
# from gtts import gTTs
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

engine = pyttsx3.init() 

engine.setProperty("volume", 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def read(img):
    return pytesseract.image_to_string(img)

# print(read("text.png"))
# print(read("vege.png"))
# speak(read("vege.png"))
# speak(read("text.png"))