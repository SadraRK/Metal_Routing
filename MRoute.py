"""
  Sadra Rahimi Kari
  SAR247@pitt.edu

  Pitt-Photonics 2021
  https://pitt-photonics.github.io/

  Smart Routing V1.0
"""

from pya import *
import pya
import numpy as np
import scipy
import math
from math import pi, sin, cos, sqrt
from pya import *
from SiEPIC import scripts  
from SiEPIC.extend import to_itype
from SiEPIC.utils import get_layout_variables
  
def metal_2_pad_route(Layer, width_metal, Direction_Matrix, source_coords, dest_coords, pad_name):
  
  # load the correct layer information
  TECHNOLOGY, lv, ly, cell = get_layout_variables()
  top_cell = ly.top_cells()[0]
  dbu = ly.dbu
  LayerMetal = Layer
  TextLayer = ly.layer(TECHNOLOGY['Text'])
  
  # initiate the routing coordinate system
  if (len(Direction_Matrix)%2 !=0):
    Direction_Matrix.append(0)
  
  Direction_Matrix.append(Direction_Matrix[len(Direction_Matrix)-2])
  Direction_Matrix.append(Direction_Matrix[len(Direction_Matrix)-1])
  
  corner_poly = []
  Orientation_matrix = []
  Distance_matrix = []
  updated_coords = source_coords*1000
  
  for i in range(len(Direction_Matrix)):
    if (i%2 == 0):
      Orientation_matrix.append(Direction_Matrix[i])
    elif(i%2 != 0):
      Distance_matrix.append(Direction_Matrix[i]*1000)
      
  for q in range(len(Orientation_matrix)-1):
    if (Orientation_matrix[q]==0):
      metal_routing = Path([Point(updated_coords[0], updated_coords[1]), Point(updated_coords[0] + Distance_matrix[q]+ (width_metal*1000)/2, updated_coords[1])], width_metal*1000)
      top_cell.shapes(LayerMetal).insert(metal_routing)
      updated_coords = [updated_coords[0] + Distance_matrix[q] + (width_metal*1000)/2, updated_coords[1]]
      pts = [pya.Point.from_dpoint(pya.DPoint(updated_coords[0], updated_coords[1]-(Orientation_matrix[q+1]/90)*(width_metal*1000)/2)), pya.Point.from_dpoint(pya.DPoint(updated_coords[0], updated_coords[1])), pya.Point.from_dpoint(pya.DPoint(updated_coords[0] + (width_metal*1000)/2, updated_coords[1]))]
      corner_poly.append(top_cell.shapes(LayerMetal).insert(pya.Polygon(pts)))
    elif (Orientation_matrix[q]==180):
      metal_routing = Path([Point(updated_coords[0], updated_coords[1]), Point(updated_coords[0]- Distance_matrix[q]- (width_metal*1000)/2, updated_coords[1])], width_metal*1000)
      top_cell.shapes(LayerMetal).insert(metal_routing)
      updated_coords = [updated_coords[0] - Distance_matrix[q]- (width_metal*1000)/2, updated_coords[1]]
      pts = [pya.Point.from_dpoint(pya.DPoint(updated_coords[0], updated_coords[1]-(Orientation_matrix[q+1]/90)*(width_metal*1000)/2)), pya.Point.from_dpoint(pya.DPoint(updated_coords[0], updated_coords[1])), pya.Point.from_dpoint(pya.DPoint(updated_coords[0] - (width_metal*1000)/2, updated_coords[1]))]
      corner_poly.append(top_cell.shapes(LayerMetal).insert(pya.Polygon(pts)))
    elif (Orientation_matrix[q]==90):
      metal_routing = Path([Point(updated_coords[0], updated_coords[1]), Point(updated_coords[0], updated_coords[1]+ Distance_matrix[q]+ (width_metal*1000)/2)], width_metal*1000)
      top_cell.shapes(LayerMetal).insert(metal_routing)
      updated_coords = [updated_coords[0], updated_coords[1]+ Distance_matrix[q] + (width_metal*1000)/2]
      pts = [pya.Point.from_dpoint(pya.DPoint(updated_coords[0]-((90-Orientation_matrix[q+1])/90)*(width_metal*1000)/2, updated_coords[1])), pya.Point.from_dpoint(pya.DPoint(updated_coords[0], updated_coords[1])), pya.Point.from_dpoint(pya.DPoint(updated_coords[0], updated_coords[1] + (width_metal*1000)/2))]
      corner_poly.append(top_cell.shapes(LayerMetal).insert(pya.Polygon(pts)))
    elif (Orientation_matrix[q]==-90):
      metal_routing = Path([Point(updated_coords[0], updated_coords[1]), Point(updated_coords[0], updated_coords[1]- Distance_matrix[q]- (width_metal*1000)/2)], width_metal*1000)
      top_cell.shapes(LayerMetal).insert(metal_routing)
      updated_coords = [updated_coords[0], updated_coords[1]- Distance_matrix[q] - (width_metal*1000)/2]
      pts = [pya.Point.from_dpoint(pya.DPoint(updated_coords[0]-((90-Orientation_matrix[q+1])/90)*(width_metal*1000)/2, updated_coords[1])), pya.Point.from_dpoint(pya.DPoint(updated_coords[0], updated_coords[1])), pya.Point.from_dpoint(pya.DPoint(updated_coords[0], updated_coords[1] - (width_metal*1000)/2))]
      corner_poly.append(top_cell.shapes(LayerMetal).insert(pya.Polygon(pts)))
  
  corner_poly[len(Orientation_matrix)-2].delete()  

  #shapes_temp = top_cell.shapes(LayerMetal)
  #ShapeProcessor().merge(ly,top_cell,LayerMetal,shapes_temp,True,0,True,True)
  return top_cell

if __name__=="__main__":
  TECHNOLOGY, lv, ly, cell = get_layout_variables()  
  metal_2_pad_route(ly.layer(LayerInfo(105, 0)), 20, [0, 100, 90, 150, 0, 50, 90, 100, 0, 60], [0.0, 0.0], [21.0, 25.0], 'test_trace')
