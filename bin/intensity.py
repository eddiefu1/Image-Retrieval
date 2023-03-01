# import the necessary packages
import cv2

# load the image, grab its spatial dimensions (width and height),
# and then display the original image to our screen
image = cv2.imread(r"C:\Users\eddie\csc664-term-project\public\images\imageObjects\A1_1.png")
(h, w) = image.shape[:2]
cv2.imshow("Original", image)
# images are arrays -- with the origin (0, 0) located at
# grabs the pixel values at the top left array at (0,0)
(b, g, r) = image[0, 0]
print("Pixel at (0, 0) - Red: {}, Green: {}, Blue: {}".format(r, g, b)) #where pixel located at (0,0) has the value 
# access the pixel located at x=50, y=20 and prints out the rgb value since it is image(y, x)
(b, g, r) = image[20, 50]
print("Pixel at (50, 20) - Red: {}, Green: {}, Blue: {}".format(r, g, b))
# update the pixel at (50, 20) and set it to red
image[20, 50] = (0, 0, 255)
(b, g, r) = image[20, 50]
print("Pixel at (50, 20) - Red: {}, Green: {}, Blue: {}".format(r, g, b))

cv2.waitKey(0)
 
