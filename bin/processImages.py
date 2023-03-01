#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 12:24:05 2022

@author: cristobalpadilla
"""
import sys
import os
import json
from base64 import b64decode
import cv2
import numpy as np
import matplotlib.pyplot as plt


def getLBPimage(image):
   ### Step 0: Step 0: Convert an image to grayscale
   input_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   imgLBP = np.zeros_like(input_image)
   neighbor = 3 #since it is a regular LBP operator it will be done on a 3x3 pixel
   for height in range(0, image.shape[0] - neighbor):
       for width in range(0, image.shape[1] - neighbor):
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
   return (imgLBP)

def extractObjects(imgDir, maskDir):
    objectsDir = '../public/images/imageObjects'

    images = get_image_paths(imgDir)
    masks = get_image_paths(maskDir)

    for image in images:
        file = os.path.basename(image)
        filename, extension = os.path.splitext(file)

        if extension == '.png':
            maskAddr = os.path.join(maskDir, filename + '_mask' + extension)

            img_full = cv2.imread(image)
            img = cv2.cvtColor(img_full, cv2.COLOR_BGR2GRAY)
            mask = cv2.imread(maskAddr, 0)

            res = cv2.bitwise_and(img, img, mask=mask)
            edges = cv2.Canny(res, 10, 250)

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
            closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

            (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                cv2.drawContours(img,[approx], -1, (0, 255, 0), 2)

            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            i = 0
            while i < len(cnts):
                x, y, width, height = cv2.boundingRect(cnts[i])
                roi = img_full[y:y+height, x:x+width]
                cv2.imwrite(os.path.join(objectsDir, filename + '_' + str(i) + extension), roi)
                i += 1

def generateJSONData(imagesDir):
    parentImgDir = '../public/images/indexed'
    images = get_image_paths(imagesDir)
    result = []

    for image in images:
        file = os.path.basename(image)
        filename, extension = os.path.splitext(file)

        if extension == '.png':
            img =  cv2.imread(image)
            img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_LBP = getLBPimage(img)

            grayscale_vector = get_vector(img_grayscale)
            LBP_vector = get_vector(img_LBP)
            img_feature = np.concatenate((grayscale_vector, LBP_vector))

            parentImgPath = os.path.join(parentImgDir, filename[:2] + extension)

            result.append({
                'id': filename,
                'image_path': image,
                'parent_path': parentImgPath,
                'feature': img_feature.tolist()
            })

    json_object = json.dumps(result, indent=4)

    with open('data.json', 'w') as outfile:
        outfile.write(json_object)

    return result

def cropObject(image):
    maskDir = '../public/images/binary'
    uploadObjectsDir = '../public/images/uploads'
    imageObjectsDir = '../public/images/imageObjects'
    imgObjectPaths = []

    file = os.path.basename(image)
    filename, extension = os.path.splitext(file)
    maskPath = os.path.join(maskDir, filename[-2:] + '_mask' + extension)
    uploadObjPath = os.path.join(uploadObjectsDir, filename)
    os.makedirs(uploadObjPath)

    img_full = cv2.imread(image)
    img = cv2.cvtColor(img_full, cv2.COLOR_BGR2GRAY)
    mask = cv2.imread(maskPath, 0)

    res = cv2.bitwise_and(img, img, mask=mask)
    edges = cv2.Canny(res, 10, 250)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        cv2.drawContours(img,[approx], -1, (0, 255, 0), 2)

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    i = 0
    while i < len(cnts):
        x, y, width, height = cv2.boundingRect(cnts[i])
        roi = img_full[y:y+height, x:x+width]
        roi_path = os.path.join(imageObjectsDir, filename[-2:] + '_' + str(i) + extension)
        roi_id = filename[-2:] + '_' + str(i)
        imgObjectPaths.append(
            {   "id": roi_id,
                "image_path": roi_path
            })
        cv2.imwrite(roi_path, roi)
        i += 1

    return imgObjectPaths

def get_image_paths(imagesDir):
    images = []

    for filename in os.listdir(imagesDir):
        imgPath = os.path.join(imagesDir, filename)
        images.append(imgPath)

    return images

def get_vector(image, bins=256):
    grayScale = cv2.calcHist([image], [0], None, [bins], [0, 256])
    vector = grayScale.reshape(-1)
    return vector

def search(img, images, k=5):
    histDir = "../public/images/histograms"
    grayDir = "../public/images/grayscale"

    results = []
    inputImg_reg = cv2.imread(img)
    inputImg = cv2.cvtColor(inputImg_reg, cv2.COLOR_BGR2GRAY)
    inputImgVector = get_vector(inputImg)

    for image in images:
        file = os.path.basename(image)
        filename, extension = os.path.splitext(file)

        if extension == ".png":
            img_reg = cv2.imread(image)
            img = cv2.cvtColor(img_reg, cv2.COLOR_BGR2GRAY)
            img_vector = get_vector(img)
            dist = float(cosine(inputImgVector, img_vector))
            hist_name = filename + "_hist" + extension
            hist_path = os.path.join(histDir, hist_name)
            gray_name = filename + "_gray" + extension
            gray_path = os.path.join(grayDir, gray_name)
            results.append({
                "image_path": image,
                "hist": hist_path,
                "gray": gray_path,
                "dist": dist})

    results.sort(key=lambda x: x['dist'], reverse=True)
    return results[:k]

def make_hist(images):
    histDir = "../public/images/histograms"

    for image in images:
        file = os.path.basename(image)
        filename, extension = os.path.splitext(file)

        if extension == '.png':
            img_reg = plt.imread(image)
            img = getLBPimage(img_reg)
            img_vector = img.flatten()
            freq,lbp, hist = plt.hist(img_vector,bins=2**8)
            plt.ylim(0, 40000)
            lbp = lbp[:-1]
            largeTF = freq > 5000
            for x, fr in zip(lbp[largeTF],freq[largeTF]):
                plt.text(x,fr, "{:6.0f}".format(x),color="magenta")
            plt.title("LBP Histogram")
            hist_name = filename + "_hist" + extension
            plt.savefig(os.path.join(histDir, hist_name))
            plt.clf()

def histogramIntersection(a, b):
    return np.sum(np.minimum(a,b))/np.sum(b)

def make_gray(images):
    grayDir = "../public/images/grayscale"

    for image in images:
        file = os.path.basename(image)
        filename, extension = os.path.splitext(file)

        if extension == '.png':
            img_reg = plt.imread(image)
            img = getLBPimage(img_reg)
            plt.imshow(img, cmap="gray")
            hist_name = filename + "_gray" + extension
            plt.savefig(os.path.join(grayDir, hist_name))
            plt.clf()

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def main():

    inputImagePath = sys.argv[1];
    imagesDir = sys.argv[2];
    method = sys.argv[3];
    images = get_image_paths(imagesDir)


    '''
    # Make histogram images. Only run this if no histogram
    # images have been generated before (i.e., histograms folder is empty)
    #make_hist(images)

    # Make LBP gray scale image. Only run this if no gray scale images
    # have been generated before (i.e., grayscale folder is empty)
    #make_gray(images)

    # Search images
    results = search(inputImagePath, images)
    response = { "data": results }

    # Extract objects from images and generate data.JSON
    extractObjects('../public/images/indexed', '../public/images/binary')
    generateJSONData('../public/images/imageObjects')
    '''

    # Extract objects from images and generate data.JSON
    results = cropObject(inputImagePath)
    response = { "data": results }

    # Send results to node.
    print(json.dumps(response))

    sys.stdout.flush()
    return 0
    
if __name__ == "__main__":
    main()