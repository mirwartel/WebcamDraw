import cv2
import numpy as np

img = cv2.imread("resources/hare.jpg")


imgHor = np.hstack((img, img))
imgVer = np.vstack((img,img))

cv2.imshow("horizontal", imgHor)
cv2.imshow("vertical", imgVer)
cv2.waitKey(0)