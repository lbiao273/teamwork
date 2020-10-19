import os
import tkinter
import tkinter.messagebox
import math
import operator
from functools import reduce
from PIL import Image,ImageTk

def pic_cmp(img1,img2):
    image1=Image.open(img1)
    image2=Image.open(img2)
    h1=image1.histogram()
    h2=image2.histogram()
    result=math.sqrt(reduce(operator.add,list(map(lambda a,b:(a-b)**2,h1,h2)))/len(h1))
    return result#result==0则图片一致

win=[0,0,0,0,0,0,0,0,0]
for i in range(9):
    for j in range(9):
        if cmp(os.path.join(r'.\test_picture',str(i)+'.png'),os.path.join(r'.\cut_picture\g_',str(j)+'.png'))==0:
           True 