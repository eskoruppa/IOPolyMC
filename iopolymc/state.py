import numpy as np
import os,sys
from ._file_read import file_read
from .simplest_type import simplest_type


def load_state(filename: str) -> dict:
    """
        Loads data in state-file and saves positions, triads and Omegas as
        numpy binaries. Data is loaded from binary if binary already exists. 
        
        Use to speed up loadtime
    """
    
    pos_fnpy    = os.path.splitext(filename)[0] + '_pos.npy'
    triads_fnpy = os.path.splitext(filename)[0] + '_triads.npy'
    Omegas_fnpy = os.path.splitext(filename)[0] + '_Omegas.npy'
    
    state     = read_spec(filename)
    all_found = True
    if state['pos_contained']:
        if not os.path.isfile(pos_fnpy) or (os.path.getmtime(pos_fnpy) < os.path.getmtime(filename)):
            all_found = False
    if state['triads_contained']:
        if not os.path.isfile(triads_fnpy) or (os.path.getmtime(triads_fnpy) < os.path.getmtime(filename)):
            all_found = False
    if state['Omegas_contained']:
        if not os.path.isfile(Omegas_fnpy) or (os.path.getmtime(Omegas_fnpy) < os.path.getmtime(filename)):
            all_found = False

    if all_found:
        print('quickload')
        if state['pos_contained']:
            print(f"loading positions from '{pos_fnpy}'")
            state['pos']    = np.load(pos_fnpy)
        if state['triads_contained']:
            print(f"loading triads from    '{triads_fnpy}'")
            state['triads'] = np.load(triads_fnpy)
        if state['Omegas_contained']:
            print(f"loading Omegas from    '{Omegas_fnpy}'")
            state['Omegas'] = np.load(Omegas_fnpy)
    else:
        state = read_state(filename)
        if state['pos_contained']:
            _save_pos(pos_fnpy,state['pos'])
        if state['triads_contained']:
            _save_pos(triads_fnpy,state['triads'])
        if state['Omegas_contained']:
            _save_pos(Omegas_fnpy,state['Omegas'])
            
    return state

def read_spec(fn: str) -> dict:
    specs = dict()
    specs["pos_contained"]    = False
    specs["triads_contained"] = False
    specs["Omegas_contained"] = False
    
    with open(fn, 'r') as f:
        line = f.readline()
        ll = _linelist(line)
        while line != '' and 'snapshot' not in line.lower():
            if line.strip()[0] == '#':
                line = f.readline()
                ll = _linelist(line)
                continue
            arg = ll[0].replace(':','').strip()
            if arg == 'pos':
                arg = 'pos_contained'
            if arg == 'triads':
                arg = 'triads_contained'
            if arg == 'Omegas':
                arg = 'Omegas_contained'
            val = simplest_type(ll[-1])
            specs[arg] = val
            line = f.readline()
            ll = _linelist(line)
    Lk0 = specs["Segments"]*specs["disc_len"]/0.34/10
    specs["sigma"] = specs["delta_LK"]/Lk0
    return specs

def read_state(fn: str) -> dict():
    """
        Reads state-file. 
    """
    specs = read_spec(fn)
    num_segs = specs['Segments']

    all_pos = list()
    all_triads = list()
    all_Omegas = list()

    with open(fn,'r') as f:
        line = f.readline()
        while 'snapshot' not in line.lower():
            line = f.readline()

        while line != '':
            if specs['pos_contained']:
                pos = np.zeros((num_segs,3))
                for i in range(num_segs):
                    line = f.readline()
                    ll = _linelist(line)
                    pos[i,0] = float(ll[0])
                    pos[i,1] = float(ll[1])
                    pos[i,2] = float(ll[2])
                all_pos.append( pos )
            if specs['triads_contained']:
                triads = np.zeros((num_segs,3,3))
                for i in range(num_segs):
                    line = f.readline()
                    ll = _linelist(line)
                    triads[i,0] = [float(ll[0]),float(ll[1]),float(ll[2])]
                    triads[i,1] = [float(ll[3]),float(ll[4]),float(ll[5])]
                    triads[i,2] = [float(ll[6]),float(ll[7]),float(ll[8])]
                all_triads.append(triads)
            if specs['Omegas_contained']:
                Omegas = np.zeros((num_segs,3))
                for i in range(num_segs):
                    line = f.readline()
                    ll = _linelist(line)
                    Omegas[i,0] = float(ll[0])
                    Omegas[i,1] = float(ll[1])
                    Omegas[i,2] = float(ll[2])
                all_Omegas.append( Omegas )
            line = f.readline()

    if specs['pos_contained']:
        specs['pos'] = np.array(all_pos)
    if specs['triads_contained']:
        specs['triads'] = np.array(all_triads)
    if specs['Omegas_contained']:
        specs['Omegas'] = np.array(all_Omegas)
    
    return specs
    
    
def _save_pos(outname,snapshots):
    if outname[-4:] == '.npy':
        outn = outname
    else:
        outn = outname + '.npy'
    np.save(outn,snapshots)

def _remove_newline(string):
    if string[-1] == "\n":
        return string[:-1]

def _linelist(string):
    return [entry for entry in string.strip().split(' ') if entry != '']

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("usage: python %s filename"%sys.argv[0])
        sys.exit(0)
    fn  = sys.argv[1]
    
    spec = read_spec(fn)
    for key,val in spec.items():
        print( key, "=", val )
    
    # state = load_state(fn)
    # pos = state['pos']
    # # ~ fnpy = fn.split('.')[0]+'.npy'
    # # ~ _save_pos(fnpy,pos)
        
    # print("%d snapshots found"%len(pos))
    
