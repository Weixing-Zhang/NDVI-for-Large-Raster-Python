"""
Acknowlegement:
@ Script Created on May 3rd 2016
@ Author: Weixing Zhang
@ Purpose: Calculate NDVI for large images
@ python 2.76
@ Required modules: gdal, os.path, numpy, and argparse

I thank Roger Veciana i Rovira for sharing his code about raster classification
Link:http://geoexamples.blogspot.com/2013/06/gdal-performance-raster-classification.html
I learned and gained a lot of help from Python community. Thank you!
I share this script mainly because back then, I could not find a easy-to-use Python script to
calculate NDVI for large RS images. I hope this script will save someone's time! 

Prerequirement
Install gdal module
(1) Download gdal if you don't have it installed on your Machine (http://www.lfd.uci.edu/~gohlke/pythonlibs/)
(2) After downloaded gdal.whl, open your command prompt, type "cd /Downloads directory"
(3) type "pip install xxxx.whl"
"""

# import required modules
import os.path
import gdal
from gdalconst import *
import numpy as np

"""
COMMANDLINE: 
python NDVI.py -block 500 -redband 1 -NIRband 4 -i sample.tif -o sample_ndvi.tif
"""

if __name__ == '__main__':
    # ___________________________Arguments___________________________
    import argparse
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Calculate NDVI for large images.')

    parser.add_argument('-block', required=True,
                        help='Size of processing block by pixel')

    parser.add_argument('-redband', required=True,
                        help='Order of red band in input raster dataset')

    parser.add_argument('-NIRband', required=True,
                        help='Order of NIR band in input raster dataset')

    parser.add_argument('-i', required=True,
                        help='Directory of input raster dataset')

    parser.add_argument('-o', required=True,
                        help='Directory of output raster dataset')
    args = parser.parse_args()

    # other parameters
    block_size = int(args.block)     # Size of processing block by pixel
    redband_num = int(args.redband)  # Order of red band in input raster
    NIRband_num = int(args.NIRband)  # Order of NIR band in input raster

    # direcotries of input and output rasters 
    inputRaster_path = args.i        # Direcotry of input
    outputRaster_path = args.o       # Direcotry of output

    """
    Or you can make your own parameters and input and output directory
    For example:
    block_size = 500
    redband_num = 1
    NIRband_num = 4

    inputRaster_path = r"sample.tif"
    outputRaster_path = r"sample_ndvi.tif"
    """

    # _______________________________________________________________
    # read input rows, cols, and bands of raster
    ds = gdal.Open(inputRaster_path, GA_ReadOnly)
    ysize = ds.RasterYSize
    xsize = ds.RasterXSize
    nbands = ds.RasterCount

    # read as raster 
    redband_raster = ds.GetRasterBand(redband_num)
    nirband_raster = ds.GetRasterBand(NIRband_num)

    # output parameters
    format = "GTiff"  
    driver = gdal.GetDriverByName(format)
    dst_ds = driver.Create(outputRaster_path, xsize, ysize, 1, gdal.GDT_Float32)  
    dst_ds.SetGeoTransform(ds.GetGeoTransform())  
    dst_ds.SetProjection(ds.GetProjection())  

    # process image in a manners of block by block
    for i in xrange(0, ysize, block_size):

        # prevent moving window from being larger than row size of input raster
        rows = block_size if i + block_size < ysize else ysize - i
            
        # read col      
        for j in xrange(0, xsize, block_size):

            # prevent moving window from being larger than col size of input raster
            cols = block_size if j + block_size < xsize else xsize - j

            # extract block out of the whole raster
            red_array = redband_raster.ReadAsArray(j, i, cols, rows) 
            nir_array = nirband_raster.ReadAsArray(j, i, cols, rows)

            # avoid zero situation
            nir_array = nir_array+0.00001

            # calculate NDVI
            ndvi_array = (nir_array - red_array) / (nir_array + red_array) 

            # write ndvi array into output .tiff file
            dst_ds.GetRasterBand(1).WriteArray(ndvi_array, j, i) 
                
    # program ends
    dst_ds = None