import base
import os

basepath='/Users/hamzamahmoud/final/3dObjects'
count=0
for file in os.listdir(basepath):
    if file.endswith('.obj'):
        filePath=os.path.join(basepath,file)
        count+=1
