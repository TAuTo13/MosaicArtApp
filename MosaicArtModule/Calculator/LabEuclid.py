from pyflann import FLANN
from MosaicArtModule.ImgModule import ImgItem, ImgCollection
from MosaicArtModule.Calculator.ImgDistBase import ImgDistCalculator


class LabEuclid(ImgDistCalculator):
		def __init__(self, unique: bool):
				#Not Supported unique parameter
				self.unique = unique
				self.flann = FLANN()
				pass

		def arrangeParts(self, src_parts: ImgCollection, parts_collection: ImgCollection):
			self.flann.build_index(parts_collection.Lab_array)

			result , _ = self.flann.nn_index(src_parts.Lab_array,num_neighbors = 5)

			result_collection = ImgCollection()

			for idx in result:
					result_collection.add(parts_collection[idx[0]])
			
			return result_collection

				