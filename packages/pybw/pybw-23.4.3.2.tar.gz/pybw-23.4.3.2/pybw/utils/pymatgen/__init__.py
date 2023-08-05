# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2023.03.01
version: 2023.03.01
function: Some useful tools
"""

from pybw.tricks.lazy_import import *

__author__ = 'Bowei Pu'
__version__ = '2023.03.14'
__maintainer__ = 'Bowei Pu'
__email__ = 'pubowei@foxmail.com'
__status__ = 'Beta'
__date__ = '2023-03-14'



def get_oxi_string(oxi_state):
    s = '\nloop_\n_atom_type_symbol\n_atom_type_oxidation_number\n'
    for k, v in oxi_state.items():
        v = int(v) if isinstance(v, int) or v.is_integer() else float(v)
        s += '{} {}\n'.format(k, v)
    return s + '\n'


def read_possible_species(species):
    """Convert possible_species list string of doc to dict
    
    Args:
        species: possible_species, list of string
                 Eg., ['Li+', 'La3+', 'Zr4+', 'O2-']
    
    Note:
        In some possible_species, one element may have more than one possible
        specie, this will make problem when apply it to add stru's oxi state. 
        Thus, the valence given by possible_species should be used with caution.
        Eg., mp-761342 'Li4 Co2 Cu3 Sb3 O16', possible_species is ['Li+', 
        'Sb5+', 'O2-', 'Cu2+', 'Cu3+', 'Co3+']. Here, Cu has two oxi state +2
        and +3
    """
    oxi = {}
    for specie in species:
        elem = re.findall('[a-zA-Z]+', specie)[0]
        sign = re.findall('[+-]', specie)[0]
        numb = re.findall('\d+', specie)
        numb = numb[0] if numb else '1'
        valence = Decimal(sign + numb)
        oxi[elem] = valence
    return oxi


class MPR():
    """
    Easy usage of MPRester
    """
    def __init__(self, key=''):
        self.key = (self.initial_mp_api_key() if self.initial_mp_api_key() 
                    else 'yDipjnlj15dOmxetQgkhzcHGRPsBHczc')
        
        self.mpr = MPRester(self.key)
        self.database_version = self.mpr.get_database_version()
    
    def search(self, **kwargs):
        docs = self.mpr.summary.search(**kwargs)
        docs.sort(key=lambda x: int(x.material_id.split('-')[1]))
        docs = [DictDoc(i.dict()) for i in docs]
        for doc in docs:
            doc.setattr('database_version', self.database_version)
        return docs

    @classmethod
    def initial_mp_api_key(csl, key: str=''):
        key = str(key).strip()
        if not key:
            key_files = []
            for p in ['C:/', os.path.expanduser('~'), 
                    os.path.expanduser('~') + '/Desktop']:
                for file in os.listdir(p):
                    file = os.path.join(p, file)
                    if os.path.isfile(file):
                        if re.search('mp_api_key', file.lower()):
                            key_files.append(file)
            key_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            keys = []
            for file in key_files:
                with open(file, 'r') as f:
                    c = [i.strip() for i in f.readlines() if len(i.strip()) == 32]
                    keys.extend(c)
            if not keys:
                key = 'yDipjnlj15dOmxetQgkhzcHGRPsBHczc'
                return key
            key = keys[0]
            return key
        return key


class DictDoc():
    '''
    Dict to class
    Designed to compatible with MPDoc
    '''
    def __init__(self, dic: dict={}):
        self.dic = dic
        self._generate_attributes()
    
    def __repr__(self):
        if hasattr(self, 'structure'):
            return '<DictDoc: {}>'.format(self.structure.formula)
        else:
            return '<DictDoc: >'
    
    def __str__(self):
        return self.__repr__()
        
    def dict(self):
        return self.dic
    
    def as_dict(self):
        return self.dic
    
    def keys(self):
        return self.dic.keys()
    
    def values(self):
        return self.dic.values()
    
    def _generate_attributes(self):
        for k, v in self.dic.items():
            setattr(self, k, v)
    
    def setattr(self, name, value):
        self.dic[name] = value
        setattr(self, name, value)
    
    def add(self, name, value):
        self.setattr(name, value)
    
    def get_light_doc(self, reserve=[]):
        reserves = ['formula_pretty', 'formula_anonymous', 'chemsys',
                    'property_name', 'material_id', 'es_source_calc_id',
                    'ordering', 'database_version']
        reserves += ['nsites', 'nelements', 'num_magnetic_sites', 
                     'num_unique_magnetic_sites']
        reserves += ['volume', 'density', 'density_atomic',
                     'uncorrected_energy_per_atom', 'energy_per_atom',
                     'formation_energy_per_atom', 'energy_above_hull',
                     'band_gap', 'cbm', 'vbm', 'efermi',
                     'total_magnetization',
                     'total_magnetization_normalized_vol',
                     'total_magnetization_normalized_formula_units']
        reserves += ['deprecated', 'is_stable', 'is_gap_direct',
                     'is_metal',  'is_magnetic', 'theoretical']
        reserves += ['elements', 'composition', 'composition_reduced', 
                     'decomposes_to', 'symmetry', 'structure', 'task_ids', 
                     'possible_species', 
                     'guess_oxi_states', 'oxi_states']
        reserves += reserve
        return self.__class__({i: self.__getattribute__(i) 
                               for i in reserves if i in self.__dir__()})


class StructureSaveCif():
    """
    Save Structure to cif
    
    Attributes:
        structure: pymatgen Structure
        symprec: if not symprec, spg info will be given by guess
    """
    def __init__(self, structure, symprec=None):
        self.structure = structure
        self.symprec, self.spg_no, self.spg_symbol = self._get_symprec_info(symprec)

    def _get_symprec_info(self, symprec):
        if isinstance(symprec, int) or isinstance(symprec, float):
            spg_info = self.structure.get_space_group_info(symprec)
            symprec_info = [symprec, spg_info[1], spg_info[0]]
        else:
            symprec_info = self.get_space_group_info()[0]
        return symprec_info

    def get_space_group_info(self):
        lattice = self.structure.lattice.matrix
        positions = self.structure.frac_coords
        numbers = [site.specie.number for site in self.structure.sites]
        cell = (lattice, positions, numbers)
        symprecs = [0.01] + [round(i, 2) for i in np.arange(0.1, 1.51, 0.1)]
        _spg_info = []
        for i in symprecs:
            _info = spglib.get_symmetry_dataset(cell=cell, symprec=i)
            if not _info:
                break
            _info = [i, _info['number'], _info['international']]
            _spg_info.append(_info)
        spg_info = []
        _spg_num = []
        for i in _spg_info:
            if i[1] not in _spg_num:
                _spg_num.append(i[1])
                spg_info.append(i)
        if spg_info[0][1] == 1 and len(spg_info >= 2):
            spg_info = spg_info[1:]
        return spg_info
    
    def save_cif(self, filename=''):
        if not filename:
            formula = self.structure.formula.replace(' ', '')
            filename = '{}-spg_{}-{}.cif'.format(formula, self.spg_no, 
                                                 time.strftime('%y%m%d_%H%M'))
        self.structure.to(fmt='cif', filename=filename, symprec=self.symprec)



