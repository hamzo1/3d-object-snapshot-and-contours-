import base
import os 

basepath='/Users/hamzamahmoud/final/horses'
camfile='camData.json'
contourfile='contourData.json'
for file in os.listdir(basepath):
    if file.endswith('.obj'):
        filePath=os.path.join(basepath,file)
        processThreeD=base.snapshotAndContour(filePath,True)# there is an extra prameter thst flips the 3d objects if the object is inverted 
        contourdata,camdata= processThreeD.snapshots(0,85)#this takes the camera takes the snapshots at elevatiobns between 0 and 85 the defualt is 0-90
        processThreeD.saveJson(camfile,contourfile,camdata,contourdata)#takes the input file names and saves the contour points and camera data in these file camfile is for cam data na dcontourfile is for contour data 
        print(contourdata.shape)
print('success')
