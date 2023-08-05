# -*- coding: utf-8 -*-
'''
modify author: Bowei Pu
version: 2022.08.17
note: This is a modified module from BVSE program by Bing He
function: __init__ class of bvseLi
'''
import os
import time
from pathlib import Path
import shutil
from pickle import NONE
import ase.io
from rich.progress import Progress

import bvseLi.Structure as Structure
import bvseLi.BVAnalysis as BVAnalysis
import bvseLi.BVAnalysisLi as BVAnalysisLi


class Progressbar:

    def __init__(self):
        self.progress = Progress()
        self.task = None

    def set_task(self, workstr: str, total):
        self.task = self.progress.add_task(workstr, total)

    def updatetask(self, i: int):
        self.progress.update(self.task, advance=0.9)
        print('    bvse computing  {0:.2f}%'.format(i))


def time_used(time0, if_print=False, return_type='tuple'):
    dt = int(time.time() - time0)
    h, m, s = dt // 3600, dt // 60 % 60, dt % 60
    if if_print:
        print('    time used: {:0>2}h {:0>2}m {:0>2}s'.format(h, m, s))
        # print('    time used: {:0>2}:{:0>2}:{:0>2}'.format(h, m, s))
    if return_type.lower() in ['default', 'normal', 'tuple', 'list']:
        return h, m, s
    elif return_type.lower() in ['dic']:
        return {'h': h, 'm': m, 's': s}
    else:
        return


def time_used_old(time0, if_print=False):
    dt = time.time() - time0
    sec = int(dt)
    mins = round(sec / 60, 2)
    hour = round(sec / 60 / 60, 2)
    if if_print:
        print('    time used: {} h, {} m, {} s'.format(hour, mins, sec))
    dic = {'h': hour, 'm': mins, 's': sec}
    return dic


class OsPath():
    '''
    '''
    def __init__(self, file):
        self.file = file
        
        self.path = self.abspath = os.path.abspath(self.file)
        self.parent, self.name = os.path.split(self.abspath)
        self.dirname, self.basename, self.filename = self.parent, self.name, self.name
        self.stem, self.suffix = os.path.splitext(self.name)
        self.path_stem = self.abs_stem = os.path.splitext(self.abspath)[0]
        
        self.str = self.string = self.abspath
        self.posix = self.as_posix()
    
    def __str__(self):
        return self.abspath
    
    def __repr__(self):
        return self.__str__()
    
    def __fspath__(self):
        return self.abspath
    
    def absolute(self):
        return self.abspath
    
    def as_posix(self):
        return Path(self.abspath).as_posix()
    
    @staticmethod
    def get_posix(cls, path):
        return Path(path).as_posix()
    
    def join(self, other: str):
        return self.__class__(os.path.join(self.abspath, other))
    
    def joinpath(self, other: str):
        return self.join(other)
    
    @property
    def exists(self):
        return os.path.exists(self.abspath)
        
    @property
    def isfile(self):
        return os.path.isfile(self.abspath)
    
    @property
    def isdir(self):
        return os.path.isdir(self.abspath)
    
    def rename(self, new_name):
        return self.__class__(os.path.join(self.dirname, new_name))


def bv_calculation(filename,
                   moveion='Li',
                   valenceofmoveion=1,
                   resolution=0.1,
                   progress=None, 
                   Rmin_moveion=3, 
                   engine='bvseLi',
                   pack_files=True, 
                   skip_done=True, 
                   rename_cif=True
                  ):
    '''
    Convenient function to apply BVSELi calculation
    
    Args:
        filename: file path
        moveion: mobile ion
        valenceofmoveion: valence of mobile ion
        resolution: resolution
        progress: whether desplay progress bar when cal
        Rmin_moveion: Rmin cutoff to judge whether cal nearby mobile ion
        engine: choose different bv method. 'bvse' or 'bvseLi'
        pack_files: if pack output files after calculation
        skip_done: if skip .cif file which is startswith 'done--'
        rename_cif: if rename '*.cif' file to 'done--*.cif' after calculation
    
    Returns:
        bvs.Ea['BVSE']
    
    Outputs:
        .npy: Data for numpy load
        .pgrid: Grid data for VESTA
        .grd: Grd data
        INFO.csv: Log to record related info, include filename, res, Rmin, Ea and etc.
    '''
    if skip_done:
        if Path(filename).name.startswith('done--'):
            return
    
    if not progress or progress.lower() in ['default', 'auto']:
        prgbar = Progressbar()
        prgbar.set_task('bvse computing progress...', total=100)
        progress = prgbar.updatetask
    
    if engine.lower() in ['default', 'normal', 'bvse']:
        engine = 'bvse'
    elif engine.lower() in ['bvseli']:
        engine = 'bvseli'
    
    atoms = ase.io.read(filename, store_tags=True)
    struc = Structure.Structure()
    struc.GetAseStructure(atoms)
    
    if engine == 'bvse':
        bvs = BVAnalysis.BVAnalysis()
        BVMethod = 'BVSE'
    elif engine == 'bvseli':
        bvs = BVAnalysisLi.BVAnalysis()
        BVMethod = 'BVSELi'
    
    bvs.SetStructure(struc)
    bvs.SetMoveIon(moveion)
    bvs.ValenceOfMoveIon = valenceofmoveion
    bvs.SetLengthResolution(resolution)
    
    time0 = time.time()
    progress = None
    if engine == 'bvse':
        bvs.CaluBVSE(progress)
    elif engine == 'bvseli':
        bvs.CaluBVSE(progress, Rmin_moveion)
    time_info = time_used(time0, if_print=False, return_type='dic')
    
    file = OsPath(filename)
    file_name = Path(filename).name
    filepath = os.path.abspath(filename)
    filepath_dire = os.path.split(filepath)[0]
    filepath_stem = os.path.splitext(filepath)[0]
    
    bvs.SaveBVSEData(file.abs_stem)
    bvs.SaveBVELData(file.abs_stem)
    bvs.SaveBVSData(file.abs_stem)
    
    bv_data = bvs.get_data()
    bvs.SaveData('{}_BVSELi.grd'.format(file.abs_stem), bv_data['BVSE'], 'BVSE')
    
    with open('{}_INFO.csv'.format(file.abs_stem), 'w') as f:
        f.write('filename,resolution,Rmin_moveion,Ea_BVSE,time_used\n')
        _BVSE_Ea = [round(i, 2) for i in bvs.BVSEEa]
        _BVSE_Ea = '[{}]'.format(' '.join([str(i) for i in _BVSE_Ea]))
        _time_info = '{}h {}m {}s'.format(time_info['h'], time_info['m'], time_info['s'])
        f.write('{0},{1},{2},{3},{4}'.format(filename, bvs._reslen, bvs.Rmin_moveion, _BVSE_Ea, _time_info))
    
    if pack_files:
        date_short = time.strftime('%y%m%d_%H%M%S')
        _dire_name = '{}_BVSELi--Res_{}-Rmin_{}--{}'.format(date_short, bvs._reslen, bvs.Rmin_moveion, file.name)
        _dire = os.path.join(file.dirname, _dire_name)
        os.mkdir(_dire)
        shutil.copy2(file.abspath, _dire)
        for _suffix in ['_BVSELi.npy', 
                        '_BVSELi.pgrid', 
                        '_BVELLi.pgrid', 
                        '_BVSLi.pgrid', 
                        '_BVSELi.grd', 
                        '_INFO.csv'
                       ]:
            shutil.move('{}{}'.format(file.abs_stem, _suffix), _dire)
    
    if rename_cif:
        file_new = file.rename('done--' + file.name).string
        os.rename(filename, file_new)
    
    return bvs.Ea['BVSE']


def bv_calculation_normal(filename,
                          moveion='Li',
                          valenceofmoveion=1,
                          resolution=0.1,
                          progress='default', 
                          Rmin_moveion=3
                         ):
    
    prgbar = Progressbar()
    prgbar.set_task('bvse computing progress...', total=100)
    if progress in ['default', 'auto']:
        progress = prgbar.updatetask
    
    atoms = ase.io.read(filename, store_tags=True)
    struc = Structure.Structure()
    struc.GetAseStructure(atoms)
    
    bvs = BVAnalysis.BVAnalysis()
    bvs.SetStructure(struc)
    bvs.SetMoveIon(moveion)
    bvs.ValenceOfMoveIon = valenceofmoveion
    bvs.SetLengthResolution(resolution)
    
    # bvs.CaluBVSE(progress, Rmin_moveion)
    bvs.CaluBVSE(progress)
    
    bvs.SaveBVSEData(os.path.splitext(filename)[0])
    bv_data = bvs.get_data()
    bvs.SaveData(os.path.splitext(filename)[0] + '.bvse.grd', bv_data['BVSE'], 'BVSE')
    
    return bvs.Ea['BVSE']


def bv_calculation_old(filename,
                   moveion='Li',
                   valenceofmoveion=1,
                   resolution=0.1,
                   progress=None):
    atoms = ase.io.read(filename, store_tags=True)
    struc = Structure.Structure()
    struc.GetAseStructure(atoms)
    bvs = BVAnalysis.BVAnalysis()
    bvs.SetStructure(struc)
    bvs.SetMoveIon(moveion)
    bvs.ValenceOfMoveIon = valenceofmoveion
    bvs.SetLengthResolution(resolution)
    
    bvs.CaluBVSE(progress)
    
    bvs.SaveBVSEData(os.path.splitext(filename)[0])
    bv_data = bvs.get_data()
    bvs.SaveData(os.path.splitext(filename)[0] + '.bvse.grd', bv_data['BVSE'], 'BVSE')
    
    return bvs.Ea['BVSE']
    
    
    
    
    