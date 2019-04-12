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
import unit_test_generative_stacking_lib as gs
reload(gs)

gs.generative_stacking_test()

direction_vectors = [1,-1]
vector_amplitude = search_step
search_size = 5
latest_placed = geos
avail_goes = geos_to_use
num_available_units = 10

placed_units = []
overlapping_areas = []
num_units_per_course = []
all_tests = []

res = gs.search_placement_between_two_units(
    geos[0], geos[1],
    vec = gs.get_geo_or(geos[0]),
    dir_vecs = direction_vectors,
    rotation_degs = rotation_degrees,
    _search_size = search_size,
    rot_geo_degs = rotate_geo_degs
    )

a = res[0]
b = res[1]