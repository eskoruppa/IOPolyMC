import iopolymc as iopmc
import sys

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("usage: python %s fin fout, snapshot"%sys.argv[0])
        sys.exit(0)

    statefn  = sys.argv[1]
    fout     = sys.argv[2]
    snapshot = int(sys.argv[3])

    iopmc.state2pdb(statefn,fout,snapshot)
