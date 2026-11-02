import base
import os
outputBasePath = '/Users/hamzamahmoud/final/contours_output'
file='/Users/hamzamahmoud/final/dogs/wolf_alph3.obj'
processThreeD=base.snapshotAndContour(file,flip=True)
contours,contoursData=processThreeD.snapshots()

foldername=input('enter folder name:')
savefolder=os.path.join(outputBasePath,foldername)
visualize=base.contourVisualizer()
for points,data in zip(contours,contoursData):
    saveName = f"{data['name']}_azimuth:{data['azimuth']:.2f}_elevation:{data['elevation']:.2f}_index:{data['camViewNum']}.png"
    visualize.drawPoints(points)
    visualize.savefig(saveName,savefolder)
print(f"Finished '{file}'. Contour plots saved to '{savefolder}'")
