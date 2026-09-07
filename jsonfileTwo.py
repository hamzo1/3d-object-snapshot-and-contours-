import base
import os 

basepath='/Users/hamzamahmoud/final/big_cats'
camfile='camData.json'
contourfile='contourData.json'
for file in os.listdir(basepath):
    if file.endswith('.obj'):
        filePath=os.path.join(basepath,file)
        processThreeD=base.snapshotAndContour(filePath,True)#added the true value here just because of the objects i was working with was inverted so i added a function that flips it upon loading the object
        contourdata,camdata= processThreeD.snapshots()
        processThreeD.saveJson(camfile,contourfile,camdata,contourdata)
        print(contourdata.shape)
print('success')
