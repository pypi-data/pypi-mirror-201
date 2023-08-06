import liblip as ll
import sys
import math
import random
import timeit
import numpy as np
from memory_profiler import profile

    
# test function, here just a product of sin(2x)sin(2y),...
def fun2( dat, dim):
    s = 1.0
    for j in range( dim): s *= math.sin( 2 * dat[j])
    return s

# generate data randomly
def generate_random_data( dim, npts):
    x, XData, YData = ll.init( dim, npts)
    for i in range( npts):
        for j in range( dim):
            x[j] = random.random() * 3.0 # some random x
            XData[i * dim + j] = x[j]
        YData[i] = fun2( x, dim)
    return x, XData, YData

@profile
def profile_liblip():
    w = ll.LipIntValues( valid_rows, dim, npts, XValid, XData, YData, LipConst, index)
    return pred




def test_slip_int():   
    print( "initializing") 
    dim = 20        # the dimension and size of the data set
    npts = 10
    LipConst = 0.03
    index = None
    
    XValid, XData, YData = generate_random_data( dim, npts)
    valid_rows = 1
    print( f'XData: {XData.shape}, YData: {YData.shape} : XValid: {XValid.shape}')

    # calculate the value
    print( "calculating")
    t0 = timeit.default_timer()
    # print( f'&x: {id( x)}, &XData: {id( XData)}, &YData: {id( YData)}')
    w = profile_liblip()
    # print( f'&x: {id( x)}, &XData: {id( XData)}, &YData: {id( YData)}')
    t1 = timeit.default_timer()   
    print( "time: ", t1 - t0)

###
# Main test program
###
if __name__ == "__main__":
    print( "-- test wrapper start --")
    test_slip_int()
    print( "-- test wrapper end --")
