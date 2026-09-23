import base
import os 

basepath='/Users/hamzamahmoud/final/3dObjects'
camfile='camData.json'
contourfile='contourData.json'
for file in os.listdir(basepath):
    if file.endswith('.obj'):
        filePath=os.path.join(basepath,file)
        processThreeD=base.snapshotAndContour(filePath)# there is an extra prameter thst flips the 3d objects if the object is inverted 
        contourdata,camdata= processThreeD.snapshots(0,85)# added a prameter that takes in the elevation you want to capture if you take it out the defult will be 0-90
        processThreeD.saveJson(camfile,contourfile,camdata,contourdata)#sames the data in to the json file 
        print(contourdata.shape)
print('success')
