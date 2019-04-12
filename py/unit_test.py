"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "Lorenzo"
__version__ = "2019.04.03"

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import Rhino.Geometry as rg
import sys
import os
sc.doc = ghdoc

curr_dir = os.getcwd()
py_dir = os.path.join(curr_dir, "py")
sys.path.append(py_dir)	
import generative_stacking_lib as gs
reload(gs)

gs.generative_stacking_test()


