import time
from numba import cuda
import numpy as np
from inspectnn.Model.BaseModel import BaseModel
class BaseModel_tflite(BaseModel):
    def __init__(self, multiplier,quant_nbits = 8,input_shape=[28, 28, 1],save_csv_path=''):
        
        super().__init__(multiplier,quant_nbits,input_shape,save_csv_path)

        self.elapsed_time = 0
        #self.interpreter = []
        self.total_elapsed_time=0
        self.baseline_accuracy = None
        
        self.net = None
         
    def evaluate2(self,images,labels,log=False):
        num_of_samples=len(images)
        if log : 
            print(f"Testing on {len(images)} images.")
        st = time.time()
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
    

    def evaluate_tflite(self, x_test_set, y_test_set,log=False):
        input_index = self.interpreter.get_input_details()[0]["index"]
        output_index = self.interpreter.get_output_details()[0]["index"]

        # Run predictions on every image in the "test" dataset.
        prediction_digits = []
        labels = []
        st = time.time()
        for i, test_image in enumerate(x_test_set):
            if i % 1000 == 0:
                print('Evaluated on {n} results so far.'.format(n=i))
            # Pre-processing: add batch dimension and convert to float32 to match with
            # the model's input data format.
            test_image = np.expand_dims(test_image, axis=0).astype(np.float32)
            self.interpreter.set_tensor(input_index, test_image)

            # Run inference.
            self.interpreter.invoke()
            output = self.interpreter.tensor(output_index)
            digit = np.argmax(output()[0])
            prediction_digits.append(np.array(digit))
            labels.append(int(y_test_set[i]))

        prediction_digits = np.array(prediction_digits)

        #TODO: agiustare calcolo predict per tflite
        accuracy = (prediction_digits == np.array(labels)).mean()

        et = time.time()
        self.elapsed_time = et - st
        if log :
            print('MIMT execution time:', self.elapsed_time, 'seconds')
            print('FPS:', len(x_test_set)/self.elapsed_time) 
        return 100*accuracy
        

    def trova_dif(self, x_test_set_tf, y_test_set_tf,x_test_set, y_test_set):
        counter = 0
        print("\tid\tinspectnn")
        for i in range(0,len(x_test_set)):
            img = x_test_set[i:i+1]
            label = y_test_set[i:i+1]
            nostro_tool=self.net.evaluate_accuracy(label, img)
            tflite = 100*self.evaluate_tflite(x_test_set_tf[i:i+1],y_test_set_tf[i:i+1])
            if(nostro_tool!=tflite):
                print(counter,i,nostro_tool,sep='\t')
                counter+=1
        
        return counter/len(x_test_set)
    
    



                

    

    
    
    
        