import os
import cv2
import geoTransform
import preProcessing
import superResolution
from progress import Progress
from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from tkinter import messagebox
import threading
import queue
import time


class aeganApp(ttk.Frame):

    def __init__(self, app):
        super().__init__(app)
        self.grid(row= 0, column=0, padx=20, pady=10)
        
        # Variables
        self.clicked_ext = StringVar()
        self.clicked_geo = StringVar()
        self.clicked_model = StringVar()
        self.clicked_type = StringVar()
        self.filename = StringVar()
        self.file = ''
        self.model2x = 'Models/Model2x.h5'
        self.model4x = 'Models/Model4x.h5'

        # App UI
        file_label = ttk.Label(self,text="File")
        file_label.grid(row=1, column=0)
      
        filenameEntry = ttk.Entry(self,text="",textvariable= self.filename)
        filenameEntry.grid(row=1, column=1)

        button = ttk.Button(self,text="open",command = self.openFileDialog)
        button.grid(row=1, column=2)

        geo_lable = ttk.Label(self, text= "Geo Transformaton Information")
        geo_lable.grid(row=2, column=0)
 
        geo_inf = ttk.OptionMenu(self,self.clicked_geo,"Select", "Available","Not-Available")
        geo_inf.grid(row = 2,column= 1)

        type_lable = ttk.Label(self, text= "Type of Image Reshaping")
        type_lable.grid(row = 3,column= 0)

        type_reshape = ttk.OptionMenu(self,self.clicked_type, "Select", "Padding", "Cropping")
        type_reshape.grid(row = 3,column= 1)

        size_lable = ttk.Label(self, text= "Size of Output Image")
        size_lable.grid(row = 4,column= 0)

        size = ttk.OptionMenu(self,self.clicked_model, "Select", "2x", "4x")
        size.grid(row = 4,column= 1)

        submit = ttk.Button(self,text='Submit',command=  lambda: self.processFile())
        submit.grid(row=6, column=1)

    def openFileDialog(self):
        # For taking file path as input
        self.file  = filedialog.askopenfilename(filetypes=[("Image files", ".tif .png .jpg .jpeg")]);
        self.filename.set(self.file)


    def processFile(self):
        # Main Program
        inputs = [self.clicked_model.get(),self.clicked_type.get(),self.file]
        # Input checking
        if '' or 'Select' in inputs:
            messagebox.showerror("Error", "One or More than One fields are empty")
            return False
        
        # Progress bar creation in different thread
        progress_thread = Progress(self,row=10, column=0, columnspan=3)

        # Queues for multi-threadding
        super_res_que = queue.Queue()
        pre_process_que = queue.Queue()

        # Informations form dialogue box
        model = self.clicked_model.get()
        type_reshape = self.clicked_type.get()
        file_name = os.path.basename(self.file)
        file_path = self.file.replace(file_name,'')
        file_name = os.path.splitext(file_name)[0]
        file_ext = os.path.splitext(file_name)[1]

        # Output File Name
        if model == "2x":
            scale = 2
            out_file = file_path + file_name + '_output2x.' + file_ext
        else:
            scale = 4
            out_file = file_path + file_name + '_output4x.' + file_ext

        def img_reshape(preprossing_thread: threading.Thread,model_name):
            # This will wait for preporcessing to complete 
            while True:
                if pre_process_que.qsize() > 0:
                    if preprossing_thread.is_alive:
                        preprossing_thread.join()
                    img_prep = pre_process_que.get()
                    if type_reshape == "Cropping":
                        reshaping_thread = threading.Thread(target=pre_process.img_cropping,args=(img_prep,pre_process_que))
                        reshaping_thread.start()
                    else:
                        reshaping_thread = threading.Thread(target=pre_process.img_padding,args=(img_prep,pre_process_que))
                        reshaping_thread.start()
                    super_res(model_name,reshaping_thread)
                else:
                    time.sleep(1)

        if self.clicked_geo.get() == "Available":
            try:
                geo_inf = geoTransform.geoInf(self.file,scale)
                gt = geo_inf.geo_scaling()
            except:
                messagebox.showerror("Error", "Improper Geo-Reference")
                return False                

            def geo_ref(thread: threading.Thread):
                # Geo-Reference thread will wait for super resolution to complete and will execute after it
                while thread.is_alive:
                    try:
                        if super_res_que.qsize() > 0:
                            thread.join()
                            out_img_arr = super_res_que.get()
                            geo_inf.geo_out(out_file,out_img_arr,gt)
                            progress_thread.pb_stop()
                            messagebox.showinfo("Message", "Superresolution Successful!")
                            print('Successful!')
                        else:
                            time.sleep(5)
                    except:
                        messagebox.showerror("Error", "Problem while Geo-Referencing")
                        return False

            

            def super_res(model_name, reshaping_thread: threading.Thread):
                # Super resolution thread will wait for image reshapping to complete and will execute after it
                while reshaping_thread.is_alive:
                    try:
                        if pre_process_que.qsize() > 0:
                            reshaping_thread.join()
                            progress_thread.pb_text(text='Super-Resolution...')
                            img_reshape = pre_process_que.get()
                            super_res = superResolution.supRes(img_reshape,model_name)
                            if model_name == self.model2x:
                                super_res_thread = threading.Thread(target= super_res.super_resolution_2x,args=(progress_thread,super_res_que))
                                super_res_thread.start()
                                threading.Thread(target=geo_ref,args= (super_res_thread,)).start()
                            
                            if model_name == self.model4x:
                                super_res_thread = threading.Thread(target= super_res.super_resolution_4x,args=(progress_thread,super_res_que))
                                super_res_thread.start()
                                threading.Thread(target=geo_ref,args= (super_res_thread,)).start()
                        else:
                            time.sleep(5)
                    except:
                        messagebox.showerror("Error", "Problem while Super-Resolution")
                        return False

                    


            if model == "2x":
                progress_thread.pb_text(text='Processing...')
                pre_process = preProcessing.preProcess(self.file,128)
                pre_process_thread = threading.Thread(target=pre_process.img_processing,args=(pre_process_que,))
                pre_process_thread.start()
                threading.Thread(target= img_reshape, args=(pre_process_thread,self.model2x)).start()


            else:
                progress_thread.pb_text(text='Processing...')
                pre_process = preProcessing.preProcess(self.file,110)
                pre_process_thread = threading.Thread(target=pre_process.img_processing,args=(pre_process_que,))
                pre_process_thread.start()
                threading.Thread(target= img_reshape, args=(pre_process_thread,self.model4x)).start()

        # If Geo-Ref is not available
        else:

            def file_save(thread: threading.Thread):
                while thread.is_alive:
                    try:
                        if super_res_que.qsize() > 0:
                            thread.join()
                            out_img_arr = super_res_que.get()
                            cv2.imwrite(out_file, out_img_arr.reshape(out_img_arr.shape[0], out_img_arr.shape[1],1))
                            progress_thread.pb_stop()
                            messagebox.showinfo("Message", "Superresolution Successful!")
                            print('Successful!')
                        else:
                            time.sleep(5)
                    except:
                        messagebox.showerror("Error", "Problem while saving file")
                        return False

            def super_res(model_name, reshaping_thread: threading.Thread):
                while reshaping_thread.is_alive:
                    try:
                        if pre_process_que.qsize() > 0:
                            reshaping_thread.join()
                            progress_thread.pb_text(text='Super-Resolution...')
                            img_reshape = pre_process_que.get()
                            super_res = superResolution.supRes(img_reshape,model_name)
                            if model_name == self.model2x:
                                super_res_thread = threading.Thread(target= super_res.super_resolution_2x,args=(progress_thread,super_res_que))
                                super_res_thread.start()
                                threading.Thread(target=file_save,args= (super_res_thread,)).start()
                            
                            if model_name == self.model4x:
                                super_res_thread = threading.Thread(target= super_res.super_resolution_4x,args=(progress_thread,super_res_que))
                                super_res_thread.start()
                                threading.Thread(target=file_save,args= (super_res_thread,)).start()
                        else:
                            time.sleep(5)

                    except:
                        messagebox.showerror("Error", "Problem while Super-Resolution")
                        return False
                    


            if model == "2x":
                progress_thread.pb_text(text='Processing...')
                pre_process = preProcessing.preProcess(self.file,128)
                pre_process_thread = threading.Thread(target=pre_process.img_processing,args=(pre_process_que,))
                pre_process_thread.start()
                threading.Thread(target= img_reshape, args=(pre_process_thread,self.model2x)).start()


            else:
                progress_thread.pb_text(text='Processing...')
                pre_process = preProcessing.preProcess(self.file,110)
                pre_process_thread = threading.Thread(target=pre_process.img_processing,args=(pre_process_que,))
                pre_process_thread.start()
                threading.Thread(target= img_reshape, args=(pre_process_thread,self.model4x)).start()




if __name__ == '__main__':

    # Main APP 

    app  = Tk(className= 'AutoEnGAN App')

    photo = PhotoImage(file = 'App/icon.png')
  
    # Setting icon of window
    app.iconphoto(False, photo)

    app.geometry("525x230")

    app.title("Satellite Image Super Resolution")

    frame = aeganApp(app)

    app.mainloop()



