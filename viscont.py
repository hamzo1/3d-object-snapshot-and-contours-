from base import contourVisualizer as vis

import json 
import numpy as np 
# the perpous of this file is to loop through the  contour data file and cam data and save it as the img of the contour

basename='contourimg'
visualize=vis()#create an instance of the class

with open('camData.json','r') as file:
    camData = json.load(file)['camData']# load json data

with open('contourData.json','r') as file:
    contourData = json.load(file)['contoursPts']#load json data 

nameCount={}# this keeps track of the of the contour we are drawing key is the name of contour and the value is the number of contours we drew

for data in camData:#loop through cam data to get the information we need for the index of the file 
    
    name= data['name']#get name of the contour
    if name not in nameCount:#check if we seen that name before else add it to the dictionary 
        nameCount[name]=0
   
    if nameCount[name] >= 3:#check how many drawings we have of the contour 
        continue
    index = data['index']# get the index of the contour 

    points=np.array(contourData[index])#create an array of points inthe contour 
    visualize.drawPoints(points)#draws the points 
    
    filename = f"{basename}_{name}_{nameCount[name]}.png"# name of the file 
    visualize.savefig(filename)#saves the file 
    nameCount[name]+=1# updates the dictionary

