
import pyvista as pv #to take the snapshots of the object  
import trimesh # to add the dome over the object and load the obj 
import numpy as np#to work with vertcies and 
import os#used for going though files and creating files 
import cv2 as cv#used for taking contours of the 2d snapshot img
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt# used for ploting the contour
from matplotlib.colors import LinearSegmentedColormap
import math#using it for doing math like finding azimuth and elevation 
import json#using it for adding files to json 



class parentsfunctions:
    def __init__(self):
        pass
    def normalizeobj(self,mesh):#makes the mean = 0 and standard diviation = 1 
        getPoints=np.asarray(mesh.vertices)

        getMean=np.mean(getPoints,axis=0)

        center= getPoints - getMean
        

        distance=np.linalg.norm(center,axis=1)
        stdDist=np.std(distance)

        normlize = center / stdDist
        mesh.vertices=normlize
        return mesh
    def convertToPyvista(self,obj):#converts trimesh object to pyvista to take snap shot 
        vertices = np.asarray(obj.vertices)
        faces= np.asarray(obj.faces)
        facesPv = np.hstack([np.full((len(faces),1),3),faces])
        pvObj=pv.PolyData(vertices,facesPv)
        return pvObj
    
    def centerDomeWithobj(self,obj):# centers the dome with the object
        dome=trimesh.load('flexDOme.obj')
        dome=self.normalizeobj(dome)
        centerMass=obj.center_mass
        dome.apply_translation(centerMass)
        self.scalObj(obj,dome)
        return dome
    
    def loadobj(self,object,flip=False):# loads objects files 
        mesh=trimesh.load(object,force='mesh')
        obj=self.normalizeobj(mesh)
        if flip:
             rotaion=trimesh.transformations.rotation_matrix(np.pi,[0,0,1])
             obj.apply_transform(rotaion)

        dome=self.centerDomeWithobj(obj)
        objPv=self.convertToPyvista(obj)
        return objPv,dome

    def getCenterMass(self, mesh):#gets center mass of object 
            vertices = np.asarray(mesh.vertices)
            faces = np.asarray(mesh.triangles)
            tmesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            return tmesh.center_mass
    def scalObj(self,obj,dome):#the function that scales the objects to be 2x the size of the dome
            dome_diameter = dome.extents[0] 

        # 2. Get the current length of your object (Z-axis extent)
            current_obj_length = obj.extents[2] 

        # 3. Calculate your target length (2x smaller than the dome's diameter)
            target_obj_length = dome_diameter / 2.0

        # 4. Calculate the scale multiplier
            scale_factor = target_obj_length / current_obj_length
            obj.apply_scale(scale_factor)
    
         

         

        
    
class threeDobject(parentsfunctions):
        def __init__(self,objName,flip=False):
            super().__init__()
            self.obj,self.dome=self.loadobj(objName,flip=flip)
           
        
        
        def addDomeOnObj(self,obj,dome):#added the dome over the object by normalizing them then moving the dome to the objects center mass
            self.normalizeobj(self.obj)
            self.normalizeobj(self.dome)
            centerMass=self.getCenterMass(self.obj)
            self.dome.translate(centerMass,relative=False)
        


        def getMeshVert(self,obj):#gets the vertcies of the mesh 
                return np.asarray(obj.vertices)
        def getDomeVert(self,dome):#gets the dome vertcies 
                return np.asarray(dome.vertices)


class snapshotAndContour(threeDobject):#resposible for taking the snap shots and contour of the object 
            def __init__(self,objname,flip=False):
                super().__init__(objname,flip=flip)
                self.objname=os.path.splitext(os.path.basename(objname))[0]
            def fitObjToCamera(self,plotter,obj,padding=1.10):#this a method way to fit the object in the camera without changing the object vertcies and the coordinates 
                 points= np.asarray(obj.points)
                 cameraPos=np.asarray(plotter.camera.position)
                 focal=np.asarray(plotter.camera.focal_point)
                 forward=focal - cameraPos
                 forward/=np.linalg.norm(forward)
                 up =np.asarray(plotter.camera.up)
                 up/=np.linalg.norm(up)
                 right = np.cross(forward,up)
                 right/=np.linalg.norm(right)
                 relative = points- cameraPos
                 x= relative @ right
                 y=relative @ up
                 width=x.max()-x.min()
                 hieght=y.max()-y.min()
                 windowWidth,windowHieght=plotter.window_size
                 aspect = windowWidth/windowHieght
                 requiredScale=max(hieght,width/aspect)
                 requiredScale*=padding
                 plotter.camera.parallel_scale=requiredScale
            
            def getElevation(self,point,center):
                 relativePoint= np.asarray(point) - np.asarray(center)
                 x,y,z=relativePoint[0],relativePoint[1],relativePoint[2]
                 groundDist=math.sqrt(x**2+y**2)
                 elevationRad=math.atan2(z,groundDist)
                 elevationDeg=math.degrees(elevationRad)
                 return elevationDeg

            def getAzimuth(self,point,center):
                 relativePoint= np.asarray(point) - np.asarray(center)
                 x,y= relativePoint[0],relativePoint[1]
                 azimuthRad=math.atan2(y,x)
                 return  math.degrees(azimuthRad)
            def getMaxMinElevation(self,points,center):
                 pointsInDegree=[]
                 for point in points:
                      pointsInDegree.append(self.getElevation(point,center))
                      
                 return np.max(pointsInDegree),np.min(pointsInDegree)
                
            def snapshots(self):#reponsible for taking the snap shots of the object at the vertcies of the dome taking the contours using helper functions
                center=np.asarray(self.obj.center_of_mass())
                os.makedirs('snapshots',exist_ok=True)
                print('processing object')
                plotter = pv.Plotter(
                off_screen=True,
                window_size=(800, 600)
            )

                plotter.add_mesh(
                self.obj,
                color="lightgray",
                lighting=False,
                show_edges=False
            )
                
                plotter.camera.enable_parallel_projection()
                points=np.asarray(self.dome.vertices)
                
                maxElevation,minElevation=self.getMaxMinElevation(points,center)
                request=input(f'enter 1 if you would like to add boundries for the camaera max elevation:{maxElevation:.2f} and min elevation {minElevation:.2f} and 0 if your would like to take all snap shots: ')
                
                useboundries = (request =='1')
                if useboundries:
                     minElvation=float(input('eneter the minimum elevatiion in degrees: '))
                     maxElvation= float(input('eneter the maximmum elevation in degrees: '))

                contours=[]
                contoursData=[]
                print('taking contours....')
                for i ,point in enumerate(points):
                    elevation=self.getElevation(point,center)
                    if useboundries:
                         if not (minElvation <= elevation <= maxElvation):
                              continue 
                        
                    campos=np.asarray(point)
                    plotter.camera.position = campos
                    plotter.camera.focal_point = center

                    forward = center - campos
                    forward /= np.linalg.norm(forward)

                    if abs(np.dot(forward, [0, 1, 0])) > 0.98:
                        up = np.array([0, 0, 1])
                    else:
                        up = np.array([0, 1, 0])

                    plotter.camera.up = up
                    
                    
                    azimuth=self.getAzimuth(point,center)
                    self.fitObjToCamera(plotter,self.obj)
                    filename = f"snapshots/{self.objname}_azimuth:{azimuth:.2f}_elevation:{elevation:.2f}_index:{i}.png"

                    plotter.show(
                            screenshot=filename,
                            auto_close=False
                        )

                    
                    contour=self.takecontour(filename)
                    centerMass=self.get2dCenterMass(contour)
                    startidx=self.findStartingPoint(contour,centerMass)
                    newcontour=self.equalSpacedPoints(contour,startidx)
                    newcontour=self.normalizepts(newcontour)
                    contours.append(newcontour)
                    contoursData.append({'camViewNum':i,'name':self.objname,'azimuth':azimuth,'elevation':elevation})
                           
                    os.remove(filename)
                contours=np.stack(contours)
                        
                plotter.close()
                return contours,contoursData
            

            def takecontour(self,img):#responsibel for taking the contour of the objects 

                img = cv.imread(img, cv.IMREAD_GRAYSCALE)

                img = cv.bitwise_not(img)

                _, thresh = cv.threshold(
                    img,
                    0,
                    255,
                    cv.THRESH_BINARY
                )

                kernel = np.ones((3, 3), np.uint8)

                contours, _ = cv.findContours(
                    thresh,
                    cv.RETR_EXTERNAL,
                    cv.CHAIN_APPROX_NONE
                )
                contours = max(contours, key=cv.contourArea)

                

                return contours
            def get2dCenterMass(self,contours):#reposible for getting the img center mass 
                 
                 M=cv.moments(contours)
                 if M['m00'] ==0:
                      return [0,0]
                 cx=int(round(M['m10']/M['m00']))
                 cy=int(round(M['m01']/M['m00']))
                 centerMass=[cx,cy]
                 return centerMass
            def findStartingPoint(self,contours,centerMass):#reposible for finding the starting point of where to draw the points and which is the lowest point the y axis intresect the contour if not it looks for the highest point 
                 cx,cy=centerMass
                 pts=contours.reshape(-1,2)
                 xDist=np.abs(pts[:,0]-cx)
                 onCenterLine = np.where(xDist == np.min(xDist))[0]
                 belowcenter=onCenterLine[pts[onCenterLine,1]>=cy]
                
                 if len(belowcenter) > 0:
                      bestindx=belowcenter[np.argmax(np.abs(pts[belowcenter,1]))]
                      

                      return bestindx
                 abovecenter=onCenterLine[pts[onCenterLine,1]<cy]
                 if len(abovecenter) > 0:
                      bestindx=abovecenter[np.argmax(np.abs(pts[abovecenter,1]))]
                      
                      
                      return bestindx
            def equalSpacedPoints(self,contour,startingpoint,numPoints=120):#resposible for creating 120 equally spaced points 
                points=contour.reshape(-1,2)
                points=np.roll(points,-startingpoint,axis=0)
                
                points = np.concatenate((points[:1], points[:0:-1]))

                points=np.vstack([points,points[0]])

                diff= np.diff(points,axis =0)

                length=np.hypot(diff[:,0],diff[:,1])

                segementlength=np.linalg.norm(diff,axis=1)

                cumluativeDist=np.concatenate([[0],np.cumsum(segementlength)])

                totalLength=cumluativeDist[-1]

                targetDist=np.linspace(0,totalLength,numPoints,endpoint=False)

                newX=np.interp(targetDist,cumluativeDist,points[:,0])

                newY=np.interp(targetDist,cumluativeDist,points[:,1])
                newpoints=np.column_stack([newX,newY])

                return newpoints
            
            def normalizepts(self,points):#normalizes the points by the minimum to equal to zero and the standard divaition to equal to 1

                pts=points.reshape(-1,2)

                ptsToZero=pts-np.min(pts,axis=0)

                dist=np.linalg.norm(ptsToZero,axis=1)

                stdDev=np.std(dist)
                if stdDev == 0: 
                     return ptsToZero
                else:

                    ptsScalled=ptsToZero/stdDev

                    return ptsScalled 
            
            def drawPoints(self,imgPath):#draws the points in a gradinat color green-blue-red green = start and red = end 

                contour = self.takecontour(imgPath)
                
                centerMass = self.get2dCenterMass(contour)

                startingIndex = self.findStartingPoint(
                        contour,
                        centerMass
                    )
                
                newcontour=self.equalSpacedPoints(contour,startingIndex)
                newcontour=self.normalizepts(newcontour)
                plt.clf()
                n=len(newcontour)
                colors=np.linspace(0,1,n)

                bright_gbr = LinearSegmentedColormap.from_list(
                    'bright_gbr',
                    ['lime', 'blue', 'red']
                )
                plt.figure(figsize=(14, 10))

                plt.scatter(newcontour[:,0],newcontour[:,1],c=colors,cmap=bright_gbr,s=10)
                plt.gca().invert_yaxis()
                plt.axis('off')
                plt.axis('equal')
                return 
            def saveJson(self,camDatafile,contourfile,camdata,contourdata):
                if not os.path.exists(camDatafile) or os.path.getsize(camDatafile) ==0: 
                    with open (camDatafile,'w') as f:
                        json.dump({'camData':[]},f)
                if not os.path.exists(contourfile) or os.path.getsize(contourfile)==0: 
                    with open (contourfile,'w') as f:
                        json.dump({'contoursPts':[]},f)
              
                with open(camDatafile,'r') as file:
                   camData=json.load(file)
                with open (contourfile,'r') as file:
                   contourData=json.load(file)
                startidx=len(camData['camData'])
                for i,item in enumerate(camdata):
                   item['index']=startidx +i

                camData['camData'].extend(camdata)
                
                contourData['contoursPts'].extend(contourdata.tolist())

                with open(camDatafile,'w') as file:
                   json.dump(camData,file,indent=2)
                with open (contourfile,'w') as file:
                   json.dump(contourData,file,indent=2)

            def savefig(self,fileName,folder ):#saves the matplot lib figure 
         
                os.makedirs(folder,exist_ok=True)
                filePath=os.path.join(folder,fileName)
                plt.savefig(filePath,bbox_inches='tight')
                plt.close()
            
                      
            

           
           
                            
                      
                      



                           
                      
                 


     
                    



                        