import glob
import cv2
import os

from MosaicArtModule.ImgModule import ImgItem,ImgCollection

class FileManager:
    def loadImgs(self, folderPath):
        if not os.path.exists(folderPath):
            os.mkdirs(folderPath)
        imgs = ImgCollection()
        files = glob.glob(os.path.join(folderPath,"*.png"))

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
        if not os.path.exists(name):
            os.mkdirs(path)
        src_path=os.path.join(path,name)
        print(src_path)

        try:
            im = cv2.imread(src_path)
        except cv2.error as e:
            print(e)

        img = ImgItem(im)

        return img

    def saveImg(self, img:ImgItem, path, name="result.png"):
        if not os.path.exists(path):
            os.mkdirs(path)
        save_path = os.path.join(path,name)

        print(save_path)
        try:
            cv2.imwrite(save_path,img.img)
        except cv2.error as e:
            print(e)
