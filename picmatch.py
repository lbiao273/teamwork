import os
import tkinter
import tkinter.messagebox
import math
import operator
from functools import reduce
from PIL import Image,ImageTk
imglist=[]

def pic_cmp(img1,img2):
    image1=Image.open(img1)
    image2=Image.open(img2)
    h1=image1.histogram()
    h2=image2.histogram()
    result=math.sqrt(reduce(operator.add,list(map(lambda a,b:(a-b)**2,h1,h2)))/len(h1))
    return result#result==0则图片一致




pathlist1=[]#初始名称列表
imglist=[]

for root,dirs,files in os.walk(r".\cut_picture"):
        for file in files:
            pathlist1.append(root)
pathlist2=list(set(pathlist1))
pathlist2.sort()#文件夹名称列表
#for name in pathlist2:
#    print(name)

path1=r'.\test_picture'
for root,dirs,files in os.walk(r".\cut_picture"):
    for file in files:
        imglist.append(os.path.join(root,file))
        #print(file)
#print(imglist)#每个文件的路径+名字



for x in range(36):
    path2=pathlist2[x]
    k=0
    resultnum=[]#图片对比结果的数值列表
    #print(path2)
    for i in range(9):
        for j in range(9):
            temp=pic_cmp(os.path.join(path1,str(i)+'.png'),os.path.join(path2,str(j)+'.png'))
            resultnum.append(temp)
    resultnum.sort()
#    print(resultnum)
    for y in range(8):
        k+=resultnum[y]
#    print(k)
    if k==0:
        #print(path2)
        break
sqq=[]
#for i in range(9):
#    temp2=pic_cmp(os.path.join(path1,str(i)+'.png'),r'.\none.png')
#    print(temp2)
print(path2)
for i in range(9):
    temp2=pic_cmp(os.path.join(path1,str(i)+'.png'),r'.\none.png')
    for j in range(9):
        temp=pic_cmp(os.path.join(path1,str(i)+'.png'),os.path.join(path2,str(j)+'.png'))        
        if temp==0:
            sqq.append(j)
        elif temp!=0 and temp2==0:
            sqq.append(j)
            break
print(sqq)