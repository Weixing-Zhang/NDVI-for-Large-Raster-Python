# Calculate NDVI for large remoted sensing images by Python

Acknowlegement:
* Script Created on May 3rd 2016</li>
* Author: Weixing Zhang</li>
* Purpose: Calculate NDVI for large images</li>
* python 2.76 or 3.7</li>
* Required modules: gdal, os.path, numpy, and argparse</li>


I thank Roger Veciana i Rovira for sharing his code about raster classification
Link:http://geoexamples.blogspot.com/2013/06/gdal-performance-raster-classification.html
I learned and gained a lot of help from Python community. Thank you!
I share this script mainly because back then, I could not find a easy-to-use Python script to
calculate NDVI for large RS images. I hope this script will save someone's time! 

- You can run it directly from the command line as such:
```sh
python2 NDVI_Python2.7.py -block 500 -redband 1 -NIRband 4 -i sample.tif -o sample_ndvi.tif
```

OR 

```sh
python3 NDVI_Python3.7.py -block 500 -redband 1 -NIRband 4 -i sample.tif -o sample_ndvi.tif
```

- You can customize your own parameters and input and output directory in the script as such:

```
block_size = 500                     # Size of processing block by pixel</li>
redband_num = 1                      # Order of red band in input raster</li>
NIRband_num = 4                      # Order of NIR band in input raster</li>
inputRaster_path = r"sample.tif"   # Direcotry of input</li>
outputRaster_path = r"sample_ndvi.tif" # Direcotry of output</li>
```
