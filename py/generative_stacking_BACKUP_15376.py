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

<<<<<<< HEAD
print('not suraaae')

=======
>>>>>>> parent of f3a8706... Add print test
curr_dir = os.getcwd()
py_dir = os.path.join(curr_dir, "py")
sys.path.append(py_dir)	
import generative_stacking_lib as gs
reload(gs)

gs.generative_stacking_test()
    
direction_vectors = [1,-1]
vector_amplitude = search_step
search_size = 10
latest_placed = geos
avail_goes = geos_to_use
num_available_units = 10

placed_units = []
overlapping_areas = []
num_units_per_course = []
all_tests = []

unit_counter = 0
for i in range(max_num_courses):
    print("COURSE {}".format(i))
    print("testing...")
    
    res = gs.search_placement_per_course(avail_geos, latest_placed, 
        dir_vecs = direction_vectors, 
        vec_ampl = vector_amplitude,
        rotation_degs = rotation_degrees, 
        _search_size = search_size,
        rot_geo_degs = rotate_geo_degs)
    
    latest_placed = res[0]
    placed_units.extend(res[0])
    avail_geos = avail_geos.pop(:res[1])

    if res[1] > 0:
        num_units_per_course.append(res[1])
    else:
        print("don't know how to place more units, interrupting...")
        break
    
    all_tests.extend(res[2])
    
    overlapping_areas.extend(res[3])
    
    unit_counter += res[1]
    print("placed {} units".format(res[1]))
    print("")