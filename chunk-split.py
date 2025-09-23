from PIL import Image
import os
import requests
import io
scriptDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptDir)
Image.MAX_IMAGE_PIXELS=None
def splitImage(fn):
    fullImage=Image.open(fn)
    segs=fn.split(".")
    folderName=segs[0]
    os.mkdir(folderName)
    segs2=segs[0].split("-")
    imageKey=segs2[0] #region specifier, e.g. pretoria
    timeStamp=int(segs2[1])
    tileX0=int(segs2[2]) #upper left tile x
    tileY0=int(segs2[3]) #upper left tile y
    imageSize=fullImage.size
    xDim=imageSize[0]//1000
    yDim=imageSize[1]//1000
    for xi in range(xDim):
        for yi in range(yDim):
            newImage=fullImage.crop(box=(xi*1000,yi*1000,(xi+1)*1000,(yi+1)*1000))
            tileX1=tileX0+xi #current tile x
            tileY1=tileY0+yi #current tile y
            ofn="{tx}-{ty}.png".format(tx=tileX1,ty=tileY1)
            newImage.save(folderName+"/"+ofn)
from tlapse import download #submodule can change
imageList=download.image_list
def getFileNameFromLink(link):
    return link.split("/")[-1]
def getImage(link,prefix="images/"):
    fn=getFileNameFromLink(link)
    contents=requests.get(link).content
    bytes=io.BytesIO(contents)
    im=Image.open(bytes)
    im.save(prefix+fn)
    fileSize=os.path.getsize(prefix+fn)
    return fileSize
totalFileSize=0
counter=0
for entry in imageList:
    fn=getFileNameFromLink(entry[1])
    dirName="images/"+fn.split(".")[0]
    if os.path.exists(dirName):
        continue
    totalFileSize+=getImage(entry[1])
    splitImage("images/"+fn)
    counter+=1
    print("processed {n} files, {mb} megabytes in total.".format(n=counter,mb=totalFileSize/1048576))
    if totalFileSize > 201326592:
        print("192MB size reached, exiting...")
        break
