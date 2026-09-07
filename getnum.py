import json 
import numpy as np 

contourdata= 'contourData.json'

with open(contourdata, 'r') as file:
    data= json.load(file)
contourPoints=data.get('contoursPts',[])

array=np.array(contourPoints)
print(array.shape)
print(len(array))
count=[]
for i in range(len(array)):
    count.append(i)
print(count[-1])

