this project is made to help in creating datasets to help with computer ML research using 3d objects to create contours of 3d objects at different angles using a geodesic dome vertices as the points of the camera. 
it uses multiple libraries:
pyvista and trimesh to load, add the dome over the objects and take snapshots of the objects,
json library to input data in to a data file,
matplotlib to draw the contours if needed, 
numpy to work with arrays and 
opencv to take the contours of the snapshots 

the process of creating the dataset 
will need two files one for the contour points and the other for contourdata to be created in advance it can be empty or has data in it. example files and files that already has data in it is contours.json and contourdata.json
contours.json is a (NxMx2) where n is the index of the contour and m would be the number of points around the contour for my uploaded data it will be 120 points 2 is the x and y coordinates of the points 
contourdata.json is a json file that stores the index of each contour, the azimuth and elevation and the file name

currently the contours are taken from  digital life 3d objects scan and SMAL datasets 
I do recommend to use obj files as I am not sure how the program will preform when given other types of files even though trimesh accepts multiple file formats 



     @inproceedings{Zuffi:CVPR:2017,
        title = {{3D} Menagerie: Modeling the {3D} Shape and Pose of Animals},
        author = {Zuffi, Silvia and Kanazawa, Angjoo and Jacobs, David and Black, Michael J.},
        booktitle = {IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)},
        month = jul,
        year = {2017},
        month_numeric = {7}
      }
