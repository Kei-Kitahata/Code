#coding:Shift_JIS
import cv2
import numpy as np
import pylab as plt
from PIL import Image
import math


def fft_graph(img):
    #画像を読み込みフーリエ変化する
    #フーリエ変換した画像の特定の周波数を取り出し画像に出力
    #周波数領域での周波数方向および角度方向のグラフを算出する

    cv2.imwrite("imggray.jpg",img)
    #低周波のみ
    #floatに変換
    img_float32 = np.float32(img)
    #フーリエ変換
    dft = cv2.dft(img_float32, flags = cv2.DFT_COMPLEX_OUTPUT)
    #スワップ
    dft_shift = np.fft.fftshift(dft)
    rows, cols = img.shape
    # 画像中央
    crow= int(rows/2)
    ccol =int(cols/2)
    # マスク作成： 中央領域は１、 その他はすべて０ 
    mask = np.zeros( (rows, cols,2), np.uint8)

    R=127  #元はR=10
    A=1
    for x in range(0,R+1):
        for y in range(0,R+1):
           if (x*x+y*y<=127*127 )and x*x+y*y>=60*60:
             mask[crow+y,ccol+x] = A
             mask[crow+y,ccol-x]=A
             mask[crow-y,ccol+x]= A
             mask[crow-y,ccol-x]=A
         
    # 周波数空間でマスク適用
    fshift = dft_shift*mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)

     # 二乗和して根を取り正にへ magnitude()
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
    low_img=img_back
    fig,ax = plt.subplots()
    plt.imshow(img_back, cmap = 'gray')
    ax.tick_params(labelbottom="off",bottom="off") # x軸の削除
    ax.tick_params(labelleft="off",left="off") # y軸の削除
    ax.set_xticklabels([]) 
    plt.box("off") #枠線の削除
    plt.savefig("gray"+".jpg",format = 'jpg', bbox_inches="tight", pad_inches=0.0)
    plt.savefig(name+"gray"+".jpg",format = 'jpg', bbox_inches="tight", pad_inches=0.0)
    plt.close()
    img2 = cv2.imread("gray.jpg",1)
    #-------------------------以下FFT--------------------------------------------------------------
    img2 = cv2.imread(file_src,0)
    gray_next=img
    height, width = img.shape[:2]

    ## マスク作成： 中央領域は１、 その他はすべて０ 
    mask = np.zeros( (rows, cols), np.uint8)
    #R=15  #元はR=10
    for x in range(0,R+1):
        for y in range(0,R+1):
          if (x*x+y*y<=127*127 )and x*x+y*y>=60*60:
             mask[crow+y,ccol+x] = A
             mask[crow+y,ccol-x]=A
             mask[crow-y,ccol+x]= A
             mask[crow-y,ccol-x]=A

    fig=plt.figure()
    rows=height
    cols=width
    crow= int(rows/2)      # 画像中央
    ccol =int(cols/2)
    #フーリエ変換
    dft= np.fft.fft2(gray_next)
    #スワップ
    dft_shift = np.fft.fftshift(dft)

    # 周波数空間でマスク適用
    fshift = dft_shift*mask
    dft_shift=fshift
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    plt.subplot(2,2,1),plt.imshow(low_img, cmap = 'gray')
    F_= np.log(5 + np.fft.fftshift(np.abs(f_ishift)))
    plt.subplot(2,2,2),plt.imshow(F_,cmap = 'gray')

    ##########周波数領域、角度方向でマスクする################################################################### 
    phase = np.zeros(dft_shift.shape, dtype=np.float32)
    amplitude= np.zeros(dft_shift.shape, dtype=np.float32)
    power= np.zeros(dft_shift.shape, dtype=np.float32)

    for y in range( dft_shift.shape[0]):
           for x in range( dft_shift.shape[1] ):
                 phase[y][x] = math.degrees(math.atan2(dft_shift[y][x].imag , dft_shift[y][x].real) )
                 amplitude[y][x]=math.sqrt(  pow( (dft_shift[y][x].imag),2)+ pow( (dft_shift[y][x].real),2) )
                 power[y][x] = pow( (dft_shift[y][x].imag),2)+ pow( (dft_shift[y][x].real),2) 

    Degree = np.zeros(180)

    for angle in range(1,180):
           if angle ==90:
                continue
           for y in range( dft_shift.shape[0]):
               for x in range( dft_shift.shape[1] ):
                    if  (    (math.degrees( math.atan2(y-crow ,x-ccol) ) ) >= angle and math.degrees( math.atan2(y-crow ,x-ccol) )< (angle+1)    ) or (    (math.degrees( math.atan2(y-crow ,x-ccol) ) +180 ) >= angle and math.degrees( math.atan2(y-crow ,x-ccol) ) +180 < (angle+1)   ) :
                    #print(math.degrees(math.atan2(y-crow ,x-ccol) ) )
                          Degree[angle] = power[y][x]+Degree[angle]
          
    plt.subplot(2,2,3)
    x = range(0, 180)
    plt.plot(x,Degree)
    plt.yscale("log")
    plt.ylim(1000000000,1000000000000)
    plt.xlim(0,180)
    plt.title("Degree")

    Freq = np.zeros(width)
    for r in range(0,ccol):
           for y in range( dft_shift.shape[0]):
                for x in range( dft_shift.shape[1] ):
                     if(math.sqrt(pow(x-ccol,2)+pow(y-crow,2) )>=r and math.sqrt( pow(x-ccol,2)+pow(y-crow,2) ) < (r+1) ):
                        Freq[r]=math.sqrt( power[y][x] ) + Freq[r]
    #空間周波数は半径r
    plt.subplot(2,2,4)
    plt.title("Freqency")
    plt.ylim(1000000,15000000)
    plt.yscale("log")
    plt.xscale("log")
    plt.xlim(1,128)
    plt.plot(Freq)
    plt.savefig(name+"FFT_"+".png",format = 'png', dpi=300)
    plt.close()

    
def hist(img):
    #ヒストグラムを求め、グラフ化
    cv2.imwrite("gray_scale.jpg", img)
    height, width = img.shape[:2]
    fig=plt.figure()
    plt.subplot(2,1,1)
    plt.imshow(img, cmap = 'gray')
    plt.subplot(2,1,2)
    plt.xlim(0, 256)
    plt.hist(img.ravel(),255,[0,256])   
    plt.grid()
    plt.savefig(name+"_hist"+".png",format = 'png', dpi=300)
    plt.close()  
   

#入力
name='test'
file_src = name+'.jpg'
img = cv2.imread(file_src,0)
fft_graph(img)
hist(img)


cv2.waitKey(0)
cv2.destroyAllWindows()