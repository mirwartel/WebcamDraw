import cv2
import numpy as np

img = cv2.imread("resources/bejd.jpg")
kernel = np.ones((5, 5), np.uint8)

imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGrey, (7,7), 0)
imgCanny = cv2.Canny(img, 150, 200)
imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
imgEroded = cv2.erode(imgDialation, kernel, iterations=1)
cv2.imshow("gray image", imgGrey)
cv2.imshow("blured gray image", imgBlur)
cv2.imshow("canny gray image", imgCanny)
cv2.imshow("dialated gray image", imgDialation)
cv2.imshow("eroded gray image", imgEroded)

cv2.waitKey(0)