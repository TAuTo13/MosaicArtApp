import numpy as np
import math
import cv2

from MosaicArtModule.ImgModule import ImgItem,ImgCollection
from MosaicArtModule.Calculator.ImgDistBase import ImgDistCalculator
from MosaicArtModule.Calculator.LabCIDE2000 import LabCIDE2000
from MosaicArtModule.Calculator.LabEuclid import LabEuclid


class MosaicCreator:
    def __init__(self, parts_imgs: ImgCollection, calcMethod = "" , unique = False):
        self.parts_imgs = parts_imgs
        self.source = None
        self.unique = unique

        if calcMethod == "LabUQ":
            self._dist_calculator = LabEuclid(unique)
            print("Calculator LabEuclid has been selected.")
        elif calcMethod == "CIDE2000":
            self._dist_calculator = LabCIDE2000(unique)
            print("Calculator LabCIDE2000 has been selected.")
        else:
            self._dist_calculator = LabEuclid(unique)

    def selectCalcMethod(self,calcMethod):
        if calcMethod == "LabUQ":
            self._dist_calculator = LabEuclid(self.unique)
            print("Calculator LabEuclid has been selected.")
        elif calcMethod == "CIDE2000":
            self._dist_calculator = LabCIDE2000(self.unique)
            print("Calculator LabCIDE2000 has been selected.")
        else:
            self._dist_calculator = LabEuclid(self.unique)
        

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
        if self._dist_calculator is None:
            return

        self.parts_imgs.toarray()
        self.src_parts.toarray()
        
        self.m_parts = self._dist_calculator.arrangeParts(self.src_parts,self.parts_imgs)

        return self.m_parts

    def splitSourceParts(self):
        if self.source is None:
            print("Source is None.Put any Img.")
            return
        
        if type(self.source) is not ImgItem:
            print("Source is not ImgItem Type.")
            return

        self.src_parts = self.source.split(self.x_num, self.y_num)

        return self.src_parts
        

    def createMosaicArt(self):
        self.splitSourceParts()
        
        self.arrangeParts()

        self.generateMosaicArt()

        return self.mosaic_art_img
