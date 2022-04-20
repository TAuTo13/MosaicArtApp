# MosaicArtApp
Create MosaicArt from parts pictures in folder and an source picture.

# How To Use
Load folder for parts pictures and source picture.
```
import MosaicArtModule.FileManager as fm
fileManager = fm.FileManager()

#Parts is loaded as format ImgCollection.
#Input directoryPath
parts = fileManager.loadImgs("local/usr/mosaic/parts")

#source is loaded as format ImgItem.
#Input a source picture path and name.
src = fileManager.loadImg("local/usr/mosaic/srcImg","source.png")
```
