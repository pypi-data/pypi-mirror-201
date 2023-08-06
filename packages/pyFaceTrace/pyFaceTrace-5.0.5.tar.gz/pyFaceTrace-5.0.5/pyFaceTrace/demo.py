import pyFaceTrace as ft
import cv2
from PIL import ImageFont
#至train資料夾載入樣本,欲辨識之目標圖片可放入 train資料夾
ft.loadDB()
#設定文字物件
FONT = ImageFont.truetype("kaiu.ttf",50,index=0)
#webcamd 影像處理迴圈
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    ret, img = cap.read()
    if not ret : continue
    #取得 img 中所有人臉之矩型區域，放入rects
    rects=ft.detector(img,1)
    for rect in rects:
        #取得webcam img 中人臉之特徵向量
        fv=ft.getFeatureVector(img,rect)
        #將特徵向量和 ft.DB 中之人特徵向量做比對，找到距離最短的(dist)當作辨識結果(tag)
        tag,dist = ft.predictFromDB(fv)
        #將辨識結果顯示在 img 上
        cv2.rectangle(img,(rect.left(),rect.top()),(rect.right(),rect.bottom()),(0,0,255),3)
        img=ft.addText2Img_cv2(img,tag,FONT,position=(rect.left(),rect.top()-FONT.size-1))
    if cv2.waitKey(10) == 27: break
    # 將 img show在視窗中
    cv2.imshow('press esc to exit...', img)
cap.release()
cv2.destroyAllWindows()
