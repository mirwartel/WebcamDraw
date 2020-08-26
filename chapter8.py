import cv2
import numpy as np

def getContours(img):
    contours,hierarchy= cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)

        if area > 5:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            aprox = cv2.approxPolyDP(cnt,0.02*peri,True)
            print(len(aprox))
            objCor = len(aprox)
            x, y, w, h = cv2.boundingRect(aprox)

            if objCor == 3: objectType = "tri"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.90 and aspRatio < 1.1: objectType="square"
                else:objectType="rectangle"
            elif objCor >4: objectType="circle"
            else:objectType="None"

            cv2.rectangle(imgContour,(x,y), (x+w, y+h),(0,255,0),2)
            cv2.putText(imgContour, objectType,
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),2)

path = 'resources/shapes.jpg'

img = cv2.imread(path)
imgContour = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)
getContours(imgCanny)


cv2.imshow("Grey Blur", imgBlur)
cv2.imshow("Grey Blur canny", imgCanny)
cv2.imshow("g", imgContour)
cv2.waitKey(0)