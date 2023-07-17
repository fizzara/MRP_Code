import cv2
import numpy as np


def findHeart(image, template="undertaleHeart.png"):
    img = cv2.imread(image)
    template = cv2.imread(template)
    height, width, _ = template.shape

    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)
    _, _, minL, _ = cv2.minMaxLoc(result)
    #!minL = x, y

    botR = (minL[0] + height, minL[1] + width)
    #!botR = x, y

    # cv2.rectangle(img2, minL, botR, 255, 2)
    # cv2.imshow("match.png", img2)
    # cv2.waitKey(0)
    print(minL, botR)

    cropped = img[minL[1]:botR[1], minL[0]:botR[0]]
    cv2.imshow("match", cropped)
    cv2.waitKey(0)

def heartText(image, template="undertaleHeart.png"):
    #* If in Act or Mercy
    img = cv2.imread(image)
    template = cv2.imread(template)
    height, width, _ = template.shape

    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)
    _, _, minL, _ = cv2.minMaxLoc(result)
    minL = (minL[0] + width, minL[1])

    crop = img[minL[1]:minL[1]+height+10, minL[0]:minL[0]+215]
    cv2.imshow("text", crop)
    cv2.waitKey(0)

heartText("saved2.png")


