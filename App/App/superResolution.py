import numpy as np
import tensorflow as tf
from skimage import exposure
from keras.models import load_model
from patchify import patchify, unpatchify


class supRes():
    def __init__(self,image,model_path) -> None:
        self.image = image
        self.patch_size = 110
        self.total_patch_size = 128
        self.border = int((self.total_patch_size - self.patch_size)/2)
        self.model = load_model(model_path, compile=False)
        self.patches_img = patchify(self.image, (self.patch_size, self.patch_size), step= (self.patch_size)) 
        self.patches_img_2x = patchify(self.image, (self.total_patch_size, self.total_patch_size), step= (self.total_patch_size)) 

    def log_transformed(self,image):
        '''Log Transfoormation of matrix'''
        c = 255/(np.log(1 + np.max(image)))
        log_transformed = c * np.log(1 + image)

        # Specify the data type.
        log_transformed = np.array(log_transformed, dtype = np.uint8)
        return log_transformed
    
    def super_resolution_4x(self,progress_thread,queue):
        '''4x Super Resolution of Image'''
        patched_prediction = []

        #For Progressbar
        total_patches = self.patches_img.shape[0]*self.patches_img.shape[1]
        count = 1

        for i in range(self.patches_img.shape[0]):
            for j in range(self.patches_img.shape[1]):

                # Log Transformation and Reshaping for porcessing
                single_patch_img = self.patches_img[i,j,:,:]
                single_patch_img = self.log_transformed(single_patch_img)
                single_patch_img = np.pad(single_patch_img, ((self.border, self.border), (self.border, self.border)), 'edge')
                single_patch_img = single_patch_img.reshape(1,self.total_patch_size, self.total_patch_size)

                # Output Generation
                pred = self.model.predict(single_patch_img)

                # Reshaping
                ref = self.patches_img[i,j,:,:].reshape(1,self.patch_size,self.patch_size,1)

                # Exposure Matching
                multi = True if pred.shape[-1] > 1 else False
                matched = exposure.match_histograms(pred, ref, multichannel=multi)
                
                # Matched Output list
                patched_prediction.append(matched[:,31:471,32:472,:])

                # Update Progressbar
                percent_completed = np.round((count / total_patches) * 100,2)
                progress_thread.pb_text(text=f"Current Progress: {percent_completed}%")
                progress_thread.pb_value(percent_completed)

                count += 1

        progress_thread.pb_text(text="Combining Patches...")
        
        # Reshaping patched prediction list
        patched_prediction = np.reshape(patched_prediction, [self.patches_img.shape[0], self.patches_img.shape[1], 
                                            (self.total_patch_size - self.border*2)*4, (self.total_patch_size - self.border*2)*4])
        
        # Combining all outputs
        unpatched_prediction = unpatchify(patched_prediction, (self.image.shape[0]*4, self.image.shape[1]*4))
        # Update into queue
        queue.put(unpatched_prediction)

    def super_resolution_2x(self,progress_thread,queue):
        '''2x Super Resolution of Image'''
        patched_prediction = []

        #For Progressbar
        total_patches = self.patches_img_2x.shape[0]*self.patches_img_2x.shape[1]
        count = 1


        for i in range(self.patches_img_2x.shape[0]):
            for j in range(self.patches_img_2x.shape[1]):

                # Log Transformation and Reshaping for porcessing
                single_patch_img = self.patches_img_2x[i,j,:,:]
                single_patch_img = self.log_transformed(single_patch_img)
                single_patch_img = single_patch_img.reshape(1,self.total_patch_size, self.total_patch_size)

                # Output Generation
                pred = self.model.predict(single_patch_img)

                # Reshaping
                ref = self.patches_img_2x[i,j,:,:].reshape(1,self.total_patch_size,self.total_patch_size,1)

                # Exposure Matching
                multi = True if pred.shape[-1] > 1 else False
                matched = exposure.match_histograms(pred, ref, multichannel=multi)
                
                # Matched Output list
                patched_prediction.append(matched)

                # Update Progressbar
                percent_completed = np.round((count / total_patches) * 100,2)
                progress_thread.pb_text(text=f"Current Progress: {percent_completed}%")
                progress_thread.pb_value(percent_completed)

                count += 1
        

        progress_thread.pb_text(text="Combining Patches...")

        # Reshaping patched prediction list
        patched_prediction = np.reshape(patched_prediction, [self.patches_img_2x.shape[0], self.patches_img_2x.shape[1], 
                                            self.patches_img_2x.shape[2]*2, self.patches_img_2x.shape[3]*2])
        
        # Combining all outputs
        unpatched_prediction = unpatchify(patched_prediction, (self.image.shape[0]*2, self.image.shape[1]*2 ))
        # Update into queue
        queue.put(unpatched_prediction)


    
