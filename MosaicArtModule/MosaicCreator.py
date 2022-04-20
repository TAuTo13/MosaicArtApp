import numpy as np
import math
import cv2

from MosaicArtModule.ImgModule import ImgItem,ImgCollection
from MosaicArtModule.Calculator.ImgDistBase import ImgDistCalculator


class MosaicCreator:
    def __init__(self, parts_imgs: ImgCollection, calculator: ImgDistCalculator, unique = False):
        self.parts_imgs = parts_imgs
        self.source = None
        self._dist_calclator = calculator
        self.unique = unique

    def initialize(self,result_width,asp = (16,9), x_num = 100):
        src_ratio = self.source.w_h_ratio
        self.x_num = x_num
        self.y_num = math.ceil(x_num * src_ratio)

        parts_width = math.floor(result_width / x_num)
        parts_height = math.ceil(parts_width * src_ratio)

        self.parts_imgs.resize(asp,parts_width,parts_height)
        
    def _concatTile(self,img_list):
        return cv2.vconcat([cv2.hconcat(img_list_h) for img_list_h in img_list])

    def generateMosaicArt(self):
        m_parts_arranged=[]
        for y in range(self.y_num):
            x_list=[]
            for x in range(self.x_num):
                x_list.append(self.m_parts[y*self.x_num+x].img)
            m_parts_arranged.append(x_list)
        
        img_tile = self._concatTile(m_parts_arranged)

        self.mosaic_art_img = ImgItem(img_tile)

        return self.mosaic_art_img

    def arrangeParts(self):
        self.m_parts = ImgCollection()
        for img in self.src_parts: 
            item = self._dist_calclator.getNearestImgs(img, self.parts_imgs, self.unique)
            self.m_parts.add(item)

        return self.m_parts

    def splitSourceParts(self):
        if self.source is None:
            print("Source is None.Put any Img.")
            return
        elif self.source is not ImgItem:
            print("Source is not ImgItem Type.")
            return

        self.src_parts = self.source.split(self.x_num, self.y_num)
        self.src_parts.mean()

        return self.src_parts
        

    def createMosaicArt(self, result_width,asp=(16, 9), x_num=100):
        self.splitSourceParts()
        
        self.arrangeParts()

        self.generateMosaicArt()

        return self.mosaic_art_img
