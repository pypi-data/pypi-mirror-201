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

@cuda.jit
def matmul_tflite(R,A, B,k_mul,k_filtri,k_bias, M,offset1,offset2,activation,result_max,out_mul,out_offest):

    row, col = cuda.grid(2)
    if row < R.shape[0] and col < R.shape[1]:
        tmp = 0
        for k in range(A.shape[1]): 
            tmp +=  M[int8(A[row, k])+offset1 , int8(B[col, k]+offset2)]        
            #tmp += A[row, k]*B[col, k]
            
        ris = k_mul[row]*tmp - k_filtri[col] + k_bias[col]#TODO:in caso di moltiplicazione matriciali(questa di fatto è un vettore per una matrice è)
        
        if activation and ris<0:
            ris=0

        R[row, col] = round(ris*out_mul + out_offest)
        
    return   
