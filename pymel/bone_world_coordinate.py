#coding:Shift_JIS

import pymel.core as pm
import math
import maya.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel

#MAYA内のボーンのワールド座標位置、回転を書き出す

#obj.getSiblings()#同階層所得
#obj.root()#最上位ノード所得
#obj.getParent()#親ノード
#obj.getAllParents()#最上位層までの親所得
#obj.getChildren()#子ノード所得
def bone_list(root):
    pm.select(root)
    pm.select(hierarchy=True)#階層選択
    select_object = pm.ls(sl=True)#階層すべてをリスト構造化
    print(select_object)
    select_joint = []
    i=0
    for node in select_object:#手足の指先の座標を除く
        #適宜指先の名前に変更
        if  "Thumb" in str(node) :#分配してif文組まないと反応しない
            #print(node)
            continue
        if  "Index" in str(node) :
            #print(node)
            continue
        if  "Middle" in str(node) :
            #print(node)
            continue
        if  "Ring" in str(node) :
            #print(node)
            continue
        if  "Pinky" in str(node) :
            #print(node)
            continue
            
        if node.type() != "joint":
            continue  
        select_joint.append(node)
    return select_joint
#print(select_joint)    
##############################################################################


def bone_coordinate(select_joint,key_frame):
    key_list=[]#[ボーン名、時間、ワールド座標、ワールド回転]
    for i in key_frame:#キーフレームの時の座標
        #in range(len(key_frame2))でキーフレームの長さ分
        #range(a,b+1)///フレームaからbの範囲で
        pm.currentTime(i)#現在の時間をiに設定
        for node in select_joint:
            #ジョイントとループさせる
            pm.select(node) 
            #cmds.xform(q=True, ws=True, ro=True) ワールド座標での回転
            #ws=ワールド空間の変換値として値を扱います。#t=	移動XYZ ro=回転値#q=値を取得する
            key_list.append([node,i,cmds.xform(q=True, ws=True, t=True),cmds.xform(q=True, ws=True, ro=True)])
    return key_list


#ルートボーンより階層で処理
#ルートボーンのキーフレームがkey_frameに格納される
root = pm.selected()[0]
select_joint=bone_list(root)
pm.selectKey(time='1:48')  #xフレームからyフレームの時間内で処理



key_frame = pm.keyframe(q=True, sl=True)
key_frame = list(set(key_frame))#重複排除
key_frame.sort()
key_list=bone_coordinate(select_joint,key_frame)

print(key_list)#[ボーン名、時間、ワールド座標、ワールド回転]

