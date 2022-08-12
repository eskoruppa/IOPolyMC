import os,sys
import json
import numpy as np
import pkg_resources

from iopolymc.state  import read_state

BPDICTS_FN = 'database/bpdicts'


def load_bpdicts(fn: str) -> dict:
    """
    Parameters:
    fn : str
        bpdict database

    Returns:
    dict - containing residue data
    """
    with open(fn, 'r') as f:
        bpdicts = json.load(f)
    return bpdicts


def DNA_residue_name(residue_name):
    if residue_name == "A":
        return "DA"
    if residue_name == "T":
        return "DT"
    if residue_name == "G":
        return "DG"
    if residue_name == "C":
        return "DC"
    return residue_name


def build_pdb_atomline(atomID: int,
                       atom_name: str,
                       residue_name: str,
                       strandID: str,
                       residueID: int,
                       atom_pos: list[float]) -> str:
    """
        generates pdb line for atom
    """
    pdbline = "ATOM  " + leftshiftstring(5, str(atomID)) + \
              " " + leftshiftstring(4, atom_name) + \
              " " + leftshiftstring(3, residue_name) + \
              " " + str(strandID) + leftshiftstring(4, str(residueID)) + \
              "    " + leftshiftstring(8,"%.3f" %atom_pos[0]) + \
              leftshiftstring(8, "%.3f" % atom_pos[1]) + \
              leftshiftstring(8, "%.3f" % atom_pos[2]) + " \n"
    return pdbline

def build_pdb_terline(atomID: int , residue_name: str, strandID: str, residueID: int) -> str:
    """
        generates TER line for pdb strand
    """
    pdbline = "TER   " + leftshiftstring(5, str(atomID)) + \
              " " + leftshiftstring(4, "") + \
              " " + leftshiftstring(3,residue_name) + \
              " " + str(strandID) + \
              leftshiftstring(4, str(residueID)) + "    \n"
    return pdbline


def leftshiftstring(total_chars: int, string: str) -> str:
    """
        fills spaces
    """
    chars = len(string)
    shifted_str = ""
    for i in range(total_chars - chars):
        shifted_str += " "
    return shifted_str + string

def rotate_z(triad: np.ndarray, phi: float) -> np.ndarray:
    """
        rotates triad over z axis by angle phi
    """
    R_z = np.zeros([3, 3])
    R_z[0, 0] = np.cos(phi)
    R_z[0, 1] = -np.sin(phi)
    R_z[1, 0] = R_z[0, 1]
    R_z[1, 1] = R_z[0, 0]
    R_z[2, 2] = 1
    return np.matmul(triad, R_z)


def random_sequence(N: int) -> list[str]:
    """
        generates random base sequence of length N
    """
    basetypes = ['A','T','C','G']
    return [basetypes[bt] for bt in np.random.randint(4, size=N)]

def discretization_length(conf: np.ndarray) -> np.ndarray:
    """ returns lengths of vectors """
    ndims = len(np.shape(conf))
    vecs  = np.diff(conf,axis=ndims-2)
    return np.mean(np.linalg.norm(vecs,axis=ndims-1))

def gen_pdb(outfn: str, positions: np.ndarray,triads: np.ndarray,bpdicts: dict, sequence = None, center=True):
    """

        positions needs to be in nm!
    """

    if len(positions.shape) > 2:
        raise ValueError(
            f"Wrong dimension provided for positions. Input needs to be a single configuration.")
    if len(triads.shape) > 3:
        raise ValueError(
            f"Wrong dimension provided for triads. Input needs to be a single configuration.")

    numbp = len(positions)


    # check if the discretization length is correct
    # this may be replaced in the future by allowing all discretization lengths
    disc_len = discretization_length(positions)
    if np.abs(disc_len-3.4)/3.4 > 0.1:
        # wrong discretization length
        raise ValueError(f"Discretization length needs to be 0.34 nm. Provided configuration has discretization length {disc_len} nm!")

    if sequence is None:
        sequence = random_sequence(numbp)

    if center:
        positions -= np.mean(positions,axis=0)

    with open(outfn, "w") as f:

        atomID = 0
        residueID = 0

        # STRAND A
        strandID     = "A"
        residue_name = ""
        for i in range(numbp):
            residueID += 1
            basetype   = sequence[i]
            triad      = triads[i]
            pos        = positions[i]

            bpdict       = bpdicts[basetype]
            residue      = bpdict['resA']
            residue_name = residue['resname']

            for atom in residue['atoms']:
                atomID += 1
                atom_name = atom['name']
                atom_pos  = atom['pos']
                # atom_pos = np.dot(atom_pos,triad) + pos
                atom_pos = np.dot(triad.T,atom_pos) + pos
                pdbline  = build_pdb_atomline(atomID, atom_name, residue_name, strandID, residueID, atom_pos)
                f.write(pdbline)

        pdbline = build_pdb_terline(atomID, residue_name, strandID, residueID)
        f.write(pdbline)

        # STRAND B
        strandID = "B"
        for i in range(numbp - 1, -1, -1):
            residueID += 1
            basetype   = sequence[i]
            triad      = triads[i]
            pos        = positions[i]

            bpdict       = bpdicts[basetype]
            residue      = bpdict['resB']
            residue_name = residue['resname']

            for atom in residue['atoms']:
                atomID += 1
                atom_name = atom['name']
                atom_pos = atom['pos']
                # atom_pos = np.dot( atom_pos,triad) + pos
                atom_pos = np.dot( triad.T,atom_pos) + pos
                pdbline = build_pdb_atomline(atomID, atom_name, residue_name, strandID, residueID, atom_pos)
                f.write(pdbline)
        pdbline = build_pdb_terline(atomID, residue_name, strandID, residueID)
        f.write(pdbline)

        f.close()





def state2pdb(statefn: str, outfn: str, snapshot: int ,bpdicts_fn=None, sequence=None, center=True):
    """
        Converts a snapshot from a polymc state file into pdb format

    Parameters:

    statefn : str
        filename of statefile
    outfn : str
        output filename
    snapshot : int
        index of selected snapshot
    bpdictsfn : str
        filename of basepair topology database. (default: None -> loads from standard database file)
    sequence : str
        sequence of reference strand bases
    center : bool
        Translates center of mass of configuration to origin if set to True (detault: True)
    """

    # load base pair database
    if bpdicts_fn is None:
        bpdicts_fn = pkg_resources.resource_filename(__name__, BPDICTS_FN)
    bpdicts = load_bpdicts(bpdicts_fn)

    # load state
    state  = read_state(statefn)
    conf   = state['pos']
    triads = state['triads']

    if snapshot >= len(conf):
        raise ValueError(f"State file only contains {len(conf)} snapshots. Chosen snapshot {snapshot} is out of range.")

    pos    = conf[snapshot]*10
    triads = triads[snapshot]
    gen_pdb(outfn, pos, triads, bpdicts, sequence=sequence)



if __name__ == "__main__":

    bpdicts_fn = pkg_resources.resource_filename(__name__, BPDICTS_FN)
    bpdicts = load_bpdicts(bpdicts_fn)

    # print(bpdicts)

    print(random_sequence(10))

    statefn = 'testdata/conf4pdb.state'

    state  = read_state(statefn)
    conf   = state['pos']
    triads = state['triads']

    snapshot = 1

    pos = conf[snapshot]
    # pos /= (2/0.34)
    triads = triads[snapshot]

    outfn = 'testdata/conf4pdb.pdb'

    # rescale to Angstrom
    pos *= 10
    gen_pdb(outfn, pos, triads, bpdicts, sequence = None)
