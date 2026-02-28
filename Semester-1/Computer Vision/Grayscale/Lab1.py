import cv2
import numpy as np
from numpy import array

img = cv2.imread('bee.jpg')

b, g, r = cv2.split(img)
cv2.imshow('Blue Channel', b)
cv2.imshow('Green Channel', g)
cv2.imshow('Red Channel', r)
cv2.waitKey(0)

cv2.imshow('Original Image', img)
cv2.waitKey(0) 

#Write a function that converts an image to grayscale.
def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_img = convert_to_grayscale(img)
cv2.imshow('Grayscale Image', gray_img)
cv2.waitKey(0)