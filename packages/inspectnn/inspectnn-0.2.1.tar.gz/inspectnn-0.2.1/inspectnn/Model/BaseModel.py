import time,sys,imp,os
#import pandas 
from numba import cuda
import numpy as np
from progressbar import ProgressBar

class Multiply():
    def __init__(self,m,Area,Power):
        self.multiplier = m
        self.Power = Power/65536.0#per moltiplicazione
        self.Area  = Area

class BaseModel():
    def __init__(self, multiplier,quant_nbits = 8,input_shape=[28, 28, 1],save_csv_path=''):
        
        self.quant_nbits = quant_nbits
        self.input_shape = input_shape
        self.elapsed_time = 0
        self.total_elapsed_time=0
        self.save_csv_path=save_csv_path
        self.images_on_gpu = False
        if None != multiplier:
            self.exact_multiplier = multiplier
        else:#Moltiplicatore di base
            dim = 128
           
            self.def_multiplier = np.zeros((2*dim,2*dim),dtype=int)
            for i in range(-dim,dim):
                for j in range(-dim,dim):
                    self.def_multiplier[i+dim,j+dim]=i*j   
            
            self.exact_multiplier = Multiply(cuda.to_device(self.def_multiplier),729.8,0.425)
        self.net = None
         
    def evaluate(self,images,labels,log=False):
        num_of_samples=len(images)
        if log : 
            print(f"Testing on {len(images)} images.")
        st = time.time()
        if self.images_on_gpu:
            Accuracy = self.net.evaluate_accuracy(self.labels, self.images)
        else:
            Accuracy = self.net.evaluate_accuracy(labels, images)
        if log :
            print(f"Accuracy: {Accuracy}")
        et = time.time()
        self.elapsed_time = et - st
        self.total_elapsed_time+=self.elapsed_time
        if log :
            print('MIMT execution time:', self.elapsed_time, 'seconds')
            print('FPS:', num_of_samples/self.elapsed_time) 
            self.net.print_time_statics()
        return Accuracy
    
   
    def evaluate_baseline_accuracy(self,images_apx,labels_apx):
        self.net.update_multipler([self.exact_multiplier])
        self.baseline_accuracy = self.evaluate(images_apx, labels_apx)

    def evaluate_all(self,images_apx,labels_apx):
        results = []
        bar = ProgressBar(max_value = len(self.all_multiplier))
        bar.update(0)
        idx=0
        for multiplier in self.all_multiplier:
            idx+=1
            self.net.update_multipler([multiplier])
            accuracy = self.evaluate(images_apx, labels_apx)
            Power = self.net.return_Power()
            results.append([multiplier.name, Power,accuracy, self.baseline_accuracy - accuracy, self.elapsed_time])
            bar.update(idx)
        return results
    

    def load_all_multiply_for_layer(self,configuration):
        self.all_multiplier = []
        net = self.net
        
        idx=0
        vector_list_mul_data = configuration["axmuls"]
        for  list_mul_data in vector_list_mul_data:

            for mul_data in list_mul_data:
                multiplier, _ = self._load_multiplier(mul_data["path"])
                multiplier.name=mul_data["name"]
                
                multiplier.MAE   =mul_data['MAE']
                multiplier.AWCE  =mul_data['AWCE']
                multiplier.MRE   =mul_data['MRE']
                multiplier.Power =mul_data['power']/65536.0#per moltiplicazione
                multiplier.Area  =mul_data['area']

                self.all_multiplier.append(multiplier)
                
        
        
        return self.all_multiplier
    
    def load_all_multiply(self,approxmults_path,filter=None):
        self.all_multiplier = []
        
        for root, dirs, files in os.walk(approxmults_path):
            for f in files:
                if f.endswith('.py') and ((filter is not None and filter in f) or filter is None):
                    py_filename = os.path.join(root, f)
                    multiplier, _ = self._load_multiplier(py_filename)
                    multiplier.filename=py_filename.split('/')[-2]
                    self.all_multiplier.append(multiplier)
        
        return self.all_multiplier
                   
    
    def _import_module(self,module_name):
        # Fast path: see if the module has already been imported.
        try:
            return sys.modules[module_name]
        except KeyError:
            pass
        # If any of the following calls raises an exception,
        # there's a problem we can't handle -- let the caller handle it.
        fp, pathname, description = imp.find_module(module_name)
        try:
            return imp.load_module(module_name, fp, pathname, description)    
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()


    def _load_multiplier(self,filename):
        module_name = os.path.basename(filename)
        name_class = os.path.splitext(module_name)[0]
        name_import = os.path.splitext(filename)[0]
        module_name = self._import_module(name_import)
        variant_mul = getattr(module_name, name_class)
        mult_class = variant_mul()
        mult_class.multiplier = cuda.to_device(np.array(mult_class.model,dtype=int))
        return mult_class, name_class
    


    


    # def load_multiply_info(self,file_name='examples/ApproxData/EvoApproxLite_info.csv'):
    #     df = pandas.read_csv(file_name,sep=';')
    #     print(df) 
        
    #     for idx in range(len(self.all_multiplier)):
    #         self.all_multiplier[idx].MAE   =df['MAE'][idx]
    #         self.all_multiplier[idx].AWCE  =df['AWCE'][idx]
    #         self.all_multiplier[idx].MRE   =df['MRE'][idx]
    #         self.all_multiplier[idx].Power =df['Power(mW)'][idx]/65536.0#per moltiplicazione
    #         self.all_multiplier[idx].Area  =df['Area(um^2)'][idx]

    def load_img_gpu(self,images,labels):
        self.images_on_gpu=True
        self.labels = labels
        self.images = []
        for i in range(len(images)):
            self.images.append(cuda.to_device(np.ascontiguousarray(images[i], dtype=np.int32)))
    
    def generate_multipler_list(self,id):
        multipler_list= []
        for i in id:
            multipler_list.append(self.all_multiplier[i])
        return multipler_list