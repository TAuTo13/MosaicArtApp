import math
from MosaicArtModule.ImgModule import ImgItem,ImgCollection
from MosaicArtModule.Calculator.ImgDistBase import ImgDistCalculator

class LabCIDE2000(ImgDistCalculator):
    def __init__(self,unique:bool):
        self.unique = unique

        self._PI_2 = math.pi * 2
        self._V25_7 = 25 ** 7
        self._D6 = math.radians(6)
        self._D25 = math.radians(25)
        self._D30 = math.radians(30)
        self._D60 = math.radians(60)
        self._D63 = math.radians(63)
        self._D275 = math.radians(275)
        self._kl = 1
        self._kc = 1
        self._kh = 1
        self._MAX = self._calcDiff(0, 0, 0, 255, 255, 255)

    def _calcDist(self, p1:ImgItem, p2:ImgItem):
        return self._calcDiff(p1.Lab[0], p1.Lab[1], p1.Lab[2], p2.Lab[0], p2.Lab[1], p2.Lab[2])/self._MAX

    def _calcDiff(self, L1, a1, b1, L2, a2, b2):
        dld = L2 - L1
        lb = (L1 + L2) / 2

        cs1 = math.hypot(a1, b1)
        cs2 = math.hypot(a2, b2)
        cb = (cs1 + cs2) / 2
        cb7 = cb ** 7
        ad1 = a1 + a1 / 2 * (1 - math.sqrt(cb7 / (cb7 + self._V25_7)))
        ad2 = a2 + a2 / 2 * (1 - math.sqrt(cb7 / (cb7 + self._V25_7)))

        cd1 = math.hypot(ad1, b1)
        cd2 = math.hypot(ad2, b2)
        cbd = (cd1 + cd2) / 2
        cbd7 = cbd ** 7

        dcd = cd2 - cd1
        hd1 = 0 if ((b1 == 0) and (ad1 == 0)) else math.atan2(b1, ad1)
        if hd1 < 0:
            hd1 += self._PI_2
        hd2 = 0 if ((b2 == 0) and (ad2 == 0)) else math.atan2(b2, ad2)
        if hd2 < 0:
            hd2 += self._PI_2

        dhd = hd2 - hd1
        if (cd1 * cd2) == 0:
            dhd = 0
        elif abs(hd1 - hd2) > math.pi:
            if hd2 <= hd1:
                dhd += self._PI_2
            else:
                dhd -= self._PI_2

        dhhd = 2 * math.sqrt(cd1 * cd2) * math.sin(dhd / 2)
        hhbd = 0
        if (cd1 * cd2) != 0:
            hhbd = (hd1 + hd2 + self._PI_2) / \
                2 if (abs(hd1 - hd2) > math.pi) else (hd1 + hd2) / 2

        tt = 1 - 0.17 * math.cos(hhbd - self._D30) + 0.24 * math.cos(2 * hhbd) + \
            0.32 * math.cos(3 * hhbd + self._D6) - 0.20 * \
            math.cos(4 * hhbd - self._D63)
        lb50_2 = (lb - 50) ** 2
        ssl = 1 + (0.015 * lb50_2) / math.sqrt(20 + lb50_2)
        ssc = 1 + 0.045 * cbd
        ssh = 1 + 0.015 * cbd * tt
        rrt = -2.0 * math.sqrt(cbd7 / (cbd7 + self._V25_7)) * math.sin(
            self._D60 * math.exp(-((hhbd - self._D275) / self._D25)**2))
        de = ((dld / (self._kl * ssl)) ** 2) + ((dcd / (self._kc * ssc)) ** 2) + ((dhhd /
                                                                                 (self._kh * ssh)) ** 2) + (rrt * (dcd / (self._kc * ssc)) * (dhhd / (self._kh * ssh)))

        return math.sqrt(de)

    def _getNearestImgs(self, p: ImgItem, collection: ImgCollection):
        min = 999999999999
        nearest_img = None
        
        for img in collection:
            dist = self._calcDist(p, img)
            if dist < min:
                min = dist
                nearest_img = img

        return nearest_img

    def _getNearestImgsUnique(self, p: ImgItem, collection: ImgCollection):
        min = 999999999999
        nearest_img = None

        for img in collection:
                if not img.used:
                    dist = self._calcDist(p, img)
                    if dist < min:
                        min = dist
                        nearest_img = img
                        img.used = True

        return nearest_img

    def arrangeParts(self,src_parts:ImgCollection,parts_collection:ImgCollection):
        result_collection = ImgCollection()
        if self.unique:
            for img in src_parts: 
                item = self._getNearestImgsUnique(img, parts_collection)
                result_collection.add(item)
        else:
            for img in src_parts: 
                item = self._getNearestImgs(img, parts_collection)
                result_collection.add(item)

        return result_collection
