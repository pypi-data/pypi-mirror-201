import liblip as ll
import sys
import math
import numpy as np

    
###
# test liblip for model comparison     
# ###  

def rmse( pred, y): return round( math.sqrt( ( (pred - y) ** 2).mean()), 4)

print( "-- test liblip for model comparison start --")
XData = np.array([[0.0000000e+00, 2.0040000e+03, 0.0000000e+00, 5.9000000e+01, 3.1570000e+03, 1.1636352e+09, 3.0000000e+00, 4.3000000e+01,
9.6300000e+02, 0.0000000e+00, 1.1392460e+06, 2.9800000e+02, 3.0000000e+00, 0.0000000e+00, 0.0000000e+00, 1.7000000e+01,
9.9908900e+05, 0.0000000e+00, 6.0000000e+00, 3.2000000e+02],
[0.0000000e+00, 1.9960000e+03, 4.0000000e+00, 6.2000000e+01, 7.7000000e+01, 1.0802592e+09, 3.0000000e+00, 5.7000000e+01,
1.7450000e+03, 0.0000000e+00, 1.1392480e+06, 5.2900000e+02, 3.0000000e+00, 9.8000000e+01, 0.0000000e+00, 1.2000000e+01,
1.1765700e+05, 0.0000000e+00, 6.0000000e+00, 8.6000000e+01]])
YData = np.array([11.09741 , 10.950807])
XValid = np.array( [[0.000000e+00, 1.000000e+03, 4.000000e+00, 4.800000e+01, 4.124000e+03, 1.317600e+09, 1.000000e+00, 4.300000e+01,
2.301000e+03, 0.000000e+00, 1.218822e+06, 7.060000e+02, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00,
1.024652e+06, 5.000000e+00, 5.000000e+00, 2.760000e+02]])
YValid = np.array( [10.043249])

dim = XData.shape[1]
npts =  XData.shape[0]
print( f'dim: {dim}, npts: {npts}')

ll.LipIntComputeLipschitz(dim,npts,XData, YData)
lip_const = ll.LipIntGetLipConst()
print( f'lipschitz constant: {lip_const}')

x_len = XValid.shape[0]
index = [0] * dim
pred = np.zeros( x_len)

for i in range( 0, x_len):
    x = XValid[i,:]
    pred[i] = ll.LipIntValue( dim, npts, x, XData, YData, lip_const, index)
    print( pred[i])

print( f'rmse: {rmse( pred, YValid)}')


print( "-- test liblip for model comparison end --")