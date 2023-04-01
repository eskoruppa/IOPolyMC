import numpy as np
import iopolymc as io


if __name__ == "__main__":

    idb = io.read_idb('test/random.idb')

    for key in idb:
        print('########')
        print(key)

    for key in idb['params'].keys():
        print(key)
        print(idb['params'][key])

    
    io.write_idb('test/test.idb',idb)