
'''
Acknowlegement:
@ Script Created on May 3rd 2016
@ Author: Weixing Zhang
@ Purpose: Calculate NDVI for large image

@ >>>>>>>>>>>>>> Statement >>>>>>>>>>>>>>

First off, I have to thank Roger Veciana i Rovira for sharing his code about raster classification
           URL: http://geoexamples.blogspot.com/2013/06/gdal-performance-raster-classification.html
Secondly, I learned a lot and got tons of help from fantastic python community. Thank them as well.

I share this script because I am a simple and lazy guy and I can't find a easy-to-use Python script to
calculate NDVI for Large! Raster! Data! I was angry, since I had to do it! I hope this script can save
someone's time! 
'''

#  Instruction below was implementd based on Windows



### Step 1: Install gdal module      download from >>>> http://www.lfd.uci.edu/~gohlke/pythonlibs/
#   (1) Download gdal if you don't have it installed.
#   (2) After download gdal.whl, open your command prompt, type "cd Downloads", then hit "Enter"
#   (3) type "pip install xxxx.whl", then "Enter"

# import required modules
import os.path
import gdal
from gdalconst import *
import numpy as np



### Step 2: set file path
#   (1) Specify paths of the input and output raster 
#   (2) Specify names of the input and output raster 
#   (3) You have to know 

# set folder path
inroot = r'C:\Users\xing\Google Drive\00_Reaserch\05_LanduseClassification\02_Data\NYC\StudyArea_01\areial images'
outroot = r'E:\New folder'

# set input and output tiff name
inputRaster_name = 'studyarea_aerial_mosaic_cliped_18N_1m.tif'
outputRaster_name = 'studyarea_aerial_mosaic_cliped_18N_1m_NDVI.tif'

# specify order of red band in input raster
redband_num = 1

# specify order of near-infrared band in input raster
NIRband_num = 4



### Step 3: Run this script, then you are done 


'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

From below on, only for people who would be interested more about python using in raster processing
For others, just ignore them

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''





















# input raster
inputRaster_path = os.path.join(inroot, inputRaster_name)
outputRaster_path = os.path.join(outroot, outputRaster_name)

# read input rows, cols, and bands of raster
ds = gdal.Open(inputRaster_path, GA_ReadOnly)
nrows = ds.RasterYSize
ncols = ds.RasterXSize
nbands = ds.RasterCount

# read as raster 
redband_raster = ds.GetRasterBand(redband_num)
nirband_raster = ds.GetRasterBand(NIRband_num)

# set up block size as 500 pixels, you can actually set an larger number if your ram is big enough
block_size = 500

# set up output parameters
format = "GTiff"  
driver = gdal.GetDriverByName(format)  
dst_ds = driver.Create(outputRaster_path, ncols, nrows, 1, gdal.GDT_Float32)  
dst_ds.SetGeoTransform(ds.GetGeoTransform())  
dst_ds.SetProjection(ds.GetProjection())  

# segment rows and cols
y_block_size = int(np.ceil(nrows/float(block_size)))
x_block_size = int(np.ceil(ncols/float(block_size)))
ysize = nrows
xsize = ncols

# read row
for i in xrange(0, ysize, block_size):

    # don't want moving window to be larger than row size of input raster
    if i + block_size < ysize:  
        rows = block_size  
    else:  
        rows = ysize - i
        
    # read col      
    for j in xrange(0, xsize, block_size):

        # don't want moving window to be larger than col size of input raster
        if j + block_size < xsize:  
            cols = block_size  
        else:  
            cols = xsize - j 
        
        # get block out of the whole raster
        red_array = redband_raster.ReadAsArray(j, i, cols, rows) 
        nir_array = nirband_raster.ReadAsArray(j, i, cols, rows)

        # avoid zero situation even it won't happen commonly
        nir_array = nir_array+0.01

        # calculate NDVI
        ndvi = (nir_array - red_array) / (nir_array + red_array) 

        # write ndvi array to tiff file
        dst_ds.GetRasterBand(1).WriteArray(ndvi, j, i) 
            
# ends program
dst_ds = None  
print 'Program ends'
