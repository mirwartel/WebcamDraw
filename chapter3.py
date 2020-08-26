import cv2
import numpy as np

img = cv2.imread("resources/bejd.jpg")
print(img.shape)

imgResize = cv2.resize(img, (300, 200))

print(imgResize.shape)

imgCropped = img[0:200, 200:500]

cv2.imshow("image", img)
#cv2.imshow("Resized image", imgResize)
cv2.imshow("Cropped image", imgCropped)

cv2.waitKey(0)

