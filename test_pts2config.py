import numpy as np

import iopolymc as iopmc

"""
    Generate a trefoil knot
"""

if __name__ == "__main__":
    disc_len = 3.4
    numbp = 500

    # pts = list()
    # pts.append(np.array([0,0,0]))
    # pts.append(np.array([0,0,40]))
    # pts.append(np.array([0,10,40]))
    # pts.append(np.array([-5,10,30]))
    # pts.append(np.array([-5,-5,30]))
    # pts.append(np.array([5,-5,35]))
    # pts.append(np.array([5,5,35]))
    # pts.append(np.array([-5,5,35]))
    # pts.append(np.array([-5,5,45]))
    # pts.append(np.array([0,0,45]))
    # pts.append(np.array([0,0,80]))

    pts = list()
    pts.append(np.array([0, 0, 0]))
    pts.append(np.array([0, 0, 80]))
    pts.append(np.array([0, 40, 80]))
    pts.append(np.array([-20, 40, 40]))
    pts.append(np.array([-20, -20, 40]))
    pts.append(np.array([20, -20, 60]))
    pts.append(np.array([20, 20, 60]))
    pts.append(np.array([-20, 20, 60]))
    pts.append(np.array([-20, 20, 100]))
    pts.append(np.array([0, 0, 100]))
    pts.append(np.array([0, 0, 140]))

    pts = np.array(pts)
    pts *= 6
    # pts.append(np.array([2,2,82]))

    # config = pts2config(pts,disc_len,numbp=500)

    xyzfn = "test/trefoil_large.xyz"
    restartfn = "test/trefoil_large.restart"

    numbp = 800
    iopmc.pts2xyz(xyzfn, pts, disc_len, numbp=numbp)
    iopmc.pts2restart(restartfn, pts, disc_len, numbp=numbp)
