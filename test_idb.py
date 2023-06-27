import numpy as np
import iopolymc as io


if __name__ == "__main__":

    idb = io.read_idb('test/test.idb')

    for key in idb:
        print('########')
        print(key)

    for key in idb['params'].keys():
        print(key)
        print(idb['params'][key])

    
    io.write_idb('test/test_out.idb',idb)