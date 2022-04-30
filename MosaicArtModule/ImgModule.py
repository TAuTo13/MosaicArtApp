import cv2
import math
import numpy as np


class ImgItem:
    def __init__(self, img):
        self.img = img
        self._initialize()

    def _initialize(self):
        self.height, self.width, c = self.img.shape
        self.w_h_ratio = self.height / self.width
        self.used = False
        img_Lab = cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)
        l,a,b = cv2.split(img_Lab)
        self.Lab = [np.mean(l),np.mean(a),np.mean(b)]


    def resizeAsp(self, asp):
        width = math.ceil(self.width * asp)
        height = math.ceil(self.height * asp)
        print(asp,width,height)
        self.img = cv2.resize(self.img,(width, height))

        self._initialize()

    def resize(self, width, height):
        self.img = cv2.resize(self.img, (width, height))

        self._initialize()

    def resizeForWidth(self, width):
        asp = width/self.width
        self.resizeAsp(asp)

    def resizeForHeight(self, height):
        asp = height/self.height
        self.resizeAsp(asp)

    def trim(self, asp=(16, 9)):
        height = int(self.width/asp[0] * asp[1])
        width = int(self.height/asp[1] * asp[0])

        if height < self.height:
            top = int((self.height-height)/2)
            left = 0
            bottom = top + height
            right = self.width
        elif width < self.width:
            top = 0
            left = int((self.width-width)/2)
            bottom = self.height
            right = left + width
        else:
            return

        self.img = self.img[top:bottom,left:right,:]
        self._initialize()

    def split(self,x_num,y_num):
        parts = ImgCollection()
        
        dy = self.height/y_num
        dx = self.width/x_num
        h = math.ceil(dy)
        w = math.ceil(dx)

        for i in range(y_num):
            py = math.floor(dx*i)
            for j in range(x_num):
                px = math.floor(dx*j)
                img = ImgItem(self.img[py:py+h,px:px+w,:])
                parts.add(img)
        
        return parts

class ImgCollection:
    def __init__(self):
        self.imgs = []
        self.count = 0

    def __iter__(self):
        yield from self.imgs

    def __getitem__(self,i):
        return self.imgs[i]

    def toarray(self):
        array = []
        for img in self.imgs:
            array.append(img.Lab)
            
        self.Lab_array=np.asarray(array)

        return self.Lab_array

    def add(self, item: ImgItem):
        self.imgs.append(item)
        self.count += 1

    def resize(self, asp=(16, 9), width = 30, height = 20):    
        for img in self.imgs:
            img.trim(asp)
            img.resize(width,height)
