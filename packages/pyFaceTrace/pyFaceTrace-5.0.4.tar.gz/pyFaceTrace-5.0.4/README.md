# Author:KuoYuan Li
[![N|Solid](https://images2.imgbox.com/8f/03/gv0QnOdH_o.png)](https://sites.google.com/ms2.ccsh.tn.edu.tw/pclearn0915)  
本程式簡單地結合dlib,opencv  
讓不懂機器學習的朋友可以軟簡單地操作人臉辨識,  
程式需另外安裝 dlib  
搜尋關鍵字：whl dlib cp***  ***代表python版本 ex:cp310代表 python 3.10  
dlib whl 安裝包下載網站: (https://github.com/datamagic2020/Install-dlib)
  - 本套工具主要針對windows使用者設計，相依之 package 及相容性問題需自行排除  
  - dlib whl 安裝包下載後必需由檔案離線安裝 pip install ...
  - opencv whl  下載點:請下載合適的opencv版本<br>
    (https://pypi.tuna.tsinghua.edu.cn/simple/opencv-contrib-python/)  
  
※PS:  
2022/11/24 使用 python3.10 搭配  
  dlib-19.22.99-cp310-cp310-win_amd64.whl  試用成功  
  
2023/4/2  
  調整函式，適配 colab  
    (https://colab.research.google.com/drive/1ou7nWLQGl8uYLR_jUDyush9-D8ToTe8P?usp=sharing)  
  移除不常用之影像檔處理函式  
  新增直接和 opencv 協作模式  

	
	
##### Download the samples to 'train' folder(下載各種照片樣本至train資料夾)
```
import pyFaceTrace as ft  
ft.downloadImageSamples()  
```
##### work with opencv webcam process (detail)  
```
import pyFaceTrace as ft
import cv2
from PIL import ImageFont
ft.loadDB()
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    ret, img = cap.read()
    FONT = ImageFont.truetype("kaiu.ttf",50,index=0)
    rect=ft.detector(img,1)[0]
    fv=ft.getFeatureVector(img,rect)
    tag,dist = ft.predictFromDB(fv)
    cv2.rectangle(img,(rect.left(),rect.top()),(rect.right(),rect.bottom()),(0,0,255),3)
    img=ft.addText2Img_cv2(img,tag,FONT,position=(rect.left(),rect.top()-FONT.size-1))
    if cv2.waitKey(10) == 27: break
    cv2.imshow('press esc to exit...', img)
cap.release()
cv2.destroyAllWindows()
```
##### work with opencv webcam process (esay)
```
import pyFaceTrace as ft
import cv2
ft.loadDB()
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while(True):    
    ret, img = cap.read()
    if not ret:continue
    #img=cv2.flip(img,1)
    tags,dists,rects,img = ft.predictImage(img)            
    cv2.imshow('press esc to exit...', img)
    if cv2.waitKey(10) == 27: break
    
cap.release()
cv2.destroyAllWindows()
```
### Demo with webcam
```
import pyFaceTrace as ft
ft.loadDB(folder='train')
ft.predictCam()
```
##### 比對目前webcam擷取到的人臉和指定影像檔案並計算它們之間的距離
```
import pyFaceTrace as ft  
im = ft.captureImageFromCam()
VTest = ft.getFeatureVector(im)
Vtrain = ft.loadFeatureFromPic('train\\李國源.jpg')
D=ft.dist(VTest,Vtrain)
print('距離=',D)
```
##### 載入train資料夾中所有jpg檔之特徵及tag並直接預測目前webcam擷取到的人臉對應的TAG 
```
import pyFaceTrace as ft
ft.loadDB(folder='train')
im = ft.captureImageFromCam()
VTest = ft.getFeatureVector(im)
result = ft.predictFromDB(VTest)
print(result)
```



License
----

MIT
