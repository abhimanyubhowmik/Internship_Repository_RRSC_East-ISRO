import rasterio
import numpy as np
from PIL import Image
import queue

class preProcess():
    def __init__(self, filename, patch_size) -> None:
        self.image = rasterio.open(filename).read()
        self.bands = self.image.shape[0]
        self.patch_size = patch_size

    def img_processing(self,queue: queue.Queue):
        '''Reading input image and extract all bands into single band'''
        img_list = []

        for i in range(self.bands):
            band_range = self.image[i].max() - self.image[i].min()

            if band_range != 0:
                img = ((self.image[i] - self.image[i].min()) * (1/(self.image[i].max() - self.image[i].min()) * 255))
                img_list.append(img/self.bands)
            
            else:
                self.bands -= 1
        
        full_image = np.stack(img_list, axis = self.bands - 1)
        full_image_1D = np.mean(full_image, axis=self.bands - 1)
        queue.put(full_image_1D)
    
    def img_cropping(self, image, queue: queue.Queue):
        '''Cropping image to nearest size divisible by patch size'''
        SIZE_X = (image.shape[1]//self.patch_size) * self.patch_size #Nearest size divisible by our patch size
        SIZE_Y = (image.shape[0]//self.patch_size)*self.patch_size #Nearest size divisible by our patch size
        crop_image = Image.fromarray(image[:,:])
        crop_image = crop_image.crop((0 ,0, SIZE_X, SIZE_Y)) #Crop from top left corner
        queue.put(np.array(crop_image))

    def img_padding(self, image, queue: queue.Queue):
        '''Padding image to nearest size divisible by patch size'''
        SIZE_X = (image.shape[1]//self.patch_size+1) * self.patch_size - image.shape[1] #Nearest padding size divisible by our patch size
        SIZE_Y = (image.shape[0]//self.patch_size+1)* self.patch_size - image.shape[0] #Nearest padding size divisible by our patch size
        pad_image = Image.fromarray(image[:,:])
        pad_image = np.pad(pad_image,((0,SIZE_Y),(0,SIZE_X)),'minimum') # Pad Right and Bottom sides
        queue.put(np.array(pad_image))

    

    

        






        




    

