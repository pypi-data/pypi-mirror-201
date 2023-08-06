"""Main module."""

import os, shutil
import numpy as np
from osgeo import gdal, osr

def ExportSubdatasets(path, hdf_file):
    
     opf_tif = os.path.join(path, 'GeoTiff')
     if os.path.exists(opf_tif):
          shutil.rmtree(opf_tif)
     os.makedirs(opf_tif)

     """   
    This function takes the folder path and the HDF file as input and exports individual layers to TIFF (named GeoTIFF)
    
    Parameters:
            path (str): Path to the folder containing the HDF file
            hdf_file (str): Name of the HDF file

    Returns:
            opf_tif (str): Path to the folder containing the exported TIFF files. The folder is named GeoTiff. The layers are not georeferenced.
    
    """

     inp_hdf = os.path.join(path, hdf_file)
     hdf_ds = gdal.Open(inp_hdf, gdal.GA_ReadOnly)
     subdatasets = hdf_ds.GetSubDatasets()
    
     for i in range(0, len(subdatasets)):
        subdataset_name = subdatasets[i][0]
        band_ds = gdal.Open(subdataset_name, gdal.GA_ReadOnly)
        band_path = os.path.join(opf_tif, 'band{0}.TIF'.format(i))
        if band_ds.RasterCount > 1:
            for j in range(1,band_ds.RasterCount + 1):
                band = band_ds.GetRasterBand(j)
                band_array = band.ReadAsArray()
        else:
            band_array = band_ds.ReadAsArray()
        
        out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                      band_ds.RasterXSize,
                                                      band_ds.RasterYSize,
                                                      1,
                                                      gdal.GDT_Float64,
                                                      ['COMPRESS=LZW', 'TILED=YES'])
        
        
        out_ds.SetGeoTransform(band_ds.GetGeoTransform())
        out_ds.SetProjection(band_ds.GetProjection())
        out_ds.GetRasterBand(1).WriteArray(band_array)
        out_ds.GetRasterBand(1).SetNoDataValue(-32768)
        
     out_ds = None
     
     return opf_tif

def metaInfo(path, hdf_file):

    """
    This function takes the folder path and the HDF file as input and returns the metadata of the HDF file.

    Parameters:
            path (str): Path to the folder containing the HDF file
            hdf_file (str): Name of the HDF file

    Returns:
           
            (ulx,  uly) (tuple): Upper left corner coordinates
            (urx, ury) (tuple): Upper right corner coordinates
            (brx, bry) (tuple): Lower right corner coordinates
            (blx, bly) (tuple): Lower left corner coordinates
            (sun_elev) (float): Sun elevation angle
    """
    
    inp = gdal.Open(os.path.join(path, hdf_file))
    meta = inp.GetMetadata()
    
    ulx, uly = float(meta['Upper Left Longitude']), float(meta['Upper Left Latitude'])
    urx, ury = float(meta['Upper Right Longitude']), float(meta['Upper Right Latitude'])
    blx, bly = float(meta['Lower Left Longitude']), float(meta['Lower Left Latitude'])
    brx, bry = float(meta['Lower Right Longitude']), float(meta['Lower Right Latitude'])
    
    sun_elev = float(meta['Sun Elevation Angle'])
    
    return (ulx,  uly), (urx, ury), (brx, bry), (blx, bly), (sun_elev)

def GetExtent(ds):
    
    """
    Return list of corner coordinates from a gdal Dataset 
    
    Parameters:
            ds (gdal.Dataset): A gdal Dataset [something like: ds = gdal.Open('path/to/file.tif')]

    Returns:
            ul, ur, lr, ll (tuple): Upper left, upper right, lower right, lower left corner coordinates
    
    """
    
    xmin, xpixel, _, ymax, _, ypixel = ds.GetGeoTransform()
    width, height = ds.RasterXSize, ds.RasterYSize
    xmax = xmin + width * xpixel
    ymin = ymax + height * ypixel

    return (xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)

def Georeference(inpf, gtif, meta, opf_ref):

    """
    This function takes the folder path and the GeoTIFF file as input and georeferences the GeoTIFF file.

    Parameters:
            inpf (str): Path to the folder containing the GeoTIFF file
            gtif (str): Name of the GeoTIFF file
            meta (tuple): Metadata of the HDF file. Returned by `metaInfo` function.
            opf_ref (str): Path to the folder containing the georeferenced GeoTIFF file. Inherited from `do_georef` function.

    Returns:
            None
    
    """
    
    inp_file = os.path.join(inpf, gtif)
    band_tif = gdal.Open(inp_file)
    ext = GetExtent(band_tif)
    
    ext_pos = [(abs(val[0]), abs(val[1])) for val in ext]

    out_file = os.path.join(opf_ref, os.path.basename(gtif).split('.')[0] + '_georef.TIF')
    shutil.copy(inp_file, out_file)
    ds = gdal.Open(out_file, gdal.GA_Update)
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326) 
    
    
    '''
    Enter the GCPs
    Format: [map x-coordinate(longitude)], [map y-coordinate (latitude)], [elevation],
    [image column index(x)], [image row index (y)]
    If map pixel is negative, multiply it with -1 to make positive since GDAL can't handle negative pixel position that well.
    
    '''
    
    gcps = [gdal.GCP(meta[0][0], meta[0][1], 0, ext_pos[0][0], ext_pos[0][1]), 
            gdal.GCP(meta[1][0], meta[1][1], 0, ext_pos[1][0], ext_pos[1][1]),
            gdal.GCP(meta[2][0], meta[2][1], 0, ext_pos[2][0], ext_pos[2][1]), 
            gdal.GCP(meta[3][0], meta[3][1], 0, ext_pos[3][0], ext_pos[3][1])]
    
    ds.SetGCPs(gcps, sr.ExportToWkt())
    ds = None
    
    return 'Done'

def do_georef(path, hdf_file, TIF = False, **output_options):

    """
    This function takes the folder path and the GeoTIFF files within it as input and georeferences the GeoTIFF file. If the GeoTIFF files are not extracted, it extracts them first. 

    Parameters:
            path (str): Path to the folder containing the HDF file
            hdf_file (str): Name of the HDF file
            TIF (bool, optional): Check if the GeoTIFF files are already extracted. Default: False
            **output_options (dict, optional): Dictionary containing the output options. 
                                              if `TIF = True`, provide the path to the folder containing the GeoTIFF files by using: `do_georef(path, meta, TIF = True, geo_tif = "path/to/geotiff/folder")`   
                                              opf_georef (str, optional): Path to the output folder containing the georeferenced GeoTIFF file.
                                                            Default: `path` + "Georeferenced". To set, use: `do_georef(path, meta, opf_georef = "path/to/folder")`          

    Returns:
            None
    """
    if TIF:

         if 'opf_georef' not in output_options:
             opf_georef = os.path.join(path, "Georeferenced")
             if os.path.exists(opf_georef):
                 shutil.rmtree(opf_georef)
             os.mkdir(opf_georef)

         else:
             opf_georef = output_options['opf_georef']
             if os.path.exists(opf_georef):
                 shutil.rmtree(opf_georef)
             os.mkdir(opf_georef)

         geo_tif = output_options['geo_tif']
         meta = metaInfo(path, hdf_file)
         original = os.listdir(geo_tif)
         gtif = list(filter(lambda x: x.endswith(("TIF", "tif", "img")), original))
         for tif in gtif:
              Georeference(geo_tif, tif, meta, opf_georef)

    else:
         if 'opf_georef' not in output_options:
             opf_georef = os.path.join(path, "Georeferenced")
             if os.path.exists(opf_georef):
                 shutil.rmtree(opf_georef)
             os.mkdir(opf_georef)

         else:
             opf_georef = output_options['opf_georef']
             if os.path.exists(opf_georef):
                 shutil.rmtree(opf_georef)
             os.mkdir(opf_georef)
    
         meta = metaInfo(path, hdf_file)
         opf_tif = ExportSubdatasets(path, hdf_file)
         
         original = os.listdir(opf_tif)
         gtif = list(filter(lambda x: x.endswith(("TIF", "tif", "img")), original))
         for tif in gtif:
              Georeference(opf_tif, tif, meta, opf_georef)
        
    return None