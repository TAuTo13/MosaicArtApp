import glob
import cv2
import os
import re

from MosaicArtModule.ImgModule import ImgItem,ImgCollection

class FileManager:
    def loadImgs(self, folderPath):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        imgs = ImgCollection()
        files = [p for p in glob.glob(os.path.join(folderPath,"*")) if re.search("/*\.(jpeg|jpg|png|bmp|webp)",p)]

        for file in files:
            print(file)

            try:
                im = cv2.imread(file)
            except cv2.error as e:
                print(e)
            
            img = ImgItem(im)
            imgs.add(img)

        return imgs

    def loadImg(self, path, name):
        src_path=os.path.join(path,name)
        if not os.path.exists(path):
            print("path "+ path +" does not exist")
            return
        print(src_path)

        try:
            im = cv2.imread(src_path)
        except cv2.error as e:
            print(e)

        img = ImgItem(im)

        return img

    def saveImg(self, img:ImgItem, path, name="result.png"):
        if not os.path.exists(path):
            os.makedirs(path)
        save_path = os.path.join(path,name)

        print(save_path)
        try:
            cv2.imwrite(save_path,img.img)
        except cv2.error as e:
            print(e)
