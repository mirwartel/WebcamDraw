import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
frameCounter = 0

myColors = [[100, 120, 118, 179, 255, 255], [63, 79, 109, 87, 255, 213]]

myColorValues = [[255, 50, 25],
                 [75, 255, 25]]  # bgr

myPoints = []  # [x, y, colorId]


def drawOnCanvas(imgResults, myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResults, (point[0], point[1]), 5, myColorValues[point[2]], cv2.FILLED)


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 250:
            # cv2.drawContours(imgResults, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            aprox = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            x, y, w, h = cv2.boundingRect(aprox)

    return x + w // 2, y


def findColor(imgResults,img, myColors, myColorValues):
    count = 0
    newPoints = []
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResults, (x, y), 7, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1

        # cv2.imshow(str(color[0]), mask)
    return newPoints


def draw():
    while True:
        success, img = cap.read()

        imgResults = img.copy()

        newPoints = findColor(imgResults, img, myColors, myColorValues)

        if len(newPoints) != 0:
            for newP in newPoints:
                myPoints.append(newP)
        if len(newPoints) != 0:
            drawOnCanvas(imgResults, myPoints, myColorValues)

        cv2.imshow("Drawing", imgResults)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quiting application")
            break

    cap.release()
    cv2.destroyAllWindows()


draw()

# while True:
#     success, img = cap.read()
#
#     imgResults = img.copy()
#
#     newPoints = findColor(img, myColors, myColorValues)
#
#     if len(newPoints)!=0:
#         for newP in newPoints:
#             myPoints.append(newP)
#     if len(newPoints)!=0:
#         drawOnCanvas(myPoints, myColorValues)
#
#
#
#
#     cv2.imshow("Drawing", imgResults)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         print("Quiting application")
#         break
#
# cap.release()
# cv2.destroyAllWindows()
