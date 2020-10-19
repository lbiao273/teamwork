# -*- coding: utf-8 -*-
import os
import tkinter
import tkinter.messagebox
import math
import operator
from functools import reduce
from PIL import Image,ImageTk

picpath=r'.\orig_picture\B_.jpg'
savepath=r'.\cut_picture\B_'


img=Image.open(picpath)
w,h=img.size        
num=0
row_height=h/3
col_width=w/3
for r in range(3):
    for c in range(3):
        box=(c*col_width,r*row_height,(c+1)*col_width,(r+1)*row_height)
        img.crop(box).resize((150,150)).save(os.path.join(savepath,str(num)+'.png'),'png')
        num+=1