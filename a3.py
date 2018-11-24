import time
def compareOne(template,searchImage,x1,y1):
  totalDiff=0
  for i in range(x1,x1+getWidth(template)):
    for j in range(y1,y1+getHeight(template)):
      searchP=getPixel(searchImage,i,j)
      tempP=getPixel(template,i-x1,j-y1)
      diffLum=abs(getRed(searchP)-getRed(tempP))
      totalDiff+=diffLum
  return totalDiff

def find2Dmin(matrix):
  min=1000000000000
  minCol=0
  minRow=0
  for i in range(len(matrix)):
    for j in range(len(matrix[0])):
      if matrix[i][j]<min:
        min=matrix[i][j]
        minCol=j
        minRow=i
  min=[minCol,minRow,min]
  return min
  
def compareAll(template,searchImage):
  matrix=[[(compareOne(template,searchImage,x,y))for x in range(getWidth(searchImage)-getWidth(template))] for y in range(getHeight(searchImage)-getHeight(template))]
  return matrix
  
def compareFast(template,searchImage):
  min=[0,0,100000]
  for i in range(0,getWidth(searchImage)-getWidth(template),3):
    for j in range(0, getHeight(searchImage)-getHeight(template),3):
      lumDiff=0
      for x in range(i,i+getWidth(template)):
        if x%(getWidth(template)/2)==0:
          for y in range(j,j+getHeight(template)):
            if y%(getHeight(template)/3)==0:
              tempP=getPixel(template,x-i,y-j)
              searchP=getPixel(searchImage,x,y)
              diff=abs(getRed(tempP)-getRed(searchP))
              lumDiff+=diff
        if lumDiff>min[2]:
          break          
      if lumDiff<min[2]:
        min[0]=i
        min[1]=j
        min[2]=lumDiff
  return min

def grayScale(picture):
  pix=getPixels(picture)
  for p in pix:
    lum=(getRed(p)+getGreen(p)+getBlue(p))/3
    setColor(p,makeColor(lum,lum,lum))
  return picture
  
def displayMatch(picture,x1,y1,w,h,color):
  pix=getPixels(picture)
  for i in range(x1-3,x1+w):
    for j in range(y1-3,y1+h):
      if(i<x1 or i>=x1+w-3):
        setColor(getPixel(picture,i,j),color)
      if(j<y1 or j>=y1+h-3):
        setColor(getPixel(picture,i,j),color)
  return picture
  
def findWaldo(targetJPG,searchJPG):
  template=grayScale(targetJPG)
  searchImage=grayScale(searchJPG)
  min=find2Dmin(compareAll(template,searchImage))
  show(displayMatch(searchImage,min[0],min[1],getWidth(template),getHeight(template),red))
  
def findWaldoFast(targetJPG,searchJPG):
  startTime=time.time()
  template=grayScale(targetJPG)
  searchImage=grayScale(searchJPG)
  min=compareFast(template,searchImage)
  show(displayMatch(searchImage,min[0],min[1],getWidth(template),getHeight(template),red))
  print "findWaldoFast - Elapsed Time: "+ str((time.time()-startTime)/60)
  