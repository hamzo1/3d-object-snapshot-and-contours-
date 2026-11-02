
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
from geodome import GeodesicDome



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
        facesPv = np.hstack([np.full((len(faces),1),3),faces]).ravel()
        pvObj=pv.PolyData(vertices,facesPv)
        return pvObj
    
    
    def loadobj(self,object,flip=False):# loads objects files 
        mesh=trimesh.load(object,force='mesh')
        obj=self.normalizeobj(mesh)
        if flip:
             rotaion=trimesh.transformations.rotation_matrix(np.pi,[0,0,1])
             obj.apply_transform(rotaion)

        return obj
    def Create_spehere(self):
        sphere=GeodesicDome(freq=3)
        vertices = np.array(sphere.get_vertices())#get vertcies 
        triangles = np.array(sphere.get_triangles())#get triangles 
        spheremesh = trimesh.Trimesh(vertices=vertices,faces=triangles,process=True)#makes the sphere as a mesh 
        spheremesh.apply_translation(-spheremesh.vertices.mean(axis=0))# applies the translation to be at point (0,0,0)
        return spheremesh
    
    def sliceSphere(self,sphere,groundY=0.0):
        planeOregin=np.array([0.0,groundY,0.0])
        planeNormal=np.array([0.0,1.0,0.0])
 
        dome=sphere.slice_plane(planeOregin,planeNormal,cap=False)
        dome.merge_vertices()#the slice repeats vertices along the cut which would make duplicate camera views
        return dome


    def getCenterMass(self, mesh):#gets center mass of object 
            vertices = np.asarray(mesh.vertices)
            faces = np.asarray(mesh.faces)
            tmesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            return tmesh.center_mass
    def scalObj(self, obj, dome, fraction=0.5):
        
        dome_diameter = dome.extents.max()
        target_length = dome_diameter * fraction
        scale_factor = target_length / obj.extents.max()
        obj.apply_scale(scale_factor)

    def PlaceOnGround(self,obj,groundLevel,sphereCenter,upaxis=1):
        centerMass = self.getCenterMass(obj)
        offSet= np.asarray(sphereCenter,dtype=float)-centerMass
        offSet[upaxis]= groundLevel - obj.bounds[0][upaxis]
        obj.apply_translation(offSet)
        
    
    
class threeDobject(parentsfunctions):
        def __init__(self,objName,flip=False):
            super().__init__()
            self.mesh=self.loadobj(objName,flip=flip)
            self.sphere= self.Create_spehere()
            self.dome=None
            self.obj=None
            self.addDomeOnObj()
           
        
        
        def addDomeOnObj(self):#added the dome over the object by normalizing them then moving the dome to the objects center mass
            sphereCenter= self.sphere.vertices.mean(axis=0)
            groundY= sphereCenter[1]
            self.dome= self.sliceSphere(self.sphere,groundY)
            self.scalObj(self.mesh,self.sphere)
            self.PlaceOnGround(self.mesh,groundY,sphereCenter)
            self.obj=self.convertToPyvista(self.mesh)
            
            
    

        


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
                 up=np.cross(right,forward)#the real up direction of the screen since the world up is not perpendicular to the view
                 relative = points- focal#measured from the focal point because that is the center of the image
                 x= np.dot(relative,right)
                 y=np.dot(relative,up)
                 width=np.abs(x).max()#half the width of the view needed since parallel_scale is half the image height
                 hieght=np.abs(y).max()
                 windowWidth,windowHieght=plotter.window_size
                 aspect = windowWidth/windowHieght
                 requiredScale=max(hieght,width/aspect)
                 requiredScale*=padding
                 plotter.camera.parallel_scale=requiredScale
            
            def getElevation(self,point,refCenter):
                 
                 relativePoint= np.asarray(point) - np.asarray(refCenter)
                 x,y,z=relativePoint[0],relativePoint[1],relativePoint[2]
                 groundDist=math.sqrt(x**2+z**2)
                 elevationRad=math.atan2(y,groundDist)
                 elevationDeg=math.degrees(elevationRad)
                 return elevationDeg

            def getAzimuth(self,point,refCenter):
                 
                 relativePoint= np.asarray(point) - np.asarray(refCenter)
                 x,z= relativePoint[0],relativePoint[2]
                 azimuthRad=math.atan2(z,x)
                 return  math.degrees(azimuthRad)
            
                
            def snapshots(self,lowerBound=0,upperBound=90):#reponsible for taking the snap shots of the object at the vertcies of the dome taking the contours using helper functions
                centerMass=self.getCenterMass(self.mesh)
                points=np.asarray(self.dome.vertices)
                domeBaseY= np.min(points[:,1])
                domeCenterRef = np.array([centerMass[0],domeBaseY,centerMass[2]])
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
                
                
                contours=[]
                contoursData=[]
                print('taking contours....')
                for i ,point in enumerate(points):
                    elevation=self.getElevation(point,domeCenterRef)
                    
                    if not (lowerBound <= elevation <= upperBound):
                            continue 
                        
                    campos=np.asarray(point)
                    plotter.camera.position = campos
                    plotter.camera.focal_point = centerMass

                    forward = centerMass - campos
                    forward /= np.linalg.norm(forward)

                    if abs(np.dot(forward, [0, 1, 0])) > 0.98:
                        up = np.array([0, 0, 1])
                    else:
                        up = np.array([0, 1, 0])

                    plotter.camera.up = up
                    
                    
                    azimuth=self.getAzimuth(point,domeCenterRef)
                    self.fitObjToCamera(plotter,self.obj)
                    filename = f"snapshots/{self.objname}_azimuth:{azimuth:.2f}_elevation:{elevation:.2f}_index:{i}.png"

                    plotter.show(
                            screenshot=filename,
                            auto_close=False
                        )

                    
                    contour=self.takecontour(filename)
                    ContourCenterMass=self.get2dCenterMass(contour)
                    startidx=self.findStartingPoint(contour,ContourCenterMass)
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


class contourVisualizer:
    def __init__(self):
        pass 
    def drawPoints(self,points):#draws the points in a gradinat color green-blue-red green = start and red = end 

        plt.clf()
        n=len(points)
        colors=np.linspace(0,1,n)

        bright_gbr = LinearSegmentedColormap.from_list('bright_gbr',['lime', 'blue', 'red'])
        plt.figure(figsize=(14, 10))

        plt.scatter(points[:,0],points[:,1],c=colors,cmap=bright_gbr,s=10)
        plt.gca().invert_yaxis()
        plt.axis('off')
        plt.axis('equal')
    def savefig(self,fileName,folder='savedcontour' ):#saves the matplot lib figure 
         
        os.makedirs(folder,exist_ok=True)
        filePath=os.path.join(folder,fileName)
        plt.savefig(filePath,bbox_inches='tight')
        plt.close()
                              
            

           
           
                            
                      
                      



                           
                      
                 


     
                    



                        