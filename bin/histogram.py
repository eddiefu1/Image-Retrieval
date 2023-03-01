import matplotlib.pyplot as plt
import cv2, os 
import numpy as np
dir_images = "indexed/"
imgs = os.listdir(dir_images)

fig = plt.figure(figsize=(20,14))
for count, imgnm in enumerate(imgs,1):
    image = plt.imread(os.path.join(dir_images,imgnm))
    ax = fig.add_subplot(2,len(imgs),count)
    ax.imshow(image)
    ax.set_title(imgnm)
plt.show()

