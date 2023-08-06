import time

import numpy as np

from inspectnn.Conv.ConvLayer_TFLITE import ConvLayer_TFLITE
from inspectnn.Dense.DenseLayer_TFLITE import DenseLayer_TFLITE
from inspectnn.Pooling.PoolingLayer_TFLITE import PoolingLayer_TFLITE
from inspectnn.Flatten.FlattenLayer import FlattenLayer
from inspectnn.Add.AddLayer import AddLayer

from inspectnn.Model.NetworkModel_tflite import NetworkModelTflite
from inspectnn.Model.BaseModel_tflite import BaseModel_tflite
from inspectnn.Quantizate.QuantizateLayer import QuantizateLayer

import tflite
import numpy as np, time, tensorflow as tf

class GenericModelTflite(BaseModel_tflite):
    def __init__(self,path_tf_file="/home/filippo/Git/PhD_AdversarialAttack/Models/ResNet8-quantized.tflite",input_no_normalizate=True):

        self.quant_nbits = 7
        save_csv_path=''
        self.input_no_normalizate = input_no_normalizate

        
        
        self.interpreter = tf.lite.Interpreter(model_path=path_tf_file,experimental_preserve_all_tensors=True)
        self.interpreter.allocate_tensors()
        #apri il file tflite
        f = open(path_tf_file,"rb")
        buf = f.read()

        self.model = tflite.Model.GetRootAsModel(buf,0)

        #print("len:",self.model.SubgraphsLength())
        graf = self.model.Subgraphs(0)
        input_shape = self.interpreter.get_tensor_details()[graf.Operators(0).Inputs(0)]['shape'][1:]
        super().__init__(None,self.quant_nbits,input_shape,save_csv_path)
       
        

        #ssuper().__init__(None,self.quant_nbits,input_shape,save_csv_path)
        layers = []
        self.data_layer = []
        self.data_layer_quant = []
        self.learned_parameters = []

        self.n_moltiplicazioni = []
        self.tensor_output_layer = []

        #Crea i singoli layer
        for i in range(graf.OperatorsLength()-2):
            op=graf.Operators(i)           
            #print(i,tflite.utils.BUILTIN_OPCODE2NAME[self.__LayerOpcodeConverter__(op.OpcodeIndex())],op.InputsLength(),op.OutputsLength())
            #for j in range(op.InputsLength()):
            #    print("\t",op.Inputs(j))
            
            layers.append(self.__ImportLayer__(op))
            self.tensor_output_layer.append(op.Outputs(0))

            #print("OUT:",op.Outputs(0))


        #collega le uscite dei layer
        layers[0].gpu_output_memory = True
        for i in range(1,graf.OperatorsLength()-2):
            layers[i].load_input_layer(layers,self.tensor_output_layer)
           
        layers[-1].end_layer =True
        layers[-1].gpu_output_memory = False

        self.net =  NetworkModelTflite(quant_data_scale=self.data_layer_quant,
                                       quant_data=self.data_layer, 
                                       learned_parameters = self.learned_parameters, 
                                       input_shape = input_shape,
                                       layers = layers)

        print(path_tf_file,np.sum(self.n_moltiplicazioni))
    def __LayerOpcodeConverter__(self,id):
        return self.model.OperatorCodes(id).BuiltinCode() 

    def __ReadGenericParameters__(self,op,name_id=0):
        name_layer=self.interpreter.get_tensor_details()[op.Outputs(0)]['name'].split(';')[-name_id].split('/')[-2]
        input_shape = self.interpreter.get_tensor_details()[op.Inputs(0)]['shape'][1:]

        return name_layer,input_shape
    
    def __ImportLayer__(self,op):
        disponibilita_gpu=True

        #TODO: parametrizare meglio i layer prendendo i dati da op
        layer=None
        op_opt = op.BuiltinOptions()

        if(tflite.utils.BUILTIN_OPCODE2NAME[self.__LayerOpcodeConverter__(op.OpcodeIndex())] == "QUANTIZE"):
            name_layer,input_shape = self.__ReadGenericParameters__(op)
            layer = QuantizateLayer(quant_nbits =  self.quant_nbits, name = 'Q_' + name_layer)
            layer.code_tensor_inputs = [op.Inputs(i) for i in range(1)]

            if op.Inputs(0) == 0 and self.input_no_normalizate:
                quant_output_k = 1#self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][0]#*255
            else:
                quant_output_k = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][0]

            quant_output_offset = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][1]

            layer.load_weights(input_shape = input_shape,enable_gpu=disponibilita_gpu,gpu_input_memory=None,
                               quant_output_k=quant_output_k,quant_output_offset=quant_output_offset)
                
        elif(tflite.utils.BUILTIN_OPCODE2NAME[self.__LayerOpcodeConverter__(op.OpcodeIndex())] == "CONV_2D"):
            
            conv_op = tflite.Conv2DOptions()
            conv_op.Init(op_opt.Bytes, op_opt.Pos)

            name_layer,input_shape = self.__ReadGenericParameters__(op,2)
            type_attivation=self.interpreter.get_tensor_details()[op.Outputs(0)]['name'].split(';')[0].split('/')[-1]

            if conv_op.Padding() == tflite.Padding.SAME :
                padding_type ='same'
            else:
                padding_type ='valid'
            
            layer = ConvLayer_TFLITE(stride = (conv_op.StrideW(), conv_op.StrideH()), padding = (0, 0), activation = type_attivation, padding_type = padding_type,
                                      quant_nbits =  self.quant_nbits, name = name_layer,multiplier=self.exact_multiplier)#multiplier=MUL_2bit_importata
           
            self.learned_parameters.append(self.interpreter.get_tensor(op.Inputs(1)))#pesi weights
            self.learned_parameters.append(self.interpreter.get_tensor(op.Inputs(2)))#pesi bias
            
            quantization_pesi = self.interpreter.get_tensor_details()[op.Inputs(1)]['quantization_parameters']['scales']
            quantization_bias = self.interpreter.get_tensor_details()[op.Inputs(2)]['quantization_parameters']['scales']

            quant_input_k = self.interpreter.get_tensor_details()[op.Inputs(0)]['quantization'][0]
            quant_input_offset =  self.interpreter.get_tensor_details()[op.Inputs(0)]['quantization'][1]

            output_shape=self.interpreter.get_tensor_details()[op.Outputs(0)]['shape'][1:]
            
            quant_output_k = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][0]
            quant_output_offset = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][1]
            
            layer.code_tensor_inputs = [op.Inputs(i) for i in range(1)]
            layer.load_weights(input_shape = input_shape,output_shape=output_shape, weights = self.learned_parameters[-2], biases = self.learned_parameters[-1],
                                                                        enable_gpu=disponibilita_gpu,gpu_input_memory=None,
                                                                        quant_data=quantization_pesi,quant_bias=quantization_bias,
                                                                        quant_input_k=quant_input_k,quant_input_offset=quant_input_offset,
                                                                        quant_output_k=quant_output_k,quant_output_offset=quant_output_offset
                                                                        )
            #dimensione kernel(senza il numero di filtri, presenti nel output) * dimensione output
            layer.n_moltiplicazioni=np.prod(self.interpreter.get_tensor(op.Inputs(1)).shape[1:])*np.prod(output_shape)
              
        elif(tflite.utils.BUILTIN_OPCODE2NAME[self.__LayerOpcodeConverter__(op.OpcodeIndex())] == "FULLY_CONNECTED"):

            type_attivation=self.interpreter.get_tensor_details()[op.Outputs(0)]['name'].split(';')[1].split('/')[-1]
            name_layer,input_shape = self.__ReadGenericParameters__(op,1)
            

            if ( type_attivation != 'relu' and type_attivation != 'Relu'):
                type_attivation='softmax'
            layer=DenseLayer_TFLITE(activation = type_attivation, quant_nbits =  self.quant_nbits, name = name_layer,multiplier=self.exact_multiplier)
            self.learned_parameters.append(self.interpreter.get_tensor(op.Inputs(1)))#pesi weights

            self.learned_parameters.append(self.interpreter.get_tensor(op.Inputs(2)))#pesi bias
            
            quantization_pesi = self.interpreter.get_tensor_details()[op.Inputs(1)]['quantization_parameters']['scales']
            quantization_bias = self.interpreter.get_tensor_details()[op.Inputs(2)]['quantization_parameters']['scales']

            quant_input_k = self.interpreter.get_tensor_details()[op.Inputs(0)]['quantization'][0]
            quant_input_offset =  self.interpreter.get_tensor_details()[op.Inputs(0)]['quantization'][1]

            quant_output_k = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][0]
            quant_output_offset = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][1]
            output_shape=self.interpreter.get_tensor_details()[op.Outputs(0)]['shape']

            layer.code_tensor_inputs = [op.Inputs(i) for i in range(1)]

            layer.load_weights(input_shape = input_shape, output_shape=output_shape,weights = self.learned_parameters[-2], biases = self.learned_parameters[-1],
                                                                        enable_gpu=disponibilita_gpu,gpu_input_memory=None,
                                                                        quant_data=quantization_pesi,quant_bias=quantization_bias,
                                                                        quant_input_k=quant_input_k,quant_input_offset=quant_input_offset,
                                                                        quant_output_k=quant_output_k,quant_output_offset=quant_output_offset
                                                                        )
            #dimensione input * output
            layer.n_moltiplicazioni=np.prod(output_shape)*np.prod(input_shape)
           

        #TODO: unire i due pool
        elif(tflite.utils.BUILTIN_OPCODE2NAME[self.__LayerOpcodeConverter__(op.OpcodeIndex())] == "AVERAGE_POOL_2D"):
            name_layer,input_shape = self.__ReadGenericParameters__(op)

            stride = self.interpreter.get_tensor_details()[op.Inputs(0)]['shape'][1:3]//self.interpreter.get_tensor_details()[op.Outputs(0)]['shape'][1:3]
            pool_size = stride
            layer = PoolingLayer_TFLITE(stride = stride, pool_size = pool_size, pooling = "avg", name = name_layer)#TODO vare averge pool
            quant_output_k = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][0]
            quant_output_offset = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][1]

            layer.code_tensor_inputs = [op.Inputs(i) for i in range(1)]
            layer.load_weights(input_shape = input_shape,enable_gpu=disponibilita_gpu,gpu_input_memory=None,
                               quant_output_k=quant_output_k,quant_output_offset=quant_output_offset)

        elif(tflite.utils.BUILTIN_OPCODE2NAME[self.__LayerOpcodeConverter__(op.OpcodeIndex())] == "MAX_POOL_2D"):
            name_layer,input_shape = self.__ReadGenericParameters__(op)

            stride = self.interpreter.get_tensor_details()[op.Inputs(0)]['shape'][1:3]//self.interpreter.get_tensor_details()[op.Outputs(0)]['shape'][1:3]
            pool_size = stride

            layer = PoolingLayer_TFLITE(stride = stride, pool_size =pool_size, pooling = "max", name = name_layer)

            quant_output_k = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][0]
            quant_output_offset = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][1]

            layer.code_tensor_inputs = [op.Inputs(i) for i in range(1)]
            layer.load_weights(input_shape = input_shape,enable_gpu=disponibilita_gpu,gpu_input_memory=None,
                               quant_output_k=quant_output_k,quant_output_offset=quant_output_offset)
        
        elif(tflite.utils.BUILTIN_OPCODE2NAME[self.__LayerOpcodeConverter__(op.OpcodeIndex())] == "RESHAPE"):
            name_layer=self.interpreter.get_tensor_details()[op.Outputs(0)]['name'].split(';')[0].split('/')[1]
            input_shape = self.interpreter.get_tensor_details()[op.Inputs(0)]['shape'][1:]
            layer = FlattenLayer(name = name_layer)

            layer.code_tensor_inputs = [op.Inputs(i) for i in range(1)]
            layer.load_weights(input_shape = input_shape,enable_gpu=disponibilita_gpu,gpu_input_memory=None)

        elif(tflite.utils.BUILTIN_OPCODE2NAME[self.__LayerOpcodeConverter__(op.OpcodeIndex())] == "ADD"):
            type_attivation=self.interpreter.get_tensor_details()[op.Outputs(0)]['name'].split(';')[0].split('/')[-1]
            name_layer=self.interpreter.get_tensor_details()[op.Outputs(0)]['name'].split(';')[1].split('/')[-2]

            layer = AddLayer(name = name_layer, activation = type_attivation)

            input_shape_A = self.interpreter.get_tensor_details()[op.Inputs(0)]['shape']
            input_shape_B = self.interpreter.get_tensor_details()[op.Inputs(1)]['shape']
            output_shape=self.interpreter.get_tensor_details()[op.Outputs(0)]['shape'][1:]

            quant_output_k = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][0]
            quant_output_offset = self.interpreter.get_tensor_details()[op.Outputs(0)]['quantization'][1]

            layer.code_tensor_inputs = [op.Inputs(i) for i in range(2)]
            layer.load_weights(input_shape_A = input_shape_A,input_shape_B=input_shape_B,output_shape=output_shape,
                               quant_output_k=quant_output_k,quant_output_offset=quant_output_offset,
                               enable_gpu=disponibilita_gpu,gpu_input_memory=None)

        else:
            print(tflite.utils.BUILTIN_OPCODE2NAME[self.__LayerOpcodeConverter__(op.OpcodeIndex())],"Not supported")
        return layer
    
    def evaluate_tflite(self, x_test_set, y_test_set,print_debug=False):

        input_index = self.interpreter.get_input_details()[0]["index"]
        output_index = self.interpreter.get_output_details()[0]["index"]
        prediction_digits = []
        labels = []
        for i, test_image in enumerate(x_test_set):
            #if i % 1000 == 0:print('Evaluated on {n} results so far.'.format(n=i))

            test_image = np.expand_dims(test_image, axis=(0,3)).astype(np.float32)#fp32
            self.interpreter.set_tensor(input_index, test_image)

            # Run inference.
            self.interpreter.invoke()

            # Post-processing: remove batch dimension and find the digit with highest
            # probability.
            
            if print_debug :
                #valori resnet8
                quant_layer=6
                conv_lay = 9
                conv1_lay = 12
                conv2_lay = 12
        
                dens1_lay = 15
    

                layer_info=7
                
                
                
                print('### tflite interpetrer: -------#####>>>>>> L(',layer_info,")")
                print(self.interpreter.get_tensor(layer_info).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer_info)))

                
                print(self.interpreter.get_tensor(layer_info)[0][7])
                print(np.average(self.interpreter.get_tensor(layer_info)[0]))
                
                print("######### cov     #######")

                print(self.interpreter.get_tensor(conv_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv_lay)))
                print(self.interpreter.get_tensor(conv_lay)[0][0][3])
                print(np.max(self.interpreter.get_tensor(conv_lay)))

                print("######### max pool   1  #######")

                print(self.interpreter.get_tensor(10).shape)
                print("max:",np.amax(self.interpreter.get_tensor(10)))
                print(self.interpreter.get_tensor(10)[0][0][3])

                print("######### cov   1  #######")

                print(self.interpreter.get_tensor(conv1_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv1_lay)))
                print(self.interpreter.get_tensor(conv1_lay)[0][0][3])
                
                """

                print("######### cov   2  #######")

                print(self.interpreter.get_tensor(conv2_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv2_lay)))
                print(self.interpreter.get_tensor(conv2_lay)[0][0][0])
            
                
                print("######### ADD 1 #######")
                
                layer= 13
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][1][1])

                

                print("######### AVG #######")
                layer= 14
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][0][0])
                
                print("######### quant #######")
                layer= 15
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][0][0])
                
                print("######### reshape #######")
                layer= 16
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][:16])


                print("######### dens 1  #######")
                dens1_lay = 18
                print(self.interpreter.get_tensor(dens1_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(dens1_lay)))
                print(self.interpreter.get_tensor(dens1_lay)[0])

                
                #valori resnet8
                quant_layer=13
                conv_lay = 15
                conv1_lay = 17
                conv2_lay = 19
                conv3_lay = 21
                dens1_lay = 15
                dens2_lay = 17

                layer_info=quant_layer
                
                
                
                print('### tflite interpetrer: -------#####>>>>>> L(',layer_info,")")
                print(self.interpreter.get_tensor(layer_info).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer_info)))
                print(self.interpreter.get_tensor(layer_info)[0][0])
                print("######### cov     #######")

                print(self.interpreter.get_tensor(conv_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv_lay)))
                print(self.interpreter.get_tensor(conv_lay)[0][0][0])
            
                print("######### cov   1  #######")

                print(self.interpreter.get_tensor(conv1_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv1_lay)))
                print(self.interpreter.get_tensor(conv1_lay)[0][0][0])
                

                print("######### cov   2  #######")

                print(self.interpreter.get_tensor(conv2_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv2_lay)))
                print(self.interpreter.get_tensor(conv2_lay)[0][0][0])
                

                print("######### cov   3  #######")

                print(self.interpreter.get_tensor(conv3_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv3_lay)))
                print(self.interpreter.get_tensor(conv3_lay)[0][0][0])

                print("######### ADD 1 #######")
                
                layer= 22
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][1][1])

         
                conv1_lay = 24
                conv2_lay = 26
                conv3_lay = 28
                dens1_lay = 15
                dens2_lay = 17

                layer_info=quant_layer
                
      
                print("######### cov   4  #######")

                print(self.interpreter.get_tensor(conv1_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv1_lay)))
                print(self.interpreter.get_tensor(conv1_lay)[0][0][0])
                

                print("######### cov   5  #######")

                print(self.interpreter.get_tensor(conv2_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv2_lay)))
                print(self.interpreter.get_tensor(conv2_lay)[0][0][0])
                

                print("######### cov   6  #######")

                print(self.interpreter.get_tensor(conv3_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(conv3_lay)))
                print(self.interpreter.get_tensor(conv3_lay)[0][0][0])

                
                print("######### ADD 2 #######")
                
                layer= 29
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][0][0])


                
                print("######### ADD 3 #######")

                
                layer= 27
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][0][0])
                
                
                print("######### AVG #######")
                layer= 14
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][0][0])
                
                print("######### quant #######")
                layer= 15
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][0][0])
                
                print("######### reshape #######")
                layer= 16
                print(self.interpreter.get_tensor(layer).shape)
                print("max:",np.amax(self.interpreter.get_tensor(layer)))
                print(self.interpreter.get_tensor(layer)[0][:16])


                print("######### dens 1  #######")
                dens1_lay = 18
                print(self.interpreter.get_tensor(dens1_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(dens1_lay)))
                print(self.interpreter.get_tensor(dens1_lay)[0])

                
                
                print("######### dens 2  #######")

                print(self.interpreter.get_tensor(dens2_lay).shape)
                print("max:",np.amax(self.interpreter.get_tensor(dens2_lay)))
                print(self.interpreter.get_tensor(dens2_lay)[0])

                #print(self.interpreter.get_tensor(0)[0][0]*256)
                #print("#########  fake quant min max    #######")
                #xf=self.interpreter.get_tensor(0)*255 -128

                #xq=(xf-np.amin(xf)/(np.amax(xf)-2*np.amin(xf)))
                #print(xq[0][0])
                #print(self.interpreter.get_tensor_details()[layer_info-1])
                #print(self.interpreter.get_tensor_details()[layer_info])
                #print("#########    risultato interpetre #######")
                #print(self.interpreter.tensor(layer_info)()[0][0])
                """
                
            output = self.interpreter.tensor(output_index)
            digit = np.argmax(output()[0])
            prediction_digits.append(np.array(digit))
            labels.append(int(y_test_set[i]))

            
    # Compare prediction results with ground truth labels to calculate accuracy.
        prediction_digits = np.array(prediction_digits)
        accuracy = (prediction_digits == np.array(labels)).mean()
        return accuracy
    
   