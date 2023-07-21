import numpy as np
import sys, os
import glob
from typing import List, Dict, Any
from .simplest_type import simplest_type

"""
########################################################


   
########################################################
"""


def read_input(filename: str) -> Dict[str, Any]:
    """
    Reads PolyMC input file and returns dictionary of contained arguments
    """
    args = dict()
    with open(filename, "r") as f:
        all_lines = f.readlines()
        dlines = [
            line.strip()
            for line in all_lines
            if len(line.strip()) > 0 and line.strip()[0] != "#"
        ]
        for line in dlines:
            if "=" not in line:
                continue
            argname = line.split("=")[0].strip()
            argstr = "=".join(line.split("=")[1:]).strip()
            arglist = [arg.strip() for arg in argstr.split(" ")]
            if len(arglist) == 1:
                args[argname] = simplest_type(arglist[0])
            else:
                args[argname] = simplest_type(arglist)
    return args


def write_input(filename: str, args: Dict[str, Any]):
    """
    Writes PolyMC input file given a dictionary containing the arguments. Argument names are specified by
    the keys.
    """
    ml = np.max([len(key) for key in args.keys()])
    with open(filename, "w") as f:
        for key in args.keys():
            elems = args[key]
            wstr = key.ljust(ml + 1) + "="
            if type(elems) is list:
                for elem in elems:
                    wstr += f" {elem}"
            else:
                wstr += f" {elems}"
            f.write(wstr + "\n")


########################################################
########################################################
########################################################
# query simulations


def querysims(
    path: str,
    select: Dict[str, Any] | None = None,
    recursive=False,
    extension="in",
    sims: List[Dict[str, Any]] | None = None,
) -> List[dict]:
    """
    Queries directory and subdirectories (if recursive=True), for simulations and ready the input. Specified simulations
    can be selected by passing a parameter dictionary via the argument select.
    """
    if sims is None:
        sims = _init_querysims(path, recursive=recursive, extension=extension)
    if select is not None:
        if not isinstance(select, dict):
            raise TypeError(
                f"Error in querysims: argument select needs to be a dictionary"
            )
        selected = list()
        for sim in sims:
            match = True
            for key in select.keys():
                if key not in sim.keys():
                    # raise exception if specified argument is not contained in input file
                    raise ValueError(
                        f"The argument '{key}' is not contained in the inputfile '{sim['input']}'"
                    )
                if sim[key] != select[key]:
                    match = False
                    break
            if match:
                selected.append(sim)
        sims = selected
    return sims


def _init_querysims(path: str, recursive=False, extension="in") -> List[dict]:
    """
    finds and reads all PolyMC input files and identifies other files belonging to the corresponding simulation.
    returns list of dictionary, one dictionary for each simulation. The other corresponding simulation files are contained in
    the dictionary under the key 'files'
    """
    infiles = list()
    if recursive:
        subpaths = [path] + _fast_scandir(path)
        for subpath in subpaths:
            infiles += glob.glob(os.path.join(subpath, "*." + extension))
    else:
        infiles += glob.glob(os.path.join(path, "*." + extension))

    sims = list()
    for infile in infiles:
        siminput = read_input(infile)
        files = simfiles(infile)
        siminput["input"] = infile
        siminput["files"] = files
        sims.append(siminput)
    return sims

def simfiles(infile: str, extension="in") -> List[str]:
    basefn = infile.replace("." + extension, "")
    allfns = glob.glob(basefn + ".*")
    return allfns



########################################################
########################################################
########################################################
# extra funcs


def _fast_scandir(path: str) -> List[str]:
    subpaths = [f.path for f in os.scandir(path) if f.is_dir()]
    for path in list(subpaths):
        subpaths.extend(_fast_scandir(path))
    return subpaths


########################################################
########################################################
########################################################
# testing

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python %s filename" % sys.argv[0])
        sys.exit(0)
    # fn  = sys.argv[1]

    # args = read_input(fn)
    # for key in args.keys():
    #     print(f'{key}: {args[key]} ({type(args[key])})')

    path = sys.argv[1]
    print(path)
    sims = querysims(path, recursive=True, extension="in")
    # for sim in sims:
    #     print(sim)
