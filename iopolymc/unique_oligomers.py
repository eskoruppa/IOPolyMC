import numpy as np
import sys
from typing import List


def unique_oligomers(num_bp: int, bases="atcg",omit_equiv=True) -> List[str]:
    uo = UniqueOligomers(bases=bases,omit_equiv=omit_equiv)
    return uo.get_oligomers(num_bp)


class UniqueOligomers(object):
    
    bases: str
    total: int
    seqlist: List[str]

    def __init__(self,bases="atcg",omit_equiv=True):
        self.bases = bases.lower()
        self.omit_equiv = omit_equiv
        self.total   = 0
        self.seqlist = list()
    
    def get_oligomers(self, num_bp: int):
        self.seqlist    = list()
        current         = 0
        self.total      = num_bp
        
        self._seqloop("",current)
        return self.seqlist
        
    def _seqloop(self,seq,current):
        current += 1
        for i in range(len(self.bases)): 
            new_seq = "%s"%seq + self.bases[i]
            
            if current < self.total:
                self.seqloop(new_seq,current)
            else:
                if (not self.omit_equiv) or (not self.invert_seq(new_seq) in self.seqlist):
                #if not self.invert_seq(new_seq) in self.seqlist:
                    self.seqlist.append(new_seq)
    
    def invert_seq(self,seq: str) -> str:
        amount_bp = len(seq)
        inv = ''
        for i in range(amount_bp):
            if seq[amount_bp-1-i] == "a":
                inv = inv + "t"
            if seq[amount_bp-1-i] == "t":
                inv = inv + "a"
            if seq[amount_bp-1-i] == "c":
                inv = inv + "g"
            if seq[amount_bp-1-i] == "g":
                inv = inv + "c"
        return inv
    
    def get_mid_dimer(self,seq: str):
        original = seq
        if len(seq)%2 == 0:
            UO = UniqueOligomers()
            unique_dimers = np.sort(UO.get_oligomers(2))
            dimer = seq[len(seq)/2-1:len(seq)/2+1] 
            if dimer not in unique_dimers:
                dimer       = self.invert_seq(dimer)
                original    = self.invert_seq(seq)
            return dimer,original
        return "",original

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("usage: %s N"%sys.argv[0])
        sys.exit()
    
    N = int(sys.argv[1])
    bases = "atcg"
    if len(sys.argv) >= 3:
        bases = sys.argv[2]
        
    uo = UniqueOligomers(bases=bases)
    olis = uo.get_oligomers(N)
    
    print(len(olis))
    #~ for oli in olis:
        #~ print(oli)
    
    
    
