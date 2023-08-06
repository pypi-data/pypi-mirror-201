"""
Copyright 2022  Salvatore Barone <salvatore.barone@unina.it>
                Filippo Ferrandino <fi.ferrandino@studenti.unina.it>

This is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 3 of the License, or any later version.

This is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
RMEncoder; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
from numba import cuda
import numpy as np, json, copy, time
from inspectnn.Model.NetworkModel import NetworkModel 
from distutils.dir_util import mkpath
from inspectnn.Conv.ConvLayer import ConvLayer
from inspectnn.Dense.DenseLayer import DenseLayer
from inspectnn.Pooling.PoolingLayer_TFLITE import PoolingLayer_TFLITE
from inspectnn.Flatten.FlattenLayer import FlattenLayer
from inspectnn.Quantizate.QuantizateLayer import QuantizateLayer
from inspectnn.Add.AddLayer import AddLayer
#from .OutputLayer import OutputLayer
from inspectnn.Utils.utils import grouped, flatten


class NetworkModelTflite(NetworkModel):
    #TODO:ereditare da NetworkModel
    def __init__(self, learned_parameters, layers,input_shape,print_input=False,quant_data=None,quant_data_scale=None):
        self.learned_parameters = learned_parameters
        self.layers = layers
        self.outputs = []
        self.input_shape=input_shape
        self.print_input = print_input
        self.total_time = 0
        self.n_frame_inference = 0
        self.elapsed_time = np.zeros(len(layers))
        self.quant_data=quant_data
        self.get_Numbers_layer_with_multiply()
        self.images_on_gpu=False

    def __deepcopy__(self, memo = None):
        return NetworkModelTflite(self.learned_parameters, copy.deepcopy(self.layers),self.input_shape)
             
    def predict(self, test_image):
        self.n_frame_inference+=1
        if self.print_input:
            with open('test_image.txt', 'w', encoding='UTF8', newline='') as f:
                print(self.outputs,file=f)
        
        id_layer = 0
        st = time.time()
        self.layers[id_layer].forward_pass(inputv = test_image)
        et = time.time()
        self.elapsed_time[id_layer] += et - st
        self.total_time += et - st

   
        for id_layer in range(1,len(self.layers)):
            st = time.time()
            #print(self.name,self.blockdim,self.griddim)
            #print("layers: ",self.layers[id_layer].name,self.layers[id_layer].blockdim,self.layers[id_layer].griddim)
            if(self.print_input):
                self.layers[id_layer].update_save_path()
            if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer,PoolingLayer_TFLITE, FlattenLayer,QuantizateLayer,AddLayer)):
                self.layers[id_layer].forward_pass()
            else:
                print('Layer {:>15} not supported yet'.format(self.layers[id_layer].name))

            et = time.time()
            self.elapsed_time[id_layer] += et - st
            self.total_time += et - st
        
        return self.layers[id_layer].outputv
    


    