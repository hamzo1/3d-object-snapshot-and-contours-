import base
import os
import glob
outputBasePath = '/Users/hamzamahmoud/final/contours_output'
file='wolf_alph3.obj'
processThreeD=base.snapshotAndContour(file,flip=True)
snapshotdir=processThreeD.snapshots()

foldername=input('enter folder name:')
savefolder=os.path.join(outputBasePath,foldername)
imgfiles=sorted(glob.glob(os.path.join(snapshotdir,'*.png')))
if imgfiles:
    for imgpath in imgfiles:
        basename = os.path.splitext(os.path.basename(imgpath))[0]
        try:
            contour = processThreeD.drawPoints(imgpath)
            saveName = f'{basename}.png'
            processThreeD.savecontour(saveName, savefolder)
        except Exception as e:
            print(f'Error: {e}')
    print(f"Finished '{file}'. Contour plots saved to '{savefolder}'")
else:
    print("No snapshot images were found to process.")



