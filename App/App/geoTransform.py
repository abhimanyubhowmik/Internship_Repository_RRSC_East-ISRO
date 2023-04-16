from osgeo import gdal
import numpy as np


class geoInf():
    def __init__(self,filepath,scale) -> None:
        self.path = filepath
        self.scale = scale
        self.out_bands = 1
        self.ds = gdal.Open(self.path)
        self.gt = self.ds.GetGeoTransform()
        self.proj = self.ds.GetProjection()
    
    def geo_scaling(self):
        '''Scaling Geo informations as per scaling factor'''
        x_origin = self.gt[0]
        y_origin = self.gt[3]
        x_px = self.gt[1]
        y_px = self.gt[5]
        x_rot = self.gt[2]
        y_rot = self.gt[4]
        return (x_origin,x_px/self.scale,x_rot,y_origin,y_rot,y_px/self.scale)    

    def geo_out(self, path, img_array, gt, dtype = gdal.GDT_Float32 ):
        '''Return geo transformed output with projection and transformation informations'''
        rows,cols = img_array.shape
        # Initialize driver & create file
        driver = gdal.GetDriverByName("GTiff")
        dataset_out = driver.Create(path, cols, rows, 1, dtype)
        dataset_out.SetGeoTransform(gt)
        dataset_out.SetProjection(self.proj)
        # Write file to disk
        dataset_out.GetRasterBand(1).WriteArray(img_array)
        dataset_out = None
        