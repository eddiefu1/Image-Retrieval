import matplotlib.pyplot as plt
import cv2, os 
import numpy as np

def getLBPimage(input_image):

    ### Step 0: Step 0: Convert an image to grayscale
    input_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgLBP = np.zeros_like(input_image)
    neighbor = 3 #since it is a regular LBP operator it will be done on a 3x3 pixel
    for height in range(0,image.shape[0] - neighbor):
        for width in range(0,image.shape[1] - neighbor):
            ### Step 1: 3 by 3 pixel
            img          = input_image[height:height+neighbor,width:width+neighbor] ##compare with neighbor 
            center       = img[1,1] #center of the image, used for thresholding
            img01        = (img >= center)*1.0
            img01_vector = img01.T.flatten() #flattens the image
            # convert the image into 1s and 0s
            # it is ok to order counterclock manner
            #img01_vector = img01.flatten()
            ### Step 2: **Binary operation**:
            img01_vector = np.delete(img01_vector,4) #deletes if it is higher than threshold
            ### Step 3: Decimal: Convert the binary operated values to a digit.
            where_img01_vector = np.where(img01_vector)[0]
            if len(where_img01_vector) >= 1:
                num = np.sum(2**where_img01_vector)
            else:
                num = 0
            imgLBP[height +1, width+1] = num
    return(imgLBP)

dir_images = "indexed/" #declaring directory of images
imgs = os.listdir(dir_images) #reads into the directory
for imgnm in imgs:
    image = plt.imread(os.path.join(dir_images,imgnm))
    imgLBP= getLBPimage(image)
    vecimgLBP = imgLBP.flatten()

    fig = plt.figure(figsize=(20,8))
    ax  = fig.add_subplot(1,3,1)
    ax.imshow(image)
    ax.set_title("Inputted image")
    ax  = fig.add_subplot(1,3,2)
    ax.imshow(imgLBP,cmap="gray")
    
    ax.set_title("Converted image")
    ax  = fig.add_subplot(1,3,3)
    freq,lbp, _ = ax.hist(vecimgLBP,bins=2**8)
    ax.set_ylim(0,40000)
    lbp = lbp[:-1]
    ## print the LBP values when frequencies are high
    largeTF = freq > 5000
    for x, fr in zip(lbp[largeTF],freq[largeTF]):
        ax.text(x,fr, "{:6.0f}".format(x),color="magenta")
    ax.set_title("LBP histogram")
    plt.show()