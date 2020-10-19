# -*- coding: utf-8 -*-
import os
import tkinter
import tkinter.messagebox
import math
import operator
from functools import reduce
from PIL import Image,ImageTk

sqqq=[]
sq=[]
standard=[]
N=3
start_flag=0
step=0
mark_row=0
mark_col=0
operates=""
pic_path=r'.\test_picture\test_pic.jpg'
save_path=r'.\test_picture'

def pic_cmp(img1,img2):
    image1=Image.open(img1)
    image2=Image.open(img2)
    h1=image1.histogram()
    h2=image2.histogram()
    result=math.sqrt(reduce(operator.add,list(map(lambda a,b:(a-b)**2,h1,h2)))/len(h1))
    return result#result==0则图片一致

class Imageblock:
    def __init__(self,num):
        self.num=num
    def draw(self,canvas,pos_x,pos_y):
        img=Pics[self.num]
        canvas.create_image(pos_x,pos_y,image=img)
'''
class stdImageblock:
    def __init__(self,num):
        self.num=num
    def draw(self,canvas,pos_x,pos_y):
        img=stdPics[self.num]
        canvas.create_image(pos_x,pos_y,image=img)
'''
def split_image(picpath,row,col,savepath):
    img=Image.open(picpath)
    w,h=img.size        
    num=0
    row_height=h/row
    col_width=w/col
    for r in range(row):
        for c in range(col):
            box=(c*col_width,r*row_height,(c+1)*col_width,(r+1)*row_height)
            img.crop(box).resize((150,150)).save(os.path.join(savepath,str(num)+'.png'),'png')
            num+=1

def pic_match():
    pathlist1=[]
    imglist=[]
    for root,dummy_dirs,files in os.walk(r".\cut_picture"):
            for file in files:
                pathlist1.append(root)
    pathlist2=list(set(pathlist1))
    pathlist2.sort()#文件夹名称列表

    path1=r'.\test_picture'
    for root,dirs,files in os.walk(r".\cut_picture"):
        for file in files:
            imglist.append(os.path.join(root,file))
    resultnum=[]
    for x in range(36):
        path2=pathlist2[x]
        k=0
        resultnum=[]
        for i in range(9):
            for j in range(9):
                temp=pic_cmp(os.path.join(path1,str(i)+'.png'),os.path.join(path2,str(j)+'.png'))
                resultnum.append(temp)
        resultnum.sort()        
        for y in range(8):
            k+=resultnum[y]
        if k==0:
            path2
            return path2

def find_white():
    white_pic=r'.\none.png'
    for i in range(9):
        pic=r'.\test_picture\\'+str(i)+'.png'
        flag=pic_cmp(white_pic,pic)
        if flag==0:
            return i
        else:
            continue

def initsquare():
    global mark_row,mark_col
    i=0
    for row in range(N):
        sq.append([])
        for col in range(N):
            sq[row].append([])
            sq[row][col]=Imageblock(i)
            i+=1
    #print(sq)
    flag=find_white()
    mark_row=math.floor(flag/3)
    mark_col=flag%3

def initanswer():
    sqq=[]
    path1=r'.\test_picture'
    path2=pic_match()
    for i in range(9):
        temp2=pic_cmp(os.path.join(path1,str(i)+'.png'),r'.\none.png')
        for j in range(9):
            temp=pic_cmp(os.path.join(path1,str(i)+'.png'),os.path.join(path2,str(j)+'.png'))
            if temp==0:
                sqq.append(j)
            elif temp!=0 and temp2==0:
                sqq.append(j)
                break
    return sqq

def draw_image(cv):
    cv.create_polygon((0,0,150,0,150,150,0,150),width=1,outline='Black',fill='grey')
    for i in range(N):
        for j in range(N):
            if(sq[i][j]!=None):
                sq[i][j].draw(cv,150*(j+0.5),150*(i+0.5))

def keyboard(event):
    global step,cv,mark_col,mark_row,operates
    if event.keysym=="w" or event.keysym=="Up":
        if mark_row!=0:
            temp=sq[mark_row-1][mark_col]
            sq[mark_row-1][mark_col]=sq[mark_row][mark_col]
            sq[mark_row][mark_col]=temp
            temp2=sqqq[3*(mark_row-1)+mark_col]
            sqqq[3*(mark_row-1)+mark_col]=sqqq[3*(mark_row)+mark_col]
            sqqq[3*(mark_row)+mark_col]=temp2
            mark_row-=1
            operates+="w"
            step+=1
            print(sqqq)
            print(operates)
    elif event.keysym=="a" or event.keysym=="Left":
        if mark_col!=0:
            temp=sq[mark_row][mark_col-1]
            sq[mark_row][mark_col-1]=sq[mark_row][mark_col]
            sq[mark_row][mark_col]=temp
            temp2=sqqq[3*(mark_row)+mark_col-1]
            sqqq[3*(mark_row)+mark_col-1]=sqqq[3*(mark_row)+mark_col]
            sqqq[3*(mark_row)+mark_col]=temp2
            mark_col-=1
            operates+="a"
            step+=1
            print(sqqq)
            print(operates)
    elif event.keysym=="s" or event.keysym=="Down":
        if mark_row!=2:
            temp=sq[mark_row+1][mark_col]
            sq[mark_row+1][mark_col]=sq[mark_row][mark_col]
            sq[mark_row][mark_col]=temp
            temp2=sqqq[3*(mark_row+1)+mark_col]
            sqqq[3*(mark_row+1)+mark_col]=sqqq[3*(mark_row)+mark_col]
            sqqq[3*(mark_row)+mark_col]=temp2
            mark_row+=1
            operates+="s"
            step+=1
            print(sqqq)
            print(operates)
    elif event.keysym=="d" or event.keysym=="Right":
        if mark_col!=2:
            temp=sq[mark_row][mark_col+1]
            sq[mark_row][mark_col+1]=sq[mark_row][mark_col]
            sq[mark_row][mark_col]=temp
            temp2=sqqq[3*(mark_row)+mark_col+1]
            sqqq[3*(mark_row)+mark_col+1]=sqqq[3*(mark_row)+mark_col]
            sqqq[3*(mark_row)+mark_col]=temp2
            mark_col+=1
            operates+="d"
            step+=1
            print(sqqq)
            print(operates)
    label_step["text"]=str(step)
    cv.delete('all')
    draw_image(cv)
    if iswin():
        tkinter.messagebox.showinfo(title="恭喜",message="挑战成功！")

def iswin():
    if sqqq==[0,1,2,3,4,5,6,7,8]:
        return True
    else:
        return False

def start():
    global menu,start_flag
    menu.destroy()
    game_window=tkinter.Tk()
    game_window.destroy()
    start_flag=1

def setting():
    setting_window=tkinter.Toplevel()
    setting_window.title('关于')
    setting_window.geometry('200x50')
    setting_window.resizable(False, False)
    tkinter.Label(setting_window,text="制作人员：赖彪，刘惟凝",font='微软雅黑').pack()

def game_begining():
    global step,operates
    step=0
    operates=""
    initsquare()
    #initanswer()
    
def game_ending():
    print("再玩一次")
    game_begining()
    print(step)
    cv.delete('all')
    draw_image(cv)

def game_quit():
    global menu,game_window
    game_window.destroy()

#主界面
menu=tkinter.Tk()
menu.title('图片华容道')
menu.geometry('300x300+600+200')
menu.resizable(False, False)
tkinter.Label(menu,text='图片华容道',font=('微软雅黑',20)).place(x=80,y=50)
tkinter.Button(menu,text="开始游戏",command=start,width=10,font='微软雅黑').place(x=90,y=140) 
tkinter.Button(menu,text="关于",command=setting,width=10,font='微软雅黑').place(x=90,y=220)
menu.mainloop()

#游戏界面
if(start_flag):
    game_window=tkinter.Tk()  
    game_window.title('图片华容道')
    game_window.geometry('650x650+450+60')
    game_window.resizable(False, False)
    #split_image(pic_path,N,N,save_path) 
    cv=tkinter.Canvas(game_window,bg='grey',width=450,height=450)

    Pics=[]
    for i in range(N*N):
        filename=Image.open(r'.\test_picture\\'+str(i)+'.png')
        picture=ImageTk.PhotoImage(filename)
        Pics.append(picture)
    #print(Pics)#内存地址
    p=pic_match()
    print(p)
    sqqq=initanswer()
    print(sqqq)

    stdPics=[]
    for i in range(N*N):
        filename=Image.open(os.path.join(p,str(i)+'.png'))
        picture=ImageTk.PhotoImage(filename)
        stdPics.append(picture)

    again=tkinter.Button(game_window,text="再玩一次",command=game_ending,font='微软雅黑')
    quitgame=tkinter.Button(game_window,text="退出游戏",command=game_quit,font='微软雅黑')
    tkinter.Label(game_window,text="步数：",font='微软雅黑').pack()
    label_step=tkinter.Label(game_window,text="0",fg="red",font='微软雅黑')
    label_step.pack()
    cv.bind_all("<KeyPress-w>",keyboard)
    cv.bind_all("<KeyPress-a>",keyboard)
    cv.bind_all("<KeyPress-s>",keyboard)
    cv.bind_all("<KeyPress-d>",keyboard)
    cv.bind_all("<KeyPress-Up>",keyboard)
    cv.bind_all("<KeyPress-Down>",keyboard)
    cv.bind_all("<KeyPress-Left>",keyboard)
    cv.bind_all("<KeyPress-Right>",keyboard)
    cv.pack()
    again.pack()
    quitgame.pack()
    game_begining()
    draw_image(cv)
    game_window.mainloop()