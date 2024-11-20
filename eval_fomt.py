import os, sys, glob
import numpy as np

from typing import List, Dict, Any, Callable, Tuple
import iopolymc as io


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python %s evaltype path disc_len [omit_frac]" %sys.argv[0])
        sys.exit(0)

    print_status=True

    evaltype = sys.argv[1]
    path     = sys.argv[2]
    disc_len = float(sys.argv[3])
    omit_frac = 0
    if len(sys.argv) > 4:
        omit_frac = float(sys.argv[4])

    if evaltype.lower() in ['ceff','both','all']:
        data = io.eval_endlink(
            path,
            forces=None,
            disc_len=disc_len,
#            omit_frac=omit_frac,
            print_status=print_status
        )
        print(data.shape)
    if evaltype.lower() in ['ext','both','all','extension']:
        data = io.eval_force_extension(
            path,
            forces=None,
            disc_len=disc_len,
#           omit_frac=omit_frac,
            print_status=print_status
        )
        print(data.shape)