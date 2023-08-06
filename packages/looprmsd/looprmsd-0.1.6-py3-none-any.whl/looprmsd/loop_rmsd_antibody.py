import os
import numpy as np
from Bio.PDB import Superimposer, PDBParser, PDBIO, PPBuilder
from Bio.Data import SCOPData
from anarci import run_anarci

REGION_TO_RANGE={
    'H1': (26,32),
    'H2': (52,56),
    'H3': (95,102),
    'L1': (24,34),
    'L2': (50,56),
    'L3': (89,97),
}

def calculate_rotation_matrix(x, y):
    # center the points
    x = x - np.mean(x, axis=0)
    y = y - np.mean(y, axis=0)

    C = np.dot(x.T, y)
    # calculate rotation matrix
    V, S, Wt = np.linalg.svd(C)
    d = (np.linalg.det(V) * np.linalg.det(Wt)) < 0.0

    if d:
        S[-1] = -S[-1]
        V[:, -1] = -V[:, -1]

    # create rotation matrix U
    U = np.dot(V, Wt)

    return U


def compute_rmsd(P, Q, prune_threshold=None) -> float:
    """
    Calculate Root-mean-square deviation from two sets of vectors V and W.

    Parameters
    ----------
    V : array
        (N,D) matrix, where N is points and D is dimension.
    W : array
        (N,D) matrix, where N is points and D is dimension.

    Returns
    -------
    rmsd : float
        Root-mean-square deviation between the two vectors
    """
    diff = P - Q
    if prune_threshold is not None:
        diff = diff[np.linalg.norm(diff, axis=1) < prune_threshold]
    return np.sqrt((diff * diff).sum() / P.shape[0])



def pdb_rmsd(model_pdb, ref_pdb, chain1, chain2, loop_region=None, loop_seq=None, prune_threshold=None):
    """
    Calculate the RMSD between two PDB files.
    If one of the PDB files uses non-Chothia numbering, convert it to Chothia numbering using ANARCI.
    If an output filename is provided, write the aligned coordinates to the output PDB file.
    """
    assert loop_region is not None or loop_seq is not None, 'Either loop_region or loop_seq must be provided'
    # Parse the PDB files
    parser = PDBParser()
    structure1 = parser.get_structure('structure1', model_pdb)
    chain1 = structure1[0][chain1]
    structure2 = parser.get_structure('structure2', ref_pdb)
    chain2 = structure2[0][chain2]
    
    # Check if either structure uses non-Chothia numbering
    ppb = PPBuilder()
    seq1 = ''.join([str(pp.get_sequence()) for pp in ppb.build_peptides(chain1)])
    seq2 = ''.join([str(pp.get_sequence()) for pp in ppb.build_peptides(chain2)])

    _, numbering1, _, _ = run_anarci(seq1, scheme='chothia')
    terminal1 = numbering1[0][0][2]

    _, numbering2, _, _ = run_anarci(seq2, scheme='chothia')
    terminal2 = numbering2[0][0][2]

    assert terminal1 == terminal2, 'The two PDB files have different termini'
    
    # Get the coordinates of the C-alpha atoms
    if loop_region is not None:
        # chothia numbering
        if loop_region in ['H1', 'H2', 'H3', 'L1', 'L2', 'L3']:
            st, ed = REGION_TO_RANGE[loop_region]  
        else:
            st, ed = loop_region
        anchor_range = list(range(st-2,st))+list(range(ed+1, ed+3))

        # Seq Check; YPHYYGSSHWYFDV
        # ''.join([SCOPData.protein_letters_3to1.get(chain1.child_list[i].get_resname(),'X') for i, tup in enumerate(numbering1[0][0][0]) if tup[0][0] in range(st, ed+1)])

        loop_ca1 = [chain1.child_list[i]['CA'].get_coord() for i, tup in enumerate(numbering1[0][0][0]) if tup[0][0] in range(st, ed+1)]
        anchor_ca1 = [chain1.child_list[i]['CA'].get_coord() for i, tup in enumerate(numbering1[0][0][0]) if tup[0][0] in anchor_range]

        loop_ca2 = [chain2.child_list[i]['CA'].get_coord() for i, tup in enumerate(numbering2[0][0][0]) if tup[0][0] in range(st, ed+1)]
        anchor_ca2 = [chain2.child_list[i]['CA'].get_coord() for i, tup in enumerate(numbering2[0][0][0]) if tup[0][0] in anchor_range]


    elif loop_seq is not None:
        # non-chothia numbering - anarci not needed
        st = seq1.find(loop_seq)
        ed = st + len(loop_seq) -1
        anchor_range = list(range(st-2,st))+list(range(ed+1, ed+3))

        # Seq Check; YPHYYGSSHWYFDV
        # ''.join([SCOPData.protein_letters_3to1.get(chain1.child_list[i].get_resname(),'X') for i in range(st, ed+1)])

        loop_ca1 = [chain1.child_list[i]['CA'].get_coord() for i in range(st, ed+1)]
        anchor_ca1 = [chain1.child_list[i]['CA'].get_coord() for i in anchor_range]

        loop_ca2 = [chain2.child_list[i]['CA'].get_coord() for i in range(st, ed+1)]
        anchor_ca2 = [chain2.child_list[i]['CA'].get_coord() for i in anchor_range]


    assert len(loop_ca1) == len(loop_ca2), 'The two PDB files have different loop lengths'
    assert len(anchor_ca1) == len(anchor_ca2), 'The two PDB files have different anchor lengths'

    # Align the structures
    center1 = np.mean(anchor_ca1, axis=0)
    center2 = np.mean(anchor_ca2, axis=0)
    rot = calculate_rotation_matrix(
        anchor_ca1 - center1, anchor_ca2 - center2)

    # Return loop RMSD
    rmsd = compute_rmsd(loop_ca2 - center2, (loop_ca1 - center1) @ rot, prune_threshold=prune_threshold)

    return rmsd


if __name__ == "__main__":
    model_pdb = 'dat/1bj1_HL_H3_pred.pdb'
    ref_pdb = 'dat/1bj1.pdb'
    # rmsd = pdb_rmsd(model_pdb, ref_pdb, 'H', 'H', loop_region='H3')  #0.5385195760350145
    rmsd = pdb_rmsd(model_pdb, ref_pdb, 'H', 'H', loop_seq='YPHYYGSSHWYFDV')  #0.5385195760350145
    print(rmsd)