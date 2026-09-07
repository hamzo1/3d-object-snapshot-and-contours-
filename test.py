import base
import os

inputbasePath='/Users/hamzamahmoud/final/3dObjects'# the base path for your file 
for file in os.listdir(inputbasePath):#loop through the folder 
    if file.endswith('.obj'):#check if the file is an obj file 
        fullPath=os.path.join(inputbasePath,file)#get the full path to your object 
        print(f'processing {file}')
        processThreeD=base.snapshotAndContour(fullPath,False)#intialize the variable 
        processThreeD.snapshots()#take the snapshot 
if 'processThreeD' in locals():
    print('exporting files in to json')
    processThreeD.saveJson('fullcontourDataSet.json')
    print('done ')

