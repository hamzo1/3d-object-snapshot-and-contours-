import base
import os 

basepath='/Users/hamzamahmoud/final/3dObjects'
camfile='camData.json'
contourfile='contourData.json'
for file in os.listdir(basepath):
    if file.endswith('.obj'):
        filePath=os.path.join(basepath,file)
        processThreeD=base.snapshotAndContour(filePath,True)
        contourdata,camdata= processThreeD.snapshots()
        processThreeD.saveJson(camfile,contourfile,camdata,contourdata)
        print(contourdata.shape)
print('success')
