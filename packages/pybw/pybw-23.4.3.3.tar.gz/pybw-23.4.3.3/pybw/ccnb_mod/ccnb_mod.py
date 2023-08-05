# -*- coding: utf-8 -*-
"""
Modified version of ccnb main.py
"""
import argparse
from pathlib import Path
from ccnb import cal_channel_cavd
from ccnb import get_bvse
from ccnb import get_migration_networks_voids

import os, time, shutil, re
from glob import glob
from pymatgen.core.structure import Structure as Structure_pmg
from pymatgen.analysis.bond_valence import BVAnalyzer


def get_voids(filename_CIF,
              energythreshold,
              moveion,
              mergecluster=True,
              clusterradii=0.75, 
              filename_CAVD=None, 
              filename_BVSE=None):
    """
    Get migration networks voids base on cal result of cavd and bvse
    
    Args:
        filename_CIF: cif filename. Used to give crastal structure and 
                      auto find filename_CAVD and filename_BVSE
        energythreshold: energythreshold
        moveion: move ion
    
    Returns:
        get_migration_networks_voids()
    """
    filename_CIF = Path(filename_CIF)
    if not filename_CAVD:
        filename_CAVD = str(filename_CIF.parent.joinpath(
            filename_CIF.stem)) + ".net"
    if not filename_BVSE:
        filename_BVSE = str(filename_CIF.parent.joinpath(
            filename_CIF.stem)) + "_BVSE.npy"
    
    if not Path(filename_CAVD).exists():
        print('{} file no exist,\n please cavd calculate first'.format(
            filename_CAVD))
        return None
    if not Path(filename_BVSE).exists():
        print('{} file no exist,\n please bvse calculate first'.format(
            filename_BVSE))
        return None
    
    mn = get_migration_networks_voids(str(filename_CIF),
                                      filename_BVSE,
                                      filename_CAVD,
                                      energythreshold,
                                      moveion=moveion,
                                      mergecluster=mergecluster,
                                      clusterradii=clusterradii)
    return mn


def get_argparse():
    """
    Old version program's function main
    Now it is changed to obtain argparse
    
    Returns:
        argparse.ArgumentParser()
    """
    parser = argparse.ArgumentParser(description='ccnb (mod ver. by pbw)')
    
    parser.add_argument('-f',
                        '-file',
                        '--structure_file',
                        dest='struct_file',
                        type=str,
                        default='',
                        required=False,
                        help='结构文件名 (compatible cif, POSCAR)')
    parser.add_argument('-i',
                        '-ion', 
                        '--move_ion',
                        dest='ion',
                        type=str,
                        default='Li',
                        required=False,
                        help='迁移离子类型')
    parser.add_argument('-c',
                        '-cal', 
                        '-mode', 
                        '-cal_type', 
                        '--calculation_type',
                        dest='cal_type',
                        type=str,
                        default='bvse',
                        choices=['bvse', 'cavd', 'find_voids', 'all'],
                        required=False,
                        help='计算类型选择')
    parser.add_argument('-p', 
                        '-pack',
                        '--pack',
                        dest='pack',
                        type=str,
                        default='True',
                        help='是否打包整理计算结果文件')
    
    bvse = parser.add_argument_group('bvse')
    bvse.add_argument('-v',
                      '-valence', 
                      '--valence',
                      type=float,
                      default=1,
                      dest='valence',
                      help='迁移离子化合价')
    bvse.add_argument('-r',
                      '-res', 
                      '-resolution', 
                      '--resolution',
                      type=float,
                      default=0.5,
                      dest='resolution',
                      help='计算区域分辨率（单位埃）')
    
    cavd = parser.add_argument_group('cavd')
    cavd.add_argument('--ntol',
                      dest='ntol',
                      type=float,
                      default=0.02,
                      help='计算容限')
    cavd.add_argument('--radius_flag',
                      dest='rad_flag',
                      type=str,
                      default='True',
                      help='几何分析时是否考虑离子半径')
    cavd.add_argument('-l',
                      '--lower',
                      dest='lower',
                      type=float,
                      default=0.5,
                      help='通道大小下限值(单位埃)')
    cavd.add_argument('-u',
                      '--upper',
                      dest='upper',
                      type=float,
                      default=1.0,
                      help='通道大小上限值(单位埃)')

    find_voids = parser.add_argument_group('find_voids')
    find_voids.add_argument('-e', 
                            '-energy', 
                            '--energy',
                            dest='energy',
                            type=float,
                            default=0.5,
                            help='能量筛选上限')
    find_voids.add_argument('-cluster', 
                            '--cluster',
                            dest='cluster',
                            type=str,
                            default='True',
                            help='是否进行合并团簇间隙点')
    find_voids.add_argument('-cr',
                            '-c_rad', 
                            '-clu_rad', 
                            '--cluster_radii',
                            dest='cluster_radii',
                            type=float,
                            default=0.75,
                            help='合并团簇范围半径')
    """
    args = parser.parse_args()
    if args.cal_type == 'cavd':
        RT = cal_channel_cavd(args.struct_file,
                              migrant=args.ion,
                              ntol=args.ntol,
                              rad_flag=args.rad_flag,
                              lower=args.lower,
                              upper=args.upper,
                              rad_dict=None)
        print(RT)
    if args.cal_type == 'bvse':
        barrier = get_bvse(args.struct_file,
                           moveion=args.ion,
                           valenceofmoveion=args.valence,
                           resolution=args.resolution)
        print(barrier)
    if args.cal_type == 'find_voids':
        mn = get_voids(filename_CIF=args.struct_file,
                       energythreshold=args.energy,
                       moveion=args.ion,
                       mergecluster=args.cluster,
                       clusterradii=args.cluster_radii)
        if mn:
            print(mn)
        else:
            print('Calculation failed!!!')
    """
    return parser


class CCNBCal():
    """
    Execute ccnb cal
    
    Attributes:
        (Including all attributes for cavd, bvse, ccnb)
        cal_type: 'cavd', 'bvse', 'find_voids', 'all'
        cal_now: whether cal immediately
        pack: whether pack result files after cal
        args: easy way to get all related args
    """
    def __init__(self, 
                 file='', 
                 ion='Li', 
                 valence=1, 
                 resolution=0.5, 
                 lower=0.5, 
                 upper=1.0, 
                 ntol=0.02, 
                 rad_flag=True, 
                 cutoff_energy=0.5, 
                 cluster=True, 
                 cluster_radii=0.75, 
                 cal_type='all', 
                 cal_now=True, 
                 pack=True, 
                 args=None):
        self.args = args
        if self.args:
            self.cal_type = self.args.cal_type
            # print('\npara pack of args: {}\n'.format(self.args.pack))
            self.pack = self.args.pack
            self.pack = False if str(self.pack) == 'False' else True
            
            self.file_origin = self.args.struct_file
            self.ion = self.args.ion
            self.valence = self.args.valence
            self.resolution = self.args.resolution
            
            self.lower = self.args.lower
            self.upper = self.args.upper
            self.ntol = self.args.ntol
            self.rad_flag = self.args.rad_flag
            
            self.cutoff_energy = self.args.energy
            self.cluster = self.args.cluster
            self.cluster_radii = self.args.cluster_radii
        else:
            self.cal_type = cal_type
            self.pack = pack
            
            self.file_origin = file
            self.ion = ion
            self.valence = valence
            self.resolution = resolution
            
            self.lower = lower
            self.upper = upper
            self.ntol = ntol
            self.rad_flag = rad_flag
            
            self.cutoff_energy = cutoff_energy
            self.cluster = cluster
            self.cluster_radii = cluster_radii
        
        self.prepare()
        
        if cal_now:
            self.cal_all()
        
    def prepare(self):
        self.task_state = {'continue': False, 'cavd': False, 
                           'bvse': False, 'find_voids': False}
        has_prefix = re.findall('^ccnb_[\d-]+--', Path(self.file_origin).name)
        if has_prefix:
            self.task_state['continue'] = True
            self.prefix = has_prefix[0]
            self.file = self.file_origin
            
            self.file_cavd = os.path.splitext(self.file)[0] + '.net'
            self.file_bvse = os.path.splitext(self.file)[0] + '_BVSE.npy'
            if os.path.exists(self.file_cavd):
                self.task_state['cavd'] = True
            if os.path.exists(self.file_bvse):
                self.task_state['bvse'] = True
        else:
            self.prefix = 'ccnb_' + time.strftime('%y%m%d%H%M') + '--'
            self.file = Path(self.file_origin).parent.joinpath(
                self.prefix + Path(self.file_origin).name).__str__()
            shutil.copy2(self.file_origin, self.file)
            
            stru = Structure_pmg.from_file(self.file)
            state = {'has_oxi_state': True, 'is_ordered': True}
            if not all(hasattr(ele, 'oxi_state') for site in stru 
                       for ele in site.species):
                state['has_oxi_state'] = False
                stru.remove_oxidation_states()
                stru = BVAnalyzer().get_oxi_state_decorated_structure(stru)
            if not stru.is_ordered:
                state['is_ordered'] = False
                from pymatgen.transformations.standard_transformations import \
                    OrderDisorderedStructureTransformation as ODST
                try:
                    stru = ODST().apply_transformation(stru)
                except:
                    raise Exception('\nThis disorder structure can not be '
                                    'transformed to ordered structure\n'
                                    'Please check the cif or try to order it '
                                    'throungh other ways\n')
            self.file = os.path.splitext(self.file)[0]
            if not state['has_oxi_state']:
                self.file = self.file + '-add_oxi_state'
            if not state['is_ordered']:
                self.file = self.file + '-ordered'
            self.file = self.file + '.cif'
            stru.to(fmt='cif', filename=self.file)
    
    def pack_files(self):
        dire = Path(self.file_origin).parent.joinpath(Path(self.file).stem)
        files = glob(r'{}/{}*'.format(Path(self.file).parent, self.prefix))
        os.makedirs(dire)
        for file in files:
            new = Path(file).name.lstrip(self.prefix)
            shutil.move(file, Path(dire).joinpath(new))
    
    def cal_cavd(self):
        RT = cal_channel_cavd(self.file,
                              migrant=self.ion,
                              ntol=self.ntol,
                              rad_flag=self.rad_flag,
                              lower=self.lower,
                              upper=self.upper,
                              rad_dict=None)
        print(RT)
    
    def cal_bvse(self):
        barrier = get_bvse(self.file,
                           moveion=self.ion,
                           valenceofmoveion=self.valence,
                           resolution=self.resolution)
        print(barrier)
    
    def cal_voids(self):
        mn = get_voids(filename_CIF=self.file,
                       energythreshold=self.cutoff_energy,
                       moveion=self.ion,
                       mergecluster=self.cluster,
                       clusterradii=self.cluster_radii, 
                       filename_CAVD=None, 
                       filename_BVSE=None)
        if mn:
            print(mn)
        else:
            print('\nCaution: Calculation failed\n')
    
    def cal_all(self):
        if self.cal_type.lower() == 'cavd':
            self.cal_cavd()
        elif self.cal_type.lower() == 'bvse':
            self.cal_bvse()
        elif self.cal_type.lower() == 'find_voids':
            self.cal_voids()
        elif self.cal_type.lower() in ['all']:
            if not self.task_state['cavd']:
                print('\n\n{0}\n[Step 01] cavd\n{0}\n'.format('-'*60))
                self.cal_cavd()
            if not self.task_state['bvse']:
                print('\n\n{0}\n[Step 02] bvse\n{0}\n'.format('-'*60))
                self.cal_bvse()
            print('\n\n{0}\n[Step 03] find_voids\n{0}\n'.format('-'*60))
            self.cal_voids()
        if self.pack:
            self.pack_files()


class Parameter():
    def __init__(self, dic):
        self.dic = dic
        
        for k, v in self.dic.items():
            setattr(self, k, v)
    
    def __repr__(self):
        return '<Parameter Storage>'


def receive_input():
    print('\n ****************************\n'
            ' *                          *\n'
            ' *         CCNB Mod         *\n'
            ' *      ver. 23.3.15.1      *\n'
            ' *                          *\n'
            ' ****************************\n'
            ' [Special for A-SOUL AVA]\n')
            
    # print('\n+--------------------------+\n'
            # '|                          |\n'
            # '|         CCNB Mod         |\n'
            # '|      ver. 23.3.15.1      |\n'
            # '|                          |\n'
            # '+--------------------------+\n'
            # '[Special for A-SOUL AVA]\n')

    print('\nParameters for cal control')
    print('    [cal_type: cavd; bvse; find_voids; all]')
    cal_type = input('    cal_type [all] = ').strip().lower()
    pack = input('    pack [True] = ').strip()
    
    print('\nParameters for BVSE')
    file = input('    Structure file [first cif file] = ').strip()
    ion = input("    ion ['Li'] = ").strip()
    valence = input('    valence [1] = ').strip()
    resolution = input('    resolution [0.5] = ').strip()
    print('\nParameters for CAVD')
    lower = input('    lower [0.5] = ').strip()
    upper = input('    upper [1.0] = ').strip()
    ntol = input('    ntol [0.02] = ').strip()
    rad_flag = input('    rad_flag [True] = ').strip()
    print('\nParameters for get_networks_voids')
    cutoff_energy = input('    cutoff_energy [0.5] = ').strip()
    cluster = input('    cluster [True] = ').strip()
    cluster_radii = input('    cluster_radii [0.75] = ').strip()
    print('\n{}\n'.format('-' * 60))
    
    paras = {}
    paras['cal_type'] = cal_type if cal_type else 'all'
    paras['pack'] = False if pack.strip() == 'False' else True
    paras['file'] = (file if file else 
                     (glob('*.cif')[0] if glob('*.cif') else ''))
    paras['struct_file'] = paras['file']
    paras['ion'] = ion if ion else 'Li'
    paras['valence'] = float(valence) if valence else 1
    paras['resolution'] = float(resolution) if resolution else 0.5
    paras['lower'] = float(lower) if lower else 0.5
    paras['upper'] = float(upper) if upper else 1.0
    paras['ntol'] = float(ntol) if ntol else 0.02
    paras['rad_flag'] = False if rad_flag.strip() == 'False' else True
    paras['cutoff_energy'] = float(cutoff_energy) if cutoff_energy else 0.5
    paras['energy'] = paras['cutoff_energy']
    paras['cluster'] = False if cluster.strip() == 'False' else True
    paras['cluster_radii'] = float(cluster_radii) if cluster_radii else 0.8
    print('\nParameters: {}\n'.format(paras))
    return Parameter(paras)


def main():
    parser = get_argparse()
    if not parser.parse_args().struct_file:
        paras = receive_input()
        ccnb_cal = CCNBCal(args=paras)
    else:
        args = parser.parse_args()
        print('\nParameters: {}\n'.format(args))
        ccnb_cal = CCNBCal(args=args)


if __name__ == '__main__':
    main()
    