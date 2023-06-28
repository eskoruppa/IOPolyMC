import numpy as np
import iopolymc as io

import time
import os
import glob


if __name__ == "__main__":

    state_fn = 'test/test2.state'
    # state_fn = 'test/s_0p0400_run1.state'

    t1 = time.time()
    state = io.read_state(state_fn)
    t2 = time.time()
    print(f'read_state: {t2-t1}')
    t1 = time.time()
    
    for key in state:
        print('########')
        print(key)
        
    state = io.load_state(state_fn,savenpy=True,loadnpy=True)
    
    t2 = time.time()
    print(f'load_state (1): {t2-t1}')
    t1 = time.time()
    
    state = io.load_state(state_fn,savenpy=True,loadnpy=True)
    
    t2 = time.time()
    print(f'load_state (2): {t2-t1}')
    t1 = time.time()
    
    npyfiles = glob.glob('test/*.npy')
    for fn in npyfiles:
        os.remove(fn)
    
    print('removed npy binaries')