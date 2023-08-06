import pickle, json
import numpy as np
import chilife as xl
from pathlib import Path

with open('../spin_atoms.json', 'r') as f:
    spin_atoms = json.load(f)


def rotlib_check(lib):
    libname = lib['rotlib']
    if 'internal_coords' not in lib:
        print(f'INTERNAL COORDS MISSING: {libname}')
    elif len(lib['internal_coords']) != len(lib['weights']):
        print(f'INTERNAL COORDS WRONG LENGTH: {libname}')

    if not all(x in lib for x in xl.rotlib_formats[float(lib['format_version'])]):
        for x in xl.rotlib_formats[lib['format_version']]:
            if x not in lib:
                print(f'{x} not in lib')
        raise ValueError('The rotamer library does not contain all the required entries for the format version')
    elif 'spin_atoms' not in lib:
        print('MISSING SPIN ATOMS')
    else:
        print('success')


def convert_library(library):
    libname = library.name[:-11]
    resname = library.name[:3]

    with np.load(library, allow_pickle=True) as f:
        lib = dict(f)

    lib['rotlib'] = libname
    lib['resname'] = resname
    lib.update(spin_atoms[resname])

    lib['type'] = 'chilife rotamer library'
    lib['format_version'] = 1.0
    rotlib_check(lib)
    # np.savez(library, **lib)


def convert_ICs(library):
    resname = library.name[:3]

    with np.load(library, allow_pickle=True) as f:
        lib = dict(f)

    with open(f'../residue_internal_coords/{resname}_ic.pkl', 'rb') as f:
        internal_coords = pickle.load(f)

    if isinstance(internal_coords, xl.ProteinIC):
        print(resname)
        return None

    if len(internal_coords) == len(lib['internal_coords']):
        lib['internal_coords'] = internal_coords
    else:
        raise ValueError('IC rotlibs are not the same length')

    rotlib_check(lib)

    # np.savez(library, **lib)


for filename in Path.cwd().glob('*.npz'):
    # convert_library(filename)
    convert_ICs(filename)

