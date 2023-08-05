# -*- coding: utf-8 -*-
# function: lazy import


## ------ System ------
import os
import sys
import gc
import shutil
import time
# from datetime import datetime
from glob import glob
from pathlib import Path


## ------ System Pro ------
import _pickle as pickle
from tqdm import tqdm
from joblib import Parallel, delayed
# from func_timeout import func_set_timeout, func_timeout


## ------ Data Analysis ------
import re
import random
import numpy as np
import pandas as pd
try:
    import polars as pl
except:
    pass

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.ion()
# import scienceplots
plt.style.use('ggplot')

import seaborn as sns

## ------ Scientific Calculation ------
import math
from decimal import Decimal


## ------ Audio Video ------
# from moviepy.editor import VideoFileClip, AudioFileClip


## ------ pybw ------
from pybw.core import *

