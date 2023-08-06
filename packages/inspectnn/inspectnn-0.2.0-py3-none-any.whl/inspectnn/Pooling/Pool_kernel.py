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
from numba import cuda, int8

TPB=16 #TODO:calcolare il tpb dinamicamente   
@cuda.jit
def pool(R, inputv, stride, pool_size):#, pooling):
    x, y,k = cuda.grid(3)
    if x < R.shape[0] and y < R.shape[1] and k < R.shape[2]:
        x_start = x * stride[0]
        x_end = x_start + pool_size[0]
        y_start = y * stride[1]
        y_end = y_start + pool_size[1]
        temp_max = -300
        for i in range(x_start,x_end):
            for j in range(y_start,y_end,):
                if(inputv[i,j,k]>temp_max):
                    temp_max=inputv[i,j,k]
        
        R[x, y, k]=temp_max
    

@cuda.jit
def pool_avg(R, inputv, stride, pool_size):#, pooling):
    x, y,k = cuda.grid(3)
    if x < R.shape[0] and y < R.shape[1] and k < R.shape[2]:
        x_start = x * stride[0]
        x_end = x_start + pool_size[0]
        y_start = y * stride[1]
        y_end = y_start + pool_size[1]
        
        temp_sum = 0
        for i in range(x_start,x_end):
            for j in range(y_start,y_end):
                temp_sum+=inputv[i,j,k]
        
        R[x, y, k] = round(temp_sum/(pool_size[0]*pool_size[1]))