import base
import os

basepath='/Users/hamzamahmoud/final/3dObjects'
camfile='camData.json'
contourfile='contourData.json'
flipFolders=['big_cats','cows','dogs','horses','hippos']# objects in these folders are inverted so they get flipped before taking the snapshots

for folder,subfolders,files in os.walk(basepath):#goes through 3dObjects and all the folders in it
    flip=os.path.basename(folder) in flipFolders
    for file in sorted(files):
        if file.endswith('.obj'):
            filePath=os.path.join(folder,file)
            print(filePath,'flip:',flip)
            processThreeD=base.snapshotAndContour(filePath,flip)
            contourdata,camdata= processThreeD.snapshots(0,85)#takes the snapshots at elevations between 0 and 85
            processThreeD.saveJson(camfile,contourfile,camdata,contourdata)#saves the contour points and camera data in the json files
            print(contourdata.shape)
print('success')
