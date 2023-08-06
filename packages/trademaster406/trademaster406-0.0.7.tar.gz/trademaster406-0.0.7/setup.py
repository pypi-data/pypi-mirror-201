#!/usr/bin/env python
# Copyright (c) OpenMMLab. All rights reserved.
import os
import os.path as osp
import platform
import shutil
import sys
import warnings
from setuptools import find_packages, setup

import torch
from torch.utils.cpp_extension import (BuildExtension, CppExtension,
                                       CUDAExtension)
with open('README.md', "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setup(
      name='trademaster406',
      version='0.0.7',
      description='TradeMaster - A platform for algorithmic trading',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='NTU_trademaster',
      author_email='TradeMaster.NTU@gmail.com',
      url='https://github.com/TradeMaster-NTU/TradeMaster',
      packages=find_packages(),
        include_package_data=True,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        license='Apache License 2.0',
        install_requires=["Flask",   
     "Flask-Cors",  
      "mmcv",   
      # "git+https://github.com/optuna/optuna.git", 
      "prettytable",  
      "plotly",   
      "psutil",    
      "scipy",
      "spacy", 
      "sqlalchemy",  
      "pandas",    
      "iopath",   
      "yfinance",    
      "matplotlib",    
      "statsmodels",    
      "scikit_learn",    
      "tslearn",    
      # "gym",    
      # "gymnasium",    
      # "ray[rllib]==1.13.0",    
      # "tensorflow==2.11.0",    
      # "packaging",    
      # "kaleido==0.1.0",    
      # "h5py",    
      # "pydantic==1.10.2",    
      "jupyter",    
      "celery",    
      "pika"],
)