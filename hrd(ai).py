# coding=utf-8
"""
Spyder Editor

This is a temporary script file.
"""
import os
import base64
import numpy as np
import random      
import requests
import json
import copy
import pytest
from PIL import Image
from io import BytesIO

class Square:
    def __init__(self,stat,pos,step=0,prboard=None,prpath=""):
        self.stat = stat
        self.pos = pos
        self.step = step
        self.cost = self.cal_cost()
        self.prboard = prboard
        self.prpath = prpath

    def cal_cost(self):
        count = 0
        sheet = [[0, 0], [0, 1], [0, 2],
                 [1, 0], [1, 1], [1, 2],
                 [2, 0], [2, 1], [2, 2]]
        for i in range(9):
            if self.stat[i] < 0:
                continue
            count += abs(sheet[i][0] - sheet[self.stat[i]][0]) + abs(sheet[i][1] - sheet[self.stat[i]][1])
        return count+self.step

class IDA:
    # (w上, d右, s下, a左)
    d = [[-1, 1, 3, -1], # 0
         [-1, 2, 4, 0],  # 1
         [-1, -1, 5, 1], # 2
         [0, 4, 6, -1],  # 3
         [1, 5, 7, 3],   # 4
         [2, -1, 8, 4],  # 5
         [3, 7, -1, -1], # 6
         [4, 8, -1, 6],  # 7
         [5, -1, -1, 7]] # 8 (-1表示无法移动)
    # 将移动方向的序列转化为'w', 'd', 's', 'a'
    index_to_direct = ['w', 'd', 's', 'a']
    swap_record = {}    # 记录强制交换的交换方案
    # forced_mark = True  # 标记最初的强制交换的可解性
    no_swap_exe = True  # 标记是否执行了强制交换
    find_sol = False  # 标记是否解决八数码问题

    def __init__(self, start, pos, target,num,swap_schedule):
        # 起始状态、白块初始位置、目标状态、第几步进行强制交换、强制交换的最初方案
        IDA.start = start
        IDA.pos = pos
        IDA.target = target
        IDA.init = Square(start, pos)
        IDA.maxdep = 0   # 搜索的最大深度
        IDA.path = ""
        IDA.num = num
        IDA.swap_schedule = swap_schedule
        # 判断目标状态的逆序对数是奇数还是偶数，当前状态必须与目标状态同奇同偶才可解
        IDA.solvable = Judge(target)

    def IDA(self):
        self.maxdep = self.init.cost
        while not self.dfs(self.init, -1, 0):
            self.maxdep += 1
        tmp_path = self.path[::-1]
        self.path = ""
        if not self.find_sol:
            while not self.dfs(self.init, -1, 0):
                self.maxdep += 1
        self.path = tmp_path + self.path[::-1]
        return self.path

    def dfs(self, now, lastd, n):#深度搜索
        if now.stat == self.target:
            self.find_sol = True
            return True

        if self.no_swap_exe and n == self.num:
            scheme = self.forced_exchange(now.stat)
            self.no_swap_exe = False
            now.stat[scheme[0]], now.stat[scheme[1]] = now.stat[scheme[1]], now.stat[scheme[0]]
            now.step = 0    # 强制交换后，从头搜索
            # 记录白块位置
            for i in range(len(now.stat)):
                if now.stat[i] < 0:
                    now.pos = i
                    break
            now.cost = now.cal_cost()  # 交换后重新计算代价
            self.maxdep = now.cost  # 重新计算最大深度
            self.init.stat = copy.deepcopy(now.stat)
            self.init.pos = now.pos
            self.init.step = now.step
            self.init.cost = now.cost
            self.swap_scheme = copy.deepcopy(scheme)  # 记录交换方案
            return True
        if now.cost > self.maxdep:
            return False

        pos = now.pos
        step = now.step
        for i in range(4):
            # 方向不可走时
            if self.d[pos][i] == -1:
                continue
            if (lastd == -1) or (lastd % 2) != (i % 2) or (lastd == i):
                stat = copy.deepcopy(now.stat)
                stat[pos], stat[self.d[pos][i]] = stat[self.d[pos][i]], stat[pos]
                temp = Square(stat, self.d[pos][i], step + 1, now, self.index_to_direct[i])
                # 如果找到最短路径，递归地记录路径
                if self.dfs(temp, i, n+1):
                    self.path += temp.prpath
                    return True
        return False

    def forced_exchange(self, stat):
        # 交换两个块
        tmp0 = copy.deepcopy(stat)
        if self.swap_schedule[0]!= self.swap_schedule[1]:
            tmp0[self.swap_schedule[0]], tmp0[self.swap_schedule[1]] = tmp0[self.swap_schedule[1]], tmp0[self.swap_schedule[0]]
        if Judge(tmp0) == self.solvable:
            # print("first Ok!")
            return self.swap_schedule
        # 否则，进行自由交换
        else:
            # 先要强制交换，在强制交换的基础上自由交换
            stat[self.swap_schedule[0]], stat[self.swap_schedule[1]] = stat[self.swap_schedule[1]], stat[self.swap_schedule[0]]
            # 双重循环，遍历可自由交换出的所有状态
            for i in range(8):
                for j in range(i+1, 9):
                    tmp = copy.deepcopy(tmp0)
                    tmp[i], tmp[j] = tmp[j], tmp[i]
                    if Judge(tmp) == self.solvable:
                        for k in range(len(tmp)):
                            if tmp[k] < 0:
                                break
                        tmp_square = Square(tmp, k)
                        cost_h = tmp_square.cost
                        # 以cost_h为键，交换方案为值，可能会有多个方案的cost_h相同的情况，但字典中只记录一个
                        self.swap_record[cost_h] = [i, j]
            m = min(self.swap_record)  # 找到最小的代价
            self.swap_schedule = copy.deepcopy(self.swap_record[m])
            return self.swap_schedule # 返回最小代价对应的交换方案


# 归并函数，返回一趟归并的逆序对数
def merge(listA, tmpA, L, R, RightEnd):
    cnt = 0
    LeftEnd = R-1  # 左半个数组最后一个元素的下标
    tmp = L
    NumElements = RightEnd-L+1  # 待归并数组元素总数
    while (L <= LeftEnd) and (R <= RightEnd):
        if listA[L] <= listA[R]:
            tmpA[tmp] = listA[L]
            tmp += 1
            L += 1
        else:
            tmpA[tmp] = listA[R]
            tmp += 1
            R += 1
            cnt += LeftEnd-L+1
    while L <= LeftEnd:
        tmpA[tmp] = listA[L]
        tmp += 1
        L += 1
    while R <= RightEnd:
        tmpA[tmp] = listA[R]
        tmp += 1
        R += 1
    for i in range(NumElements):
        listA[RightEnd] = tmpA[RightEnd]
        RightEnd -= 1
    return cnt


# 循环进行归并排序，返回以len为步长进行归并排序得到的逆序对数
def merge_pass(listA, tmpA, N, len):
    # 一趟归并（采用循环方法，非递归）
    cnt = 0
    double_len = 2*len
    i = 0
    while i <= N-double_len:
        cnt += merge(listA, tmpA, i, i+len, i+double_len-1)
        i += double_len
    if i + len < N:
        cnt += merge(listA, tmpA, i, i+len, N-1)
    else:
        for j in range(i, N):
            tmpA[j] = listA[j]
    return cnt


# 基于归并排序求列表中逆序对的数目
def inverse_number(listA, N):
    # 使用非递归的方法实现基于归并排序的逆序对数目计数
    len = 1
    cnt = 0
    tmpA = [0]
    tmpA = tmpA*N
    while len < N:
        cnt += merge_pass(listA, tmpA, N, len)
        len *= 2
        cnt += merge_pass(tmpA, listA, N, len)
        len *= 2
    return cnt


# 判断列表中逆序对数的奇偶，若为偶，返回True
# 计算逆序对数时，不算空白块
def Judge(listA):
    n = len(listA)
    # inverse_number函数会进行归并排序，破坏原列表，故先拷贝一份
    tmp = copy.deepcopy(listA)
    for i in range(n):
        if tmp[i] < 0:
            del tmp[i]
            n -= 1
            break
    cnt = inverse_number(tmp, n)
    if (cnt % 2) == 0:
        return True
    else:
        return False


# 将图片填充为正方形
def fill_image(image):
    width, height = image.size
    # 选取长和宽中较大值作为新图片的
    new_image_length = width if width > height else height
    # 生成新图片[白底]
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    # 将之前的图粘贴在新图上，居中
    if width > height:  # 原图宽大于高，则填充图片的竖直维度
        new_image.paste(image, (0, int((new_image_length - height) / 2)))  # (x,y)二元组表示粘贴上图相对下图的起始位置
    else:
        new_image.paste(image, (int((new_image_length - width) / 2), 0))
    return new_image


# 切图(n * n)
def cut_image(image, n):
    width, height = image.size
    item_width = int(width / n)
    box_list = []
    for i in range(0, n):
        for j in range(0, n):
            box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
            box_list.append(box)

    image_list = [image.crop(box) for box in box_list]

    return image_list  # 返回numpy矩阵列表


# 保存
def save_images(image_list, content):
    index = 0
    for image in image_list:
        image.save(content + '/' + str(index) + '.jpg', 'JPEG')
        index += 1

def original_partition(dir):
    dirs = './tiles'  # 当前目录下的tiles目录，用于存放所有原图的切片结果
    file_path1 = "original_img"  # 当前目录下的original_img文件夹
    file_path2 = dir + '.jpg'  # 输入original_img文件夹中的jpg文件全名（包括.jpg后缀）
    file_path = os.path.join(file_path1, file_path2)  # 组合成完整的源文件（待切片的图片）路径

    image = Image.open(file_path)  # 打开图片
    image = fill_image(image)  # 将图片填充为方形
    image_list = cut_image(image, 3)  # 切割图片（3*3）

    # 在tiles文件夹里再建一个文件夹，存放一张原图的所有切片，文件夹的名字与原图文件名（不包括后缀）一样
    dir_path = os.path.join(dirs, dir)  # 组合成完整的目标文件夹路径
    # 判断文件夹是否存在，若不存在则创建目标文件夹
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_images(image_list, dir_path)  # 保存切片结果

def img_match(img_base64):
    img = base64.b64decode(img_base64)  # base64编码转字符串
    img = BytesIO(img)  # 字符串转字节流
    pic = Image.open(img)  # 以图片形式打开img
    # 将读取的测试图片保存到本地，同目录下的chaos文件夹中，并命名为integral.jpg
    pic.save('./chaos/integral.jpg', 'JPEG')
    # 将原图切分为3*3片，存入img_list列表，并将切片保存到同目录./chaos/discrete文件夹中
    img_list = cut_image(pic, 3)
    save_images(img_list, './chaos/discrete')

    ls_chaos = []  # 存放乱序切片的numpy矩阵的列表
    for root, dirs, files in os.walk("./chaos/discrete"):  # 遍历discrete文件夹
        for file in files:  # 处理该文件夹里的所有文件
            p = Image.open(os.path.join(root, file))  # 合成绝对路径，并打开图像
            p = np.asarray(p)  # 图像转矩阵
            ls_chaos.append(p)  # 将得到的矩阵存入列表
            
    stat = [-1, -1, -1, -1, -1, -1, -1, -1, -1]  # 存放乱序图片的状态，-1代表白块，0~8代表该切片是处于原图中的哪一位置
    dir_path = "./tiles_300"
    # 遍历同目录中./tiles文件夹中的所有文件夹
    for root, dirs, files in os.walk(dir_path):
        for dir in dirs:
            # k代表状态列表下标，cnt记录当前已匹配上的切片数
            k, cnt = 0, 0
            # tar_stat列表存放目标状态，由于不同原图之间可能存在完全一样的切片，会影响tar_stat的最终结果
            # 因此每次与新的一张原图比较前，将tar_stat初始化为全-1
            tar_stat = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
            # 从ls_chaos列表（即乱序切片的numpy矩阵列表）中，逐个与原图库中的切片比较
            for i in ls_chaos:
                # index用于指示乱序的切片在原图的哪一位置
                index = 0
                # 遍历存放原图切片的文件夹中的所有文件（即，原图切片）
                for root, dirs, files in os.walk(os.path.join(dir_path, dir)):
                    for j in files:
                        # 用os.path.join()拼接出文件的绝对路径，然后打开该文件（图片）
                        j = Image.open(os.path.join(root, j))
                        j = np.asarray(j)  # 将原图切片转换为numpy矩阵
                        if (i == j).all():  # 判断两个矩阵是否完全相同
                            stat[k] = index
                            tar_stat[index] = index
                            cnt += 1
                            break
                        index += 1
                    k += 1
            # 若已有8个切片匹配上则说明匹配到了原图
            if cnt > 7:
                print("原图是:", dir)  # 打印原图名称
                break
    if cnt <8:
        print("没找到原图QAQ")
    # 遍历初始状态列表，获得白块的初始位置
    for i in range(len(stat)):
        if stat[i] < 0:
            blank = i
            break
    return stat, blank, tar_stat

# 使用get函数调用api接口获取数据
def get(url_):
    response = requests.get(url=url_)
    resp = json.loads(response.text)  # 从内存中加载字符串，并转换成字典类型
    return resp

# 使用post函数提交答案并返回测试结果
def post(url_, uuid, operations, swap):
    url = url_
    data = {"uuid":uuid,
            "answer":{
                "operations":operations,
                "swap":swap
            }}
    response = requests.post(url=url_, json=data)
    resp = json.loads(response.text)
    return resp


if __name__ == '__main__':
    url_get = "http://47.102.118.1:8089/api/problem?stuid=031802621"
    url_post = "http://47.102.118.1:8089/api/answer"
    resp_g = get(url_get)
    step_num = resp_g['step']  # 第几步进行强制交换
    swap_scheme = resp_g['swap']  # 强制交换最初方案
    # 题目中图片编号1~9，程序中为0~8，故调整一下调换图片的编号
    swap_scheme[0] -= 1
    swap_scheme[1] -= 1
    start, pos, end = img_match(resp_g['img'])
    solve = IDA(start, pos, end, step_num, swap_scheme)
    path = solve.IDA()
    solve.swap_scheme[0] += 1
    solve.swap_scheme[1] += 1
    resp_p = post(url_post, resp_g['uuid'], path, solve.swap_scheme)
    print(resp_p)#输出结果

