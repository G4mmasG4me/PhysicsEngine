from numba import jit, cuda
import numpy as np
# to measure exec time
import time
  
# normal function to run on cpu
def func(a):                                
    for i in range(10000000):
        a[i]+= 1      
  
# function optimized to run on gpu 
@jit(target_backend='cuda')                         
def func2(a):
    for i in range(10000000):
        a[i]+= 1
  
if __name__=="__main__":
    n = 10000000                            
    a = np.ones(n, dtype = np.float64)
      
    start = time.time()
    func(a)
    print("without GPU:", time.time()-start)    
      
    start = time.time()
    func2(a)
    print("with GPU:", time.time()-start)