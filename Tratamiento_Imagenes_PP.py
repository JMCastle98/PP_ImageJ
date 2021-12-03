import cv2
import numpy as np
import skimage
from skimage import color
import pandas as pd

img = cv2.imread('C:/Users/JMCas/Downloads/dust_promete004.tif',cv2.IMREAD_GRAYSCALE)

cropped = img[0:1920]
cropped2 = cropped.copy()
pixels_to_um = 0.454


ret1, thresh = cv2.threshold(cropped, 40 , 255, cv2.THRESH_BINARY)


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)) 

opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)



im_floodfill = opening.copy()

h,w = opening.shape[:2]
mask = np.zeros((h+2,w+2), np.uint8)

cv2.floodFill(im_floodfill, mask, (0,0), 255)

im_floodfill_inv = cv2.bitwise_not(im_floodfill)

im_out = opening | im_floodfill_inv




sure_bg = cv2.dilate(im_out ,kernel,iterations=2)

dist_transform = cv2.distanceTransform(im_out ,cv2.DIST_L2,3)

ret2, sure_fg = cv2.threshold(dist_transform,0.15*dist_transform.max(),255,0)
sure_fg = np.uint8(sure_fg)

unknown = cv2.subtract(sure_bg,sure_fg)

ret3, markers = cv2.connectedComponents(sure_fg)

markers = markers+1

markers[unknown==255] = 0

img1 = cv2.cvtColor(cropped, cv2.COLOR_GRAY2BGR)

markers = cv2.watershed(img1,markers)

img1[markers == -1]  = [0,255,233]

img2 = color.label2rgb(markers, colors = ['white'],  bg_label=1)


img3 = cv2.cvtColor(cropped, cv2.COLOR_GRAY2BGR)


cv_image = skimage.img_as_ubyte(img2)


buffer = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2GRAY)

ret, m2 = cv2.threshold(buffer, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

contours, hierarchy = cv2.findContours(m2,cv2.RETR_TREE,  cv2.CHAIN_APPROX_NONE)    

big_contours = [c for c in contours if cv2.contourArea(c) >= 1000]


############################


        
        
sorted_contours= sorted(big_contours , key=cv2.contourArea, reverse= True)


for c in big_contours :
    cv2.drawContours(img3, c, -1, (255,255,255), 3) 



area = []
perimeter = []
aspect_ratio = []
solidity = []
major = []
minor = []


for i,c in enumerate(sorted_contours): 
    
    #### añador resto de parametros del archivo de Pintor
    x,y,w,h = cv2.boundingRect(c)
    aspect_ratio.append(float((w)/h))
    area.append(cv2.contourArea(c))
    perimeter.append(cv2.arcLength(c,True))
    area1=cv2.contourArea(c)
    hull=cv2.convexHull(c)
    hull_area=cv2.contourArea(hull)
    solidity.append(float((area1)/hull_area))
    (a1, a2),(d1,d2),angle=cv2.fitEllipse(c)
    long=a1-d2
    small=a2-d2
    major.append(abs(long/2))
    minor.append(abs(small/2))
    
    M= cv2.moments(c)
    cx= int(M['m10']/M['m00'])
    cy= int(M['m01']/M['m00'])
    x,y,w,h= cv2.boundingRect(c)
    cv2.putText(img3, text= str(i+1), org=(cx-10,cy-30),
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color= (0,0,255),
            thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(cropped2, text= str(i+1), org=(cx-10,cy-30),
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color= (255 ,255,255),
            thickness=2, lineType=cv2.LINE_AA)
    
    
    
#### aqui se van a poner en forma de dataframe
data = { "areas" : area ,
         "perimetros": perimeter,
         "aspect_ratio": aspect_ratio,
         "solidity": solidity
        }


archivo = pd.DataFrame(data) 

archivo.index +=1

#Aqui se guarda
archivo.to_csv("Particulas.csv", index = True)




##################################


for i in range(0,len(big_contours)):
    rect = cv2.minAreaRect(big_contours [i])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    img_result = cv2.drawContours(cropped2,[box],0,(255,0,255),2)



cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 1400, 1200)


cv2.imshow('img', cropped)
cv2.waitKey(0)

cv2.imshow('img', thresh)
cv2.waitKey(0)
   
cv2.imshow('img', opening)
cv2.waitKey(0)

cv2.imshow('img', im_out)
cv2.waitKey(0)

cv2.imshow('img', img1)
cv2.waitKey(0)

cv2.imshow('img', m2)
cv2.waitKey(0)

cv2.imshow('img', img3)
cv2.waitKey(0)

cv2.imshow('img', cropped2)
cv2.waitKey(0)



cv2.destroyAllWindows()





