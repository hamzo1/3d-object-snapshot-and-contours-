import json 
import numpy as np 

contourdata= 'contourData.json'

with open(contourdata, 'r') as file:
    data= json.load(file)
contourPoints=data.get('contoursPts',[])

array=np.array(contourPoints)
print(array.shape)