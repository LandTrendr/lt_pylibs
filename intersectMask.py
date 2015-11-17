
import docopt, gdal, os, sys
from gdalconst import *
import numpy as np
from lthacks import *
from datetime import datetime
import getpass

def GetExtent(gt,cols,rows):
    ''' Returns list of corner coordinates from a geotransform &  number of columns+rows'''
    ext=[]
    xarr=[0,cols]
    yarr=[0,rows]

    for px in xarr:
        for py in yarr:
            x=gt[0]+(px*gt[1])+(py*gt[2])
            y=gt[3]+(px*gt[4])+(py*gt[5])
            ext.append([x,y])
        yarr.reverse()
    return ext

def findLeastCommonBoundaries(listOfMaps):
    '''Determine least common extent from a list of maps'''

    #extract corner coordinate info from all masks
    corners = np.zeros((len(listOfMaps), 4, 2))
    projections = []
    drivers = []
    pixelSizes = np.zeros((len(listOfMaps), 2))
    for ind,mask in enumerate(listOfMaps):
        src = gdal.Open(mask, GA_ReadOnly)
        projection = src.GetProjection()
        driver = src.GetDriver()
        transform = src.GetGeoTransform()
        cols = src.RasterXSize
        rows = src.RasterYSize
        corners[ind] = GetExtent(transform, cols, rows)
        projections.append(projection)
        drivers.append(driver)
        pixelSizes[ind] = (transform[1], transform[5])

    #define number of columns & rows for final mask
    upperLeftX = np.max(corners[:, 0, 0])
    upperLeftY = np.min(corners[:, 0, 1])
    lowerRightX = np.min(corners[:, 2, 0])
    lowerRightY = np.max(corners[:, 2, 1])
    pixSizeX = pixelSizes[np.argmin(np.abs(pixelSizes), axis=0)[0],0]
    pixSizeY = pixelSizes[np.argmin(np.abs(pixelSizes), axis=0)[1],1]
    numCols = abs((upperLeftX - lowerRightX)/abs(pixSizeX))
    numRows = abs((lowerRightY - upperLeftY)/abs(pixSizeY))
    finalSize = (numCols, numRows)

    #define transform for final mask
    finalTransform = (upperLeftX, pixSizeX, 0.0, upperLeftY, 0.0, pixSizeY)

    return finalSize, finalTransform, projection, driver

def transformToCenter(transform, cols, rows):
    '''Returns center pixel coordinates based on transform and number of columns&rows'''
    upperLeftX = transform[0]
    upperLeftY = transform[3]
    pixSizeX = transform[1]
    pixSizeY = transform[5]

    centerX = upperLeftX + pixSizeX*(cols/2.)
    centerY = upperLeftY + pixSizeY*(rows/2.)

    return (centerX, centerY)

def maskAsArray(sourcePath, maskPath, src_band=1, msk_band=1, msk_value=None, out_value=None):
    '''masks out pixels in a source raster according to 0 pixels in mask raster, outputs numpy array'''

    #calculate boundary coordinates using least common pixels of mask & source
    finalSize, finalTransform, projection, driver = findLeastCommonBoundaries([sourcePath, maskPath])
    cols = int(finalSize[0])
    rows = int(finalSize[1])
    (midx, midy) = transformToCenter(finalTransform, cols, rows)

    #extract source array & get nodata value + datatype
    src = gdal.Open(sourcePath, GA_ReadOnly)
    srcTransform = src.GetGeoTransform()
    srcBandArray = extract_kernel(src, midx, midy, cols, rows, src_band, srcTransform)
    srcBand = src.GetRasterBand(src_band)
    nodata = srcBand.GetNoDataValue()
    datatype = srcBand.DataType

    #extract mask array
    msk = gdal.Open(maskPath, GA_ReadOnly)
    mskTransform = msk.GetGeoTransform()
    mskBandArray = extract_kernel(msk, midx, midy, cols, rows, msk_band, mskTransform)

    #ensure mask is of 0's & 1's, then multiply source & mask
    if not msk_value:
        #use all non-zero's if msk_value not specified
        mask = (mskBandArray!=0)
    else:
    	mask = (mskBandArray==msk_value)
    
    if not out_value:
    	outBandArray = mask * srcBandArray
    else:
    	outBandArray = srcBandArray
    	outBandArray[mask==0] = out_value


    return outBandArray, finalTransform, projection, driver, nodata, datatype

def saveArrayAsRaster(outBandArray, transform, projection, driver, outPath, datatype, nodata=None):
    '''saves a numpy array as a new raster'''
    print "\nSaving raster..."
    (rows,cols) = outBandArray.shape
    #save new raster
    out = driver.Create(outPath, cols, rows, 1, datatype)
    if out is None:
        print sys.exit('\nCould not create ' + outPath)
    #write the data
    outBand = out.GetRasterBand(1)
    outBand.WriteArray(outBandArray)
    #flush data to disk
    outBand.FlushCache()
    if nodata: outBand.SetNoDataValue(nodata)

    #georeference the image and set the projection
    out.SetGeoTransform(transform)
    out.SetProjection(projection)
    print "\n Done! \nNew raster available here:", outPath

def saveArrayAsRaster_multiband(outbands, transform, projection, driver, outPath, datatype, nodata=None):
    '''saves a numpy array as a new raster'''
    print "\nSaving raster..."
    (rows,cols) = outbands[0].shape
    #save new raster
    numbands = len(outbands)
    out = driver.Create(outPath, cols, rows, numbands, datatype)
    if out is None:
        print sys.exit('\nCould not create ' + outPath)
    #write the data
    for ind,i in enumerate(outbands):
        band = ind + 1
        outBand = out.GetRasterBand(band)
        outBand.WriteArray(i)
        #flush data to disk
        outBand.FlushCache()
        if nodata: outBand.SetNoDataValue(nodata)

    #georeference the image and set the projection
    out.SetGeoTransform(transform)
    out.SetProjection(projection)
    print "\n Done! \nNew raster available here:", outPath





