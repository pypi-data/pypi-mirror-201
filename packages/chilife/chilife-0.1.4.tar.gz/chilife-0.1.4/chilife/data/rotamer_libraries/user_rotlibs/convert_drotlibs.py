import pickle, json
import numpy as np
import chilife as xl
from pathlib import Path
import zipfile, os

with open('../spin_atoms.json', 'r') as f:
    spin_atoms = json.load(f)


def convert_library(libname):
    with open(f'../residue_internal_coords/{libname}C_ic.pkl', 'rb') as f:
        cst_idxs, csts = pickle.load(f)

    save_dict = {'cst_pairs': cst_idxs, 'cst_distances': csts}
    np.savez(f'{libname}_csts.npz', **save_dict)

    with zipfile.ZipFile(f'{libname}_drotlib.zip', mode='w') as archive:
        archive.write(f'{libname}A_rotlib.npz')
        archive.write(f'{libname}B_rotlib.npz')
        archive.write(f'{libname}_csts.npz')

        # Cleanup intermediate files
    # os.remove(f'{libname}A_rotlib.npz')
    # os.remove(f'{libname}B_rotlib.npz')
    # os.remove(f'{libname}_csts.npz')


    # np.savez(library, **lib)

def add_to_library(libname):

    with zipfile.ZipFile(libname + '_drotlib.zip', 'r') as archive:
        archive.extractall()
    files = list(Path.cwd().glob(f'{libname}*.npz'))
    for file in files:
        if 'csts' not in file.name:
            with np.load(file, allow_pickle=True) as f:
                lib = dict(f)

            resname = libname[:3]

            lib['rotlib'] = libname + file.name[len(libname)]
            print(lib['rotlib'])
            lib['resname'] = resname
            spin_atoms = {'spin_atoms': ['Cu1'], 'spin_weights': ['1.0']}

            lib.update(spin_atoms)

            lib['type'] = 'chilife rotamer library'
            lib['format_version'] = 1.0

            np.savez(file, **lib)

    with zipfile.ZipFile(f'{libname}_drotlib.zip', mode='w') as archive:
        archive.write(f'{libname}A_rotlib.npz')
        archive.write(f'{libname}B_rotlib.npz')
        archive.write(f'{libname}_csts.npz')

    # Cleanup intermediate files
    os.remove(f'{libname}A_rotlib.npz')
    os.remove(f'{libname}B_rotlib.npz')
    os.remove(f'{libname}_csts.npz')


def adjust_library(libname):

    with zipfile.ZipFile(libname + '_drotlib.zip', 'r') as archive:
        archive.extractall()

    files = list(Path.cwd().glob(f'{libname}*.npz'))
    for file in files:
        if 'csts' not in file.name:
            with np.load(file, allow_pickle=True) as f:
                lib = dict(f)

                lib['spin_weights'] = lib['spin_weights'].astype(float)

            np.savez(file, **lib)

    with zipfile.ZipFile(f'{libname}_drotlib.zip', mode='w') as archive:
        archive.write(f'{libname}A_rotlib.npz')
        archive.write(f'{libname}B_rotlib.npz')
        archive.write(f'{libname}_csts.npz')

    # Cleanup intermediate files
    os.remove(f'{libname}A_rotlib.npz')
    os.remove(f'{libname}B_rotlib.npz')
    os.remove(f'{libname}_csts.npz')



# convert_library('DHCip2')
# convert_library('DHCip4')

# add_to_library('DHCip2')
# add_to_library('DHCip4')


adjust_library('DHCip2')
adjust_library('DHCip4')