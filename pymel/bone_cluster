#-*- encoding: utf-8
import maya.cmds as cmds
import maya.mel as mel
import csv
import codecs
import pymel.core as pm

# ルートボーンが選択されている状態で実行する必要あり

#リストからクラスターを作成する
#ボーンウェイトと対応するクラスターを作成

def GetBoneNames(root):
	cmds.select(root, hierarchy=True)
    
	return cmds.ls(sl=True)

def GetParentBone(name):
	parent = cmds.listRelatives(name, p=True)	# 親ボーン名を取得
	if parent != None:
		return parent[0]
	return ""

def ConstructParentHash(bones):
	bone_hash = {}
	for bone in bones:
		bone_hash[bone] = GetParentBone(bone)
	return bone_hash

def ConstructPositionHash(bones):
	positions = {}
	for bone in bones:
		# ボーンの座標を取得
		positions[bone] = cmds.xform(bone, q=True, ws=True, t=True)
	return positions

def GetPolyCount(mesh):
	return cmds.polyEvaluate(mesh, v=True)

def BoneWeightMap(skin_cluster, attr_name, names):#一つの頂点に対するウエイトを出す
	weights = {}
	for bname in names:
		weight = cmds.skinPercent(skin_cluster, attr_name, transform=bname, q=True) 
		if weight > 0.3 and weight != None:#肩が除外されないように作成する0.3 #閾値は場合に応じて調整
			weights[bname] = weight
			#break

	return weights

def GetSkinCluster(mesh):
	history = cmds.listHistory(mesh)
	for h in history:
		if cmds.objectType(h, isType='skinCluster'):
			return h
	return None

mesh = cmds.ls(sl=True)[0]#最初にメッシュ選択
root = cmds.ls(sl=True)[1]#2番目にルートボーン選択
skin_cluster = GetSkinCluster(mesh)

names = [u'Hips', u'Spine', u'Spine1', u'Neck',u'Head',u'LeftHip',u'LeftKnee',u'LeftFoot',u'RightHip',u'RightKnee',u'RightFoot',u'RightShoulder',u'RightArm',u'RightElbow',u'RightWrist',u'LeftShoulder',u'LeftArm',u'LeftElbow',u'LeftWrist']#GetBoneNames(root)#ボーンの名前リスト
parents = ConstructParentHash(names)
positions = ConstructPositionHash(names)
print(names)
poly_count = GetPolyCount(mesh)


Hip_list=[]#ボーンに対応するリスト作成
Spine_list=[]
Spine1_list=[]
#Spine2_list=[]
Head_list=[]
RightShoulder_list=[]
LeftShoulder_list=[]
Rightfoot_list=[]
Leftfoot_list=[]



for i in range(poly_count):#ウエイトリストを作成
	attr_name = mesh + ".vtx[" + str(i) + "]"#頂点番号#
	weights = BoneWeightMap(skin_cluster, attr_name, names)
	#print(i,weights)	
	if "Hips" in weights:
	    Hip_list.append(mesh + ".vtx[" + str(i) + "]")
	elif "Spine1" in weights:
	    Spine1_list.append(mesh + ".vtx[" + str(i) + "]")
	#elif "Spine2" in weights:
	    #Spine2_list.append(mesh + ".vtx[" + str(i) + "]")
	elif "Spine" in weights:
	    Spine_list.append(mesh + ".vtx[" + str(i) + "]")
	elif "Head" in weights:
	    Head_list.append(mesh + ".vtx[" + str(i) + "]")
	elif "RightShoulder" in weights:
	    RightShoulder_list.append(mesh + ".vtx[" + str(i) + "]")
	elif "RightArm" in weights:
	    RightShoulder_list.append(mesh + ".vtx[" + str(i) + "]")
	elif "RightElbow" in weights:
	    RightShoulder_list.append(mesh + ".vtx[" + str(i) + "]")        
	elif "RightWrist" in weights:
	    RightShoulder_list.append(mesh + ".vtx[" + str(i) + "]")  

	elif "LeftShoulder" in weights:
	    LeftShoulder_list.append(mesh + ".vtx[" + str(i) + "]")
	elif "LeftArm" in weights:
	    LeftShoulder_list.append(mesh + ".vtx[" + str(i) + "]")
	elif "LeftElbow" in weights:
	    LeftShoulder_list.append(mesh + ".vtx[" + str(i) + "]")        
	elif "LeftWrist" in weights:
	    LeftShoulder_list.append(mesh + ".vtx[" + str(i) + "]")   	

	elif "RightHip" in weights:
	    Rightfoot_list.append(mesh + ".vtx[" + str(i) + "]")  
	elif "RightKnee" in weights:
	    Rightfoot_list.append(mesh + ".vtx[" + str(i) + "]")  
	elif "RightFoot" in weights:
	    Rightfoot_list.append(mesh + ".vtx[" + str(i) + "]")  

	elif "LeftHip" in weights:
	    Leftfoot_list.append(mesh + ".vtx[" + str(i) + "]")  
	elif "LeftKnee" in weights:
	    Leftfoot_list.append(mesh + ".vtx[" + str(i) + "]")  
	elif "LeftFoot" in weights:
	    Leftfoot_list.append(mesh + ".vtx[" + str(i) + "]")  





#print(Hip_list)
#print(Spine_list)	
#print(Spine1_list)	
#print(Spine2_list)		


#クラスタのピボットとボーンの位置を対応させる
pm.select(Hip_list)
pm.cluster(n="Hip_cluster")

pm.select(Spine_list)
pm.cluster(n="Spine_cluster")
	
pm.select(Spine1_list)
pm.cluster(n="Spine1_cluster")

#pm.select(Spine2_list)
#pm.cluster(n="Spine2_cluster")

pm.select(Head_list)
pm.cluster(n="Head_cluster")

pm.select(RightShoulder_list)
pm.cluster(n="RightShoulder_cluster")

pm.select(LeftShoulder_list)
pm.cluster(n="LeftShoulder_cluster")

pm.select(Leftfoot_list)
pm.cluster(n="Leftfoot_cluster")

pm.select(Rightfoot_list)
pm.cluster(n="Rightfoot_cluster")



#クラスターの中心とボーンの中心合わせる
sel = pm.select("Hip_cluster")
sel = pm.selected()[0]
#pvt = sel.getPivots(worldSpace=True)[0]
pm.select("Hips")

tx = cmds.xform(q=True, ws=True, t=True)[0]
ty = cmds.xform(q=True, ws=True, t=True)[1]
tz = cmds.xform(q=True, ws=True, t=True)[2]
sel.setPivots([tx,ty,tz],absolute=True,worldSpace=True)


sel = pm.select("Spine_cluster")
sel = pm.selected()[0]
pvt = sel.getPivots(worldSpace=True)[0]
pm.select("Spine")

tx = cmds.xform(q=True, ws=True, t=True)[0]
ty = cmds.xform(q=True, ws=True, t=True)[1]
tz = cmds.xform(q=True, ws=True, t=True)[2]
sel.setPivots([tx,ty,tz],absolute=True,worldSpace=True)


sel = pm.select("Spine1_cluster")
sel = pm.selected()[0]
#pvt = sel.getPivots(worldSpace=True)[0]
pm.select("Spine1")

tx = cmds.xform(q=True, ws=True, t=True)[0]
ty = cmds.xform(q=True, ws=True, t=True)[1]
tz = cmds.xform(q=True, ws=True, t=True)[2]
sel.setPivots([tx,ty,tz],absolute=True,worldSpace=True)



sel = pm.select("Leftfoot_cluster")
sel = pm.selected()[0]
pvt = sel.getPivots(worldSpace=True)[0]
pm.select("LeftKnee")

tx = cmds.xform(q=True, ws=True, t=True)[0]
ty = cmds.xform(q=True, ws=True, t=True)[1]
tz = cmds.xform(q=True, ws=True, t=True)[2]
sel.setPivots([tx,ty,tz],absolute=True,worldSpace=True)



sel = pm.select("Rightfoot_cluster")
sel = pm.selected()[0]
pvt = sel.getPivots(worldSpace=True)[0]
pm.select("RightKnee")

tx = cmds.xform(q=True, ws=True, t=True)[0]
ty = cmds.xform(q=True, ws=True, t=True)[1]
tz = cmds.xform(q=True, ws=True, t=True)[2]
sel.setPivots([tx,ty,tz],absolute=True,worldSpace=True)

