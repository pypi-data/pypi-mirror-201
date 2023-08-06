# inspect-nn : simPle sImulator for Neural nEtworks using APProximate muLtipliErs (written in python)

inspect-nn is a simulation tool for measuring the classification accuracy loss due to the use of approximate multipliers (i.e., multipliers designed by exploiting the [approximate computing design paradigm](https://link.springer.com/book/10.1007/978-3-030-94705-7)) in neural networks. 

It has been developed to easily do porting of keras/tensorflow models, and to use the GPU to simulate a neural network while using approximate arithmetic units quickly and almost effortlessly. 

Anyway, it is still under development!

## Installing the module
You can install this module using ```pip```
```bash
$ pip install inspect-nn
```

## Using inspect-nn

### Layers supported
| Name | Supported  | GPU |
|-----------|:-----------|:-----------: 
| Conv      | yes | yes | 
| Dense     | yes | yes |
| Pool      | yes | yes |
| Flattern  | yes | yes |

### Activation supported
| Name | Supported  | GPU |
|-----------|:-----------|:-----------:
| Relu      | yes | yes |
| Softmax   | yes | no  |

## Using inspect-nn whit kaggle
creare un nuovo notebook in kaggle.

importare il notebook presente nella cartella kaggle.


aggiungere al proprio dataset il file h5 contente i pesi della rete addestrata.

aggiungere al proprio dataset i file contenenti i modelli dei moltiplciatori approsimati.

Il moltiplicatore è  composta da una matrice N*N che contiene il risultato della moltiplicazione approsimata tra i valori degli indici meno l' offset
```model[a,b]=(a-offset1)*(b-offset2)```

Installare su kaggle il pachetto. Run:  
``` !pip install inspect-nn ```

importare inspectnn e tutti i layer necessari di cui è composta la rete

# Exemple 

```python
import numpy as np, time, tensorflow as tf, random, os, sys
from keras.utils import np_utils
from numba import cuda

import inspectnn
from inspectnn import ConvLayer,PoolingLayer,FlattenLayer,DenseLayer


#load the learned parameters from training model
model = tf.keras.models.load_model('/kaggle/input/py-apple/lenet5.h5')
learned_parameters = model.get_weights()

#load the images e labels data
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
test_images = x_test.astype(np.int8)
test_labels = np_utils.to_categorical(y_test, 10)

num_of_samples = 1000
dataset = random.sample(range(len(test_images)), num_of_samples)
images = [ test_images[i].reshape([28, 28, 1]) for i in dataset ]
labels = [ test_labels[i] for i in dataset ]

#import model's aproximate multiplicator
sys.path.insert(1, '/kaggle/input/lenetvariantmux')
from variant_00000 import s_arrmul8


if __name__ == '__main__':
        
    #caricare su gpu i dati del moltiplicatore approsimato
    mult_class = s_arrmul8()
    multiplier=cuda.to_device(np.array(mult_class.model,dtype=np.int16))
      
    input_shape=[28, 28, 1]
   
    conv1=ConvLayer(stride = (1, 1), padding = (0, 0), activation = "relu", quant_nbits = 7, name = "conv_1",multiplier=multiplier)
    pool1=PoolingLayer(stride = (2, 2), pool_size = (2, 2), pooling = "max", name = "pool_1")
    conv2=ConvLayer(stride = (1, 1), padding = (0, 0), activation = "relu", quant_nbits = 7, name = "conv_2",multiplier=multiplier)
    pool2=PoolingLayer(stride = (2, 2), pool_size = (2, 2), pooling = "max", name = "pool_2")
    
    flat=FlattenLayer(name = "reshape")
    dense1=DenseLayer(activation = "relu", quant_nbits = 7, name = "dense_1",multiplier=multiplier)
    dense2=DenseLayer(activation = "relu", quant_nbits = 7, name = "dense_2",multiplier=multiplier)
    dense3=DenseLayer(activation = "softmax", quant_nbits = 7, name = "dense_3",multiplier=multiplier)  # type: ignore

    pineapple = inspectnn.NetworkModel(learned_parameters = learned_parameters, input_shape = input_shape,
                                       layers = [conv1,pool1,conv2,pool2,flat,dense1,dense2,dense3])

    print(len(images))
    print(f"Testing on {num_of_samples} images (over {len(test_images)} test images available).")
    st = time.time()
    print(f"Accuracy: {pineapple.evaluate_accuracy(labels, images)}")
    et = time.time()
    elapsed_time = et - st
    print('MIMT execution time:', elapsed_time, 'seconds')
    print('FPS:', num_of_samples/elapsed_time) 
    pineapple.print_time_statics()
```
# Exemple test all multiplicator

```python
import glob, os,sys,imp
import importlib.util
from numba import cuda
  
#dynamic import 
def __import__(module_name,class_name, globals=None, locals=None, fromlist=None):
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
            
with open('/kaggle/working/Results.csv', 'w', encoding='UTF8', newline='') as f:
    print('Name, Accuracy',file=f)
    f.close()
os.chdir('/kaggle/input/pyalslenet5int8mse-noiaa')

for file in glob.glob("/kaggle/input/pyalslenet5int8mse-noiaa/*.py"):
    
    module_name = file.replace('/kaggle/input/pyalslenet5int8mse-noiaa/', '')
    name_class = module_name.replace('.py', '')    
    module_name = __import__(name_class,name_class)
    
    variant_mul = getattr(module_name, name_class)
    mult_class = variant_mul()
    multiplier=cuda.to_device(np.array(mult_class.model,dtype=np.int16))
    
    model=Lenet5_aproximate(multiplier,7)    
    Accuracy = model.evaluate(images,labels)
    
    with open('/kaggle/working/Results.csv', 'a', encoding='UTF8', newline='') as f:
        print(name_class,', ',str(Accuracy),file=f)
        f.close()
```