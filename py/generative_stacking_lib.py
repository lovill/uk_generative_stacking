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

debug_print_enabled = True

def generative_stacking_test():
    print("~*~*~*~*~*~*~")
    print("import of generative stacking module succesful")
    print("~*~*~*~*~*~*~")
    print("")

def debug_print(string_to_print):
    if debug_print_enabled:
        print(string_to_print)

def geo_translate(geo, vec, f):
    vec *= f
    xf = rg.Transform.Translation(vec)
    geo_id = sc.doc.Objects.Transform(geo, xf, False)
    return geo_id

def ccx_points(c1, c2):

    c1 = rs.coercecurve(c1)
    c2 = rs.coercecurve(c2)
    # Calculate the intersection
    intersection_tolerance = 0.001
    overlap_tolerance = 0.0
    events = Rhino.Geometry.Intersect.Intersection.CurveCurve(c1, 
                                                            c2, 
                                                            intersection_tolerance, 
                                                            overlap_tolerance)
    # Process the results
    if not events: 
        return False
        
    else:
        pts = []
        for ccx_event in events:
            pts.append(sc.doc.Objects.AddPoint(ccx_event.PointA))
            
    
        return pts

def calc_overlap_area_ratio(c1, c2):
    c1 = rs.coercecurve(c1)
    c2 = rs.coercecurve(c2)
    geo_area = rs.CurveArea(c1)[0]
    
    overlap_region = c1.CreateBooleanIntersection(c1, c2)
    if overlap_region:
        overlap_area = rg.AreaMassProperties.Compute(overlap_region).Area
        overlap_area_ratio = (overlap_area / geo_area)*100
        
        debug_print("overlap area ratio: {}%".format(round(overlap_area_ratio, 1)))
    
        return overlap_area_ratio
    
    else:
        return 0

def test_conditions(geo_underneath, geo_to_test, 
    geo_to_test_against, placed_geos = [], boolean_check = False,
    min_area_overlap1 = 12.5, min_area_overlap2 = 12.5):
    
    # check for intersection with underneath geo unit
    overlap_area_r1 = calc_overlap_area_ratio(geo_to_test, geo_underneath)
    if ccx_points(geo_to_test, geo_underneath) and overlap_area_r1 > min_area_overlap1:
        
#        # check if overlapping area requirement is satisfied
#        overlap_area_r = calc_overlap_area_ratio(geo_to_test, geo_underneath)
#        print(overlap_area_r)
#        if overlap_area_r > min_area_overlap:
                
            
        # check for intersection (overlap on top of other lower course)

        if ccx_points(geo_to_test, geo_to_test_against):
            
            # check for intersection of already placed bricks
            # use surrogate version of unit to take into account...
            # ...robot endeffector size
            surrogate_geo =  non_uniform_scale(geo_to_test, scale_x = 1)
            int_with_placed_geos = False
            for pg in placed_geos:

                if pg:
                    if ccx_points(surrogate_geo, pg):
                        
                        int_with_placed_geos = True
                        break
            
            if not int_with_placed_geos:
                # overlap requirement
                overlap_area_r2 = calc_overlap_area_ratio(geo_to_test, geo_to_test_against)
                tot_overlap_area_r = overlap_area_r1 + overlap_area_r2
                
                if overlap_area_r2 > min_area_overlap2:
                    boolean_check = True
            
            
    else:
        return "terminate search"              
    
    
    
    return boolean_check

def get_geo_or(geo):
    
    # get lines
    lines = rs.ExplodeCurves(geo)
    lines_lengths_tuples = [(rs.CurveLength(l), l) for l in lines]
    
    # get reference line for base vector
    longest_line = lines[0]

    # get vector
    or_vec = rs.VectorUnitize(rs.VectorCreate(rs.CurveStartPoint(longest_line),
                             rs.CurveEndPoint(longest_line)))
    
    return or_vec

def non_uniform_scale(geo, scale_x = 1, scale_y = 1, scale_z = 1):

    vy = get_geo_or(geo)
    vx = vy
    vx = rs.VectorRotate(vy, 90, rs.AddPoint(0,0,1))
    geo_cp = rs.CurveAreaCentroid(geo)[0]

    geo_plane = rg.Plane(geo_cp, vx, vy)

    xf = rg.Transform.Scale(geo_plane, 
                                    scale_x,
                                    scale_y,
                                    scale_z)
                                    
    scaled_geo = sc.doc.Objects.Transform(geo, xf, False)

    return scaled_geo

def search_placement_between_two_units(c1, c2, 
    vec = rs.AddPoint(1,0,0), dir_vecs = [1], 
    rotation_degs = [0], vec_ampl = 1, 
    _search_size = 2, rot_geo_degs = [0], 
    placed_geos = [],
    min_area_overlap1 = 15, min_area_overlap2 = 15):
    debug_print("")
    debug_print("initialize testing...")
    debug_print("vector amplitude: {}".format(vec_ampl))
    debug_print("search size: {}".format(_search_size))
    debug_print("testing...")    
    
    search_iters = []
    placed_brick = None
    tot_overl_area = None
    found_placed_brick = False
    geo_to_translate = c1
    geo_original_underneath = c1
    
    # for rot_geo_deg in rot_geo_degs:
    #     geo_to_translate = rs.RotateObject(geo_to_translate, 
    #                         rs.CurveAreaCentroid(geo_to_translate)[0], 
    #                         rot_geo_deg)

    for rot_vec in rotation_degs:
        vec = rs.VectorRotate(vec, rot_vec, rs.AddPoint(0,0,1))   
        
        for dir_vec in dir_vecs:
            vec *= dir_vec
            
            for si in range(_search_size):
            
                translated_geo = geo_translate(geo_to_translate, 
                    vec, vec_ampl)
                
                # CONDITIONS TO MEET FOR BRICK PLACEMENT
                conditions_met = test_conditions(geo_original_underneath, 
                    translated_geo, c2, placed_geos)
                
                search_iters.append(translated_geo)
                debug_print("search_iter: {}".format(translated_geo))

                if conditions_met == "terminate search":
                    break
                
                
                if conditions_met:
                    placed_brick = translated_geo
                    found_placed_brick = True
                    overl_area1 = calc_overlap_area_ratio(
                                    translated_geo, 
                                    geo_original_underneath
                                    )
                    overl_area2 = calc_overlap_area_ratio(
                                    translated_geo, 
                                     c2
                                    )
                    tot_overl_area = overl_area1 + overl_area2
                    return search_iters, placed_brick, tot_overl_area    
                
                else:
                    geo_to_translate = translated_geo
                    continue
                        
    return search_iters, placed_brick, tot_overl_area

def search_placement_per_course(geos, vec = rs.AddPoint(1,0,0), 
    dir_vecs = [1], rotation_degs = [0], 
    vec_ampl = 1, _search_size = 2, 
    rot_geo_degs = [0], placed_geos = []):
    placed_bricks_per_course = []
    all_tests_per_course = []
    overl_areas = []
    
    for ig, g1 in enumerate(geos):
        debug_print("unit: {}".format(ig))

        for g2 in geos:
            
            if g1 == g2:
                continue
            
            else:
                res = search_placement_between_two_units(g1, g2, 
                            vec = get_geo_or(g1), 
                            dir_vecs = dir_vecs,
                            rotation_degs = rotation_degs, 
                            _search_size = _search_size,
                            vec_ampl = vec_ampl,
                            rot_geo_degs = rot_geo_degs,
                            placed_geos = placed_bricks_per_course)
                
                if res[1]:
                    placed_bricks_per_course.append(res[1])
                    overl_areas.append(res[2])

                all_tests_per_course.extend(res[0])    

    return placed_bricks_per_course, len(placed_bricks_per_course), all_tests_per_course, overl_areas            