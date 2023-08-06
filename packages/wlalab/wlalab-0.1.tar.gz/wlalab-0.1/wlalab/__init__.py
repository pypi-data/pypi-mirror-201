import os 

def limit_thread(a:int):
    a = str(a)
    os.environ["MKL_NUM_THREADS"]=a
    os.environ["OMP_NUM_THREADS"]=a

# by default, set  number of threads to 1
limit_thread(1)

