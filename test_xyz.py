import numpy as np
import iopolymc as io

import time
import os
import glob


if __name__ == "__main__":

    xyz_fn = 'test/test.xyz'

    t1 = time.time()
    xyz = io.read_xyz(xyz_fn)
    t2 = time.time()
    print(f'read_xyz: {t2-t1}')
    t1 = time.time()
    
    for key in xyz:
        print('########')
        print(key)
        
    xyz = io.load_xyz(xyz_fn,savenpy=True,loadnpy=True)
    
    t2 = time.time()
    print(f'load_xyz (1): {t2-t1}')
    t1 = time.time()
    
    xyz = io.load_xyz(xyz_fn,savenpy=True,loadnpy=True)
    
    t2 = time.time()
    print(f'load_xyz (2): {t2-t1}')
    t1 = time.time()
    
    npyfiles = glob.glob('test/*.npy')
    for fn in npyfiles:
        os.remove(fn)
    print('removed npy binaries')
        
    xyzout_fn = 'test/test_xyzout'
    io.write_xyz(xyzout_fn,xyz)
    
    xyzout_fns = glob.glob(xyzout_fn+'*')
    for fn in xyzout_fns:
        os.remove(fn)
    print(f'removed {xyzout_fn}')