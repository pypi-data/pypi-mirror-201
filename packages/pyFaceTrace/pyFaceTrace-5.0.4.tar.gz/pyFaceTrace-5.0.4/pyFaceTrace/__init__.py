#!/usr/bin/env python
# coding: utf-8
import sys,dlib
import numpy as np
#pip install scikit-image
from skimage import io
import cv2
import os
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from os.path import dirname
import requests
import bz2#bz2file pypi
import zipfile

def loadDBFromFeatureFiles(folder):
    files = os.listdir(folder)
    with open(folder+"\\" + "IDs.txt",encoding='utf8') as ff:
        IDs = ff.readlines()
    for ID in IDs:
        print("load "+ ID.strip() +".npy")
        DB[ID.strip()]=np.load(folder+"\\"+ID.strip()+'.npy')
            
            
def saveDB(folder):
    _createFolder(folder)
    for key in DB.keys():
        np.save(folder+"\\"+key.strip(),DB[key.strip()])
    with open(folder+'\\'+'IDs.txt','w',encoding='utf8') as fkey:        
        for key in DB.keys():
            fkey.write(key.strip()+"\n")        
        
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = _get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    _save_response_content(response, destination)    
def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None
def _save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
#==============================
def download_url_response(path,url):
    r = requests.get(url, stream = True)
    with open(path, 'wb') as f:
        i=0
        for ch in r:
            if i%1024==0:print('.',end='')
            f.write(ch);i+=1
    
def _bz2Decode(filepath):
    zipfile = bz2.BZ2File(filepath) # open the file
    data = zipfile.read() # get the decompressed data
    newfilepath = filepath[:-4] # assuming the filepath ends with .bz2
    open(newfilepath, 'wb').write(data) # write a uncompressed file
def downloadImageSamples(folder='train'):
    '''
    downloadImageSamples(folder='train')
    download sample images to 'folder'
    '''
    #vedio==> https://drive.google.com/file/d/1076Ftdz8hxZkly-7QxYUR6kRJHSft-7s/view?usp=sharing
    #images==> https://drive.google.com/file/d/1zmpZY5D5vNwcxhNmTgBprisevixexA4I/view
    #          new image
    #          https://drive.google.com/file/d/11FI4IqsbC-_QWz8qnuO7bRBW4LjSckDF/view?usp=sharing
    file_id = '11FI4IqsbC-_QWz8qnuO7bRBW4LjSckDF'
    destination = 'train.zip'
    download_file_from_google_drive(file_id, destination)
    with zipfile.ZipFile(destination, mode='r') as myzip:
        for file in myzip.namelist():
            print("extract "+file)
            myzip.extract(file,folder)
    os.remove(destination)
    
def downloadFileInNeed(filename):
    '''
    downloadFileInNeed(filename)
    dowload file from dlib web site:
    http://dlib.net/files
    filename: for example ==>"shape_predictor_68_face_landmarks.dat"
    '''
    if os.path.isfile(filename):return
    print("載入"+filename+"...可能需要一點時間") 
    if filename.find('.ttf')>=0:
        download_url_response("kaiu.ttf","http://sf1.loxa.edu.tw/104736/Download/kaiu.ttf")
    else:
        url="http://dlib.net/files/"+filename+".bz2"
        download_url_response(filename+".bz2",url)
        _bz2Decode(filename+".bz2")
        os.remove(filename+".bz2")
        print("ok")
        
downloadFileInNeed("shape_predictor_68_face_landmarks.dat")  
downloadFileInNeed("dlib_face_recognition_resnet_model_v1.dat")
downloadFileInNeed("kaiu.ttf")

Package_Dir = dirname(__file__)
#載入字型
_FONT = ImageFont.truetype("kaiu.ttf",20,index=0)
# 載入人臉檢測器
detector = dlib.get_frontal_face_detector()
# 載入人臉特徵點檢測器
_sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# 載入人臉辨識檢測器
_facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
#dlib_face_recognition_resnet_model_v1.dat  has to download by user
DB={}

def _createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' +  directory)
        
#一張圖片中，取rect區域當作人臉得到特徵向量   
def getFeatureVector(img,rect=None):
    '''
    getFeatureVector(img,rect=None)
    get Fecture vector(rank=128) from img according to rect
    '''
    if not rect:
        try:
            rect=detector(img, 1)[0] #如果沒有傳入rect取第一個檢測到的臉區域
        except:return []
    shape = _sp(img,rect) #找出特徵點位置
    #由圖片中特徵點位置(shape)擷取出特徵向量(128維特徵向量)
    face_descriptor = _facerec.compute_face_descriptor(img, shape)
    # 轉換numpy array格式
    return np.array(face_descriptor)     

def getFaceRects(img):
    try:
        return detector(img, 1)
    except:return []
    

def loadDB(db=DB,folder='train',isClearDB=True):
    '''
    loadDB(db=DB,folder='train')
    db:dictionary of key feature vectors
    DB is a default dictionary object for db
    default folder should be "train"
    the files should be like:
    John.jpg
    KY.jpg
    Marry.jpg
    ...
    
    the file name would be the TAG name
    '''
    if isClearDB:db.clear()
    for f in os.listdir(folder):
        path = f"{folder}/{f}"
        if os.path.isfile(path):
            img=io.imread(path)#cv2.imread(path)==>opencv的這個函式在windows裡面讀中文檔名有問題
            FV = getFeatureVector(img)
            if len(FV)>0:
                db[f[:f.rfind('.')]]=getFeatureVector(img)
                print(f+" feature loaded")
            else:print(f+" fail to detect face!!")

def predictFromDB(VTest,db=DB):
    '''
        predictFromDB(VTest,db=DB)
        Get the correspondent class which is most similar with VTest
        db:list of models (default=DB)
    '''
    minD = sys.float_info.max
    minK=''
    for k in db:
        dist=np.linalg.norm(VTest-db[k])
        if dist<minD:
            minK=k
            minD=dist
    return minK,minD


def dist(V1,V2):
    '''
    dist(V1,V2)
    return distance between V1,V2
    V1,V2:np.array
    '''
    return np.linalg.norm(V1-V2)

def addText2Img_cv2(img_cv2,text,font=_FONT,position=(20,20),fill=(255,0,0)):
    '''
    addText2Img_cv2(img_cv2,text,font=_FONT,position=(20,20),fill=(255,0,0))
    add text to imaget
    img_cv2:target image
    text:target text
    '''
    img_PIL = Image.fromarray(cv2.cvtColor(img_cv2,cv2.COLOR_BGR2RGB))#cv2.COLOR_BGR2RGB cv2.COLOR_RGB2BGR
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, text, font=font, fill=fill)
    ret = cv2.cvtColor(np.asarray(img_PIL),cv2.COLOR_RGB2BGR)# 转换回OpenCV格式
    img_PIL.close()
    return ret

def captureImageFromCam(camSerial=None):
    '''
    captureImageFromCam(camSerial=None)
    return cv2 image capture from webcam
    '''
    ret = None
    cap = None
    if not camSerial:
        for i in range(5):#assume there are less than 5 webcam attached to the platform
            cap = cv2.VideoCapture(i,cv2.CAP_DSHOW)
            if cap.isOpened():break
    else: cap = cv2.VideoCapture(camSerial,cv2.CAP_DSHOW)
    if not cap:return None
    
    # 載入人臉檢測器
    while(True):
        if cap.isOpened():
            ret, frame = cap.read()
            ret = frame
            break
    cap.release()
    return ret

#由webcam擷取訓練影像 and save          
def captureImageFromCamAndSave(tag,folder="train",camSerial=None):
    '''
    captureImageFromCamAndSave(tag,folder="train",camSerial=None)
    capture picture from camera and save it as:
    folder/tag.jpg
    return cv2 image
    '''
    ret = None
    cap = None
    if not camSerial:
        for i in range(5):#assume there are less than 5 webcam attached to the platform
            cap = cv2.VideoCapture(i,cv2.CAP_DSHOW)
            if cap.isOpened():break
    else: cap = cv2.VideoCapture(camSerial,cv2.CAP_DSHOW)
    if not cap:return None
    
    cv2.startWindowThread()
    # 載入人臉檢測器
    text="press p to take picture"
    # 先建立照片存放之資料夾(預設為train)
    _createFolder(folder)

    while(True):
        if cap.isOpened():
            ret, frame = cap.read()
            # 顯示圖片
            if ret: 
                try:
                    rect=detector(frame, 1)[0] #取第一個檢測到的臉區域# IndexError
                    if cv2.waitKey(1) & 0xFF == ord('p'):
                        im=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        
                        io.imsave(folder+"\\"+tag+".jpg",im)
                        text=" pictures saved..."
                        ret = frame
                        break
                    cv2.rectangle(frame,(rect.left(),rect.top()),(rect.right(),rect.bottom()),(255,0,0),3)
                    cv2.putText(frame, text,(rect.left()-80, rect.top()-20), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 2, cv2.LINE_AA)    
                    frame=addText2Img_cv2(frame,'tag='+tag,_FONT,(rect.left(), rect.top()-_FONT.size*2-5))   
                #except:pass 
                except IndexError:pass
                cv2.imshow('press esc to exit', frame)
            #若按下 esc 鍵則離開迴圈
            if cv2.waitKey(1) == 27: break
    cap.release()
    cv2.destroyAllWindows()
    return ret

def predictImage(frame,db=DB,showResult=True):
    '''
    predictImage(frame,db=DB,showResult=True)
    '''
    rects=detector(frame, 1)
    Tags = [];dists = []
    for rect in rects:
        try:
            V=getFeatureVector(frame,rect)
            Tag,dist=predictFromDB(V,db) # predict the target Tag
            Tags.append(Tag);dists.append(dist);rects.append(rect)
            if showResult:
                cv2.rectangle(frame,(rect.left(),rect.top()),(rect.right(),rect.bottom()),(255,0,0),3)
                #cv2.putText(frame, Tag+":"+str(dist),, cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 2, cv2.LINE_AA)
                text=Tag+":"+str(dist)
                frame=addText2Img_cv2(frame,Tag+":"+str(round(dist,3)),_FONT,(rect.left(), rect.top()-_FONT.size-1))
        except IndexError:pass
    return Tags,dists,rects,frame
    
def predictCam(camSerial=None,skipFranmes=1,outputFileName="",db=DB):
    '''
        predictCam(camSerial=None,skipFranmes=1,outputFileName="")
        
        perform predict on webcam the show the result to window
        press esc to exit
        
        skipFranmes: perform prediction every <skipFrames> frames
        outputFilename:output the predicted result(tag) to file<outputFilename>
    '''
    #即時辨識
    cap = None
    if not camSerial:
        for i in range(5):
            cap = cv2.VideoCapture(i,cv2.CAP_DSHOW)
            if cap.isOpened():break
    else: cap = cv2.VideoCapture(camSerial,cv2.CAP_DSHOW)
    cv2.startWindowThread()
    #detector = dlib.get_frontal_face_detector()
    count = 0
    while(True):    
        if not cap.isOpened():break
        ret, frame = cap.read()
        count+=1
        if count%skipFranmes!=0 :continue
        if ret:
            Tags,dists,rects,frame = predictImage(frame)
            if outputFileName!="":
                try:
                    with open(outputFileName,'w',encoding='UTF-8') as f:
                        for i in range(len(Tags)):
                            rect = [rects[i].left(),rects[i].top(),rects[i].right(),rects[i].bottom()]
                            f.write(Tags[i]+'\t'+str(dists[i])+'\t'+str(rect)+'\r\n' )
                except:print("file exception...")
            
            cv2.imshow('press esc to exit...', frame)
        if cv2.waitKey(10) == 27: break
    cap.release()
    cv2.destroyAllWindows()

def predictVedio(vedioPath,skipFranmes=10,db=DB):
    '''
    predictVedio(vedioPath,skipFranmes=10,db=DB)
    skipFranmes: perform prediction every <skipFrames> frames
    demo predicion from the vedio file
    press esc to exit
    '''
    cv2.startWindowThread()
    cap = cv2.VideoCapture(vedioPath)
    success,image = cap.read()
    count = 0
    while success:
        success,frame = cap.read()
        count+=1
        if count%skipFranmes!=0 :continue
        try:
            rects=detector(frame, 1)
            for rect in rects:
                V=getFeatureVector(frame,rect)
                Tag,dist=predictFromDB(V,db) # predict the target Tag
                cv2.rectangle(frame,(rect.left(),rect.top()),(rect.right(),rect.bottom()),(255,0,0),3)
                text=Tag+":"+str(dist)
                frame=addText2Img_cv2(frame,Tag+":"+str(round(dist,3)),_FONT,(rect.left(), rect.top()-_FONT.size-1))        
        except IndexError:pass    
        cv2.imshow('press esc to exit...', frame)
        if cv2.waitKey(10) == 27:                     # exit if Escape is hit
            break
    cap.release()
    cv2.destroyAllWindows()
    
#from skimage import transform
#import matplotlib.pyplot as plt
#from skimage.util import crop
if __name__ == "__main__":
    pass


