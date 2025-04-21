## ###############################################################
## DEPENDENCIES
## ###############################################################
import numpy


## ###############################################################
## FUNCTIONS
## ###############################################################
def norm_vec(vec):
  norm = numpy.linalg.norm(vec)
  return vec if norm == 0 else vec / norm

def rotate_ray_ver(vec, angle):
  matrix = numpy.array([
    [1, 0, 0],
    [0, numpy.cos(angle), -numpy.sin(angle)],
    [0, numpy.sin(angle), numpy.cos(angle)]
  ])
  return vec @ matrix

def rotate_ray_hor(vec, angle):
  matrix = numpy.array([
    [numpy.cos(angle), 0, numpy.sin(angle)],
    [0, 1, 0],
    [-numpy.sin(angle), 0, numpy.cos(angle)]
  ])
  return vec @ matrix


## END OF MODULE