#!/usr/bin/env python

import os
from distutils.core import setup, Extension
from subprocess import Popen, PIPE
import sys


this_dir = os.path.dirname(os.path.realpath(__file__))

Pymodule = Extension('parsepom', 
                  define_macros = [('MAJOR_VERSION', '1'),
                                   ('MINOR_VERSION', '0')],
                  sources = [os.path.join('src', 'ToPy.cpp'), os.path.join('src','global.cc'),
                    os.path.join('src', 'misc.cc'),os.path.join('src', 'normal_law.cc'),os.path.join('src', 'pom.cc'),
                    os.path.join('src', 'pom_solver.cc'), os.path.join('src', 'proba_view.cc'),os.path.join('src', 'rectangle.cc'),
                    os.path.join('src', 'rgb_image.cc'),os.path.join('src', 'room.cc')],
                  libraries = ["png"],
                  extra_compile_args = ['-std=c++11'])

setup (name = 'parsepom',
       version = '1.0',
       ext_modules = [Pymodule])
