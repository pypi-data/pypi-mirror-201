import pyFaceTrace as ft
import cv2
from PIL import ImageFont
ft.downloadImageSamples()
'''
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
'''