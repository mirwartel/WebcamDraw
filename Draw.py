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

def selectColor( myColors, myColorValues):

    cv2.namedWindow("My colors")
    cv2.resizeWindow("My colors", 300, 100)
    cv2.createTrackbar("Color Num", "My colors", 0, int(len(myColors))-1, empty)
    switch = '0:OFF, 1:ON'
    cv2.createTrackbar(switch, "My colors", 0, 1, empty)


    while True:

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


        s = cv2.getTrackbarPos(switch, "My colors")
        colorTrackbar = cv2.getTrackbarPos('Color Num', 'My colors')


        if s == 1:

            selectedColor = myColors[colorTrackbar]

            print(selectedColor)
            cv2.destroyWindow("My colors")


            colorFilter(selectedColor[0], selectedColor[3], selectedColor[1],
                        selectedColor[4], selectedColor[2], selectedColor[5], colorTrackbar)
            break
    cv2.destroyWindow("My colors")


def empty(a):
      pass


def brushColor(color):
    image = np.zeros((512, 512, 3), np.uint8)
    cv2.namedWindow("Brush color")
    cv2.createTrackbar('Blue', "Brush color", myColorValues[color][0], 255, empty)
    cv2.createTrackbar('Green', "Brush color", myColorValues[color][1], 255,empty)
    cv2.createTrackbar('Red', "Brush color", myColorValues[color][2], 255, empty)

    while True:
        cv2.imshow("Brush color", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        blue = cv2.getTrackbarPos('Blue', "Brush color")
        green = cv2.getTrackbarPos('Green', "Brush color")
        red = cv2.getTrackbarPos('Red', "Brush color")
        image[:] = [blue, green, red]
        print(blue, green, red)
    cv2.destroyWindow("Brush color")



def colorFilter(HueMin, HueMax, SatMin, Satmax, ValMin, ValMax, color):


    cv2.namedWindow("HSV")
    cv2.resizeWindow("HSV", 640, 240)
    cv2.createTrackbar("HUE Min", "HSV", HueMin, 179, empty)
    cv2.createTrackbar("HUE Max", "HSV", HueMax, 179, empty)
    cv2.createTrackbar("SAT Min", "HSV", SatMin, 255, empty)
    cv2.createTrackbar("SAT Max", "HSV", Satmax, 255, empty)
    cv2.createTrackbar("VALUE Min", "HSV", ValMin, 255, empty)
    cv2.createTrackbar("VALUE Max", "HSV", ValMax, 255, empty)

    switch = '1:Apply'
    cv2.createTrackbar(switch, "HSV", 0, 1, empty)

    while True:

        success, img = cap.read()
        imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos("HUE Min", "HSV")
        h_max = cv2.getTrackbarPos("HUE Max", "HSV")
        s_min = cv2.getTrackbarPos("SAT Min", "HSV")
        s_max = cv2.getTrackbarPos("SAT Max", "HSV")
        v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
        v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
        s = cv2.getTrackbarPos(switch, "HSV")

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(imgHsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)

        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        hStack = np.hstack([img, mask, result])
        cv2.imshow('Horizontal Stacking', hStack)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if s == 1:
            myColors[color] = [h_min,s_min,v_min,h_max,s_max,v_max]
            break

    cv2.destroyWindow("HSV")
    cv2.destroyWindow("Horizontal Stacking")









def draw():
    switch = '1:Modify My colors'

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

        s = cv2.getTrackbarPos(switch, "Drawing")
        if s == 1:

            cv2.destroyWindow("Drawing")


            selectColor(myColors,myColorValues)
        cv2.createTrackbar(switch, "Drawing", 0, 1, empty)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quiting application")
            break
    cap.release()
    cv2.destroyAllWindows()


brushColor(0)

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