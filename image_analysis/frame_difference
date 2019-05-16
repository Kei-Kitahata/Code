#coding:Shift_JIS
import cv2
import numpy as np
import pylab as plt
from PIL import Image
import matplotlib.animation as animation
import matplotlib
import math
from collections import Counter
from scipy import signal

#
name="test"
cap = cv2.VideoCapture(name+'.mp4')

# 最初のフレームの処理
end_flag, frame = cap.read()
gray_prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(frame)
width = frame.shape[0]
height = frame.shape[1]
time=0

fig=plt.figure()
tmp=[]
change=np.array([])

while(end_flag):
    # グレースケールに変換
    gray_next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    time=time+1
    # ウィンドウに表示
    #cv2.imshow('window', gray_next)
    #plt.figure()   
    # ESCキー押下で終了
    if cv2.waitKey(30) & 0xff == 27:
        break
    #cv2.imwrite("walk_"+str(time)+".png",gray_next ) 
    diff1=cv2.absdiff(gray_next,gray_prev)
    contour=255-diff1
    #cv2.imwrite("walk2_"+str(time)+".png",diff1 )  
     
   

#xフレーム、x＋１フレーム共通範囲
    bitwise_or = cv2.bitwise_or(gray_next,gray_prev)
    #cv2.imwrite("bitwise_and.png", bitwise_and)
    #cv2.imwrite("walkor"+str(time)+".png",bitwise_or )


    #xフレーム、x＋１フレームの合計
    bitwise_and = cv2.bitwise_and(gray_next,gray_prev)
    #cv2.imwrite("bitwise_and.png", bitwise_and)
    #cv2.imwrite("walkand"+str(time)+".png",bitwise_and )

    #x＋１フレームの新規情報
    pre_frame=gray_prev-bitwise_and
    pre_frame2=255-pre_frame
    #cv2.imwrite("walknew2_"+str(time)+".png",pre_frame2 )

    # 2値化
    gray = cv2.threshold(pre_frame2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #cv2.imwrite("walknew2_"+str(time)+".png",gray )
    height = gray.shape[0]
    width = gray.shape[1]
    ########################################
    count=0
    for y in range(height):
        for x in range(width):
            if gray[y][x]==0:
                count=count+1
    tmp.append(count)
    change=np.append(change,count)
 #############################################
    print("------------",count)
    # 次のフレーム、ポイントの準備
    gray_prev = gray_next.copy()
    #feature_prev = good_next.reshape(-1, 1, 2)
    end_flag, frame = cap.read()
    print(time)


#変化をグラフで確認
#plt.plot(tmp) 
#plt.show()
#print(tmp)
#print(change)
 #極大値のインデックスを取得
maxId = signal.argrelmax(change)

 #極小値のインデックスを取得
minId = signal.argrelmin(change)
print(maxId)
#print(maxId[0][0])
print(minId)

#変化の極大値を持つフレームをリスト化
maxid_frame=np.array([],dtype=np.int)
for i in range(change.size):
    if i in maxId[0]:
        maxid_frame=np.append(maxid_frame,i)

maxid_frame=np.append(maxid_frame,1 )
maxid_frame=np.append(maxid_frame,time-1)
maxid_frame=np.unique(maxid_frame)

maxid_frame=np.array(np.sort(maxid_frame),dtype=np.int64)
print(maxid_frame)
#print(maxid_frame.dtype)
#need_frameに必要なフレームを代入

need_frame=np.array([],dtype=np.int)
frame_size=maxid_frame.size

while True:
    A=0#フレーム間が3フレームの処理の回数
    B=0#フレーム間が4フレームの回数
    C=0#フレーム間が5フレームの回数
    D=0#フレーム間が5フレームの回数の中で中心と上端の間探した
    E=0#フレーム間が5フレームの回数の中で中心と下端の間探した

    for i in range(frame_size-1):
        need_frame=np.append(need_frame,maxid_frame[i])
        if maxid_frame[i+1]-maxid_frame[i]==4:#フレーム間が3フレーム
            if (maxid_frame[i+1]+maxid_frame[i])/2==0:
              continue
            need_frame=np.append(need_frame, (maxid_frame[i+1]+maxid_frame[i])/2  )
            A=A+1
            
        if maxid_frame[i+1]-maxid_frame[i]==5:#フレーム間が4フレーム
            intermediate=round( ( change[ maxid_frame[i+1] ]+change[ maxid_frame[i] ] ) / 2 )
            t=intermediate
            t_time=0
            #print("===================",maxid_frame[i],maxid_frame[i+1])
            for j in range(maxid_frame[i]+2,maxid_frame[i+1]-1):
                if abs(change[j]- intermediate) < t:
                    t = abs(change[j]- intermediate)
                    t_time=j
            if t_time==0:
                continue
            need_frame=np.append(need_frame,t_time)
            B=B+1
               
       
        if maxid_frame[i+1]-maxid_frame[i]>5:   #フレーム間が5フレーム 以上
            #print(change[ maxid_frame[i] ],change[ maxid_frame[i+1] ])
            intermediate=round( ( change[ maxid_frame[i] ]+change[ maxid_frame[i+1] ] ) / 2 )
            t=intermediate
            t_time=0
            for j in range(maxid_frame[i]+2,maxid_frame[i+1]-1):
                if abs(change[j]- intermediate) < t: #極値の平均変化量に一番近い点探す
                    t = abs(change[j]- intermediate)
                    t_time=j
                    
            if abs(maxid_frame[i]-t_time)> 1 and abs(maxid_frame[i+1] - t_time) >1:
                print("--------t_time",t_time)
                if t_time ==0:
                    continue
                need_frame=np.append(need_frame,t_time)
                C=C+1
        
            #中心と上端の間探す
            intermediate=round( ( change[ maxid_frame[i+1] ]+change[t_time] ) / 2 )
            t=intermediate
            t1_time=t_time
            for j in range(t_time+2,maxid_frame[i+1]-1):
                if abs(change[j]- intermediate) < t:
                    t = abs(change[j]- intermediate)
                    t1_time=j
                
            if abs(t1_time-t_time)> 1 and abs(maxid_frame[i+1]  - t1_time) >1:
                print("----------t1_time",t1_time)
                if t1_time ==0:
                    continue
                need_frame=np.append(need_frame,t1_time)
                D=D+1

            #中心と下端の間探す                
            intermediate=round( ( change[ maxid_frame[i] ]+change[t_time] ) / 2 )
            t=intermediate
            t2_time=t_time
            for j in range(maxid_frame[i]+2,t_time-1):
               if abs(change[j]- intermediate) < t:
                   t = abs(change[j]- intermediate)
                   t2_time=j
               
            if abs(t2_time-t_time)>1 and abs(maxid_frame[i] - t2_time) >1:
                 print("------t2_time",t2_time)
                 if t2_time ==0:
                    continue
                 need_frame=np.append(need_frame,t2_time)
                 E=E+1
    
    if maxid_frame[frame_size-1]  not in need_frame :
       need_frame=np.append(need_frame,maxid_frame[frame_size-1])

    need_frame=np.unique(need_frame)#重複を除く                     
    frame_size=need_frame.size 
    maxid_frame=np.array(np.sort(need_frame),dtype=np.int)
    print(maxid_frame)
 
    print("3フレーム間埋めー",A,"  4フレーム間埋めー",B,"  5フレーム以上間埋めー",C)    
    if A==0 and B==0 and C==0 and D==0 and E==0 :
        break
        

need_frame=np.array(np.sort(need_frame),dtype=np.int)#順番並び替え
print(np.sort(need_frame))

cap.release()

##################################################書き出し

cap = cv2.VideoCapture("test"+'.mp4')
# 最初のフレームの処理
end_flag, frame = cap.read()
gray_prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(frame)
time=0
width = frame.shape[0]
height = frame.shape[1]

while(end_flag):
    # グレースケールに変換
    time=time+1
    if time in need_frame:
        gray_next = frame   
    cv2.imwrite("test"+"_frame_"+str(time)+".png",gray_next)
    
    # 次のフレーム、ポイントの準備
    gray_prev = gray_next.copy()
    #feature_prev = good_next.reshape(-1, 1, 2)
    end_flag, frame = cap.read()

    print(time)
cap.release()


# 終了処理
cv2.destroyAllWindows()
cap.release()
