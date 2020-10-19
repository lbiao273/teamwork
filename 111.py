import os
import tkinter
import tkinter.messagebox
import math
import operator
from functools import reduce
from PIL import Image,ImageTk


pathlist1=[]
for root,dirs,files in os.walk(r".\cut_picture"):
        for file in files:
            pathlist1.append(root)
pathlist2=list(set(pathlist1))
pathlist2.sort()#文件夹名称列表