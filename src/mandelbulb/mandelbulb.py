## ###############################################################
## DEPENDENCIES
## ###############################################################
import numpy


## ###############################################################
## FUNCTIONS
## ###############################################################
def estimate_distance(input_position, exponent, num_iterations=10):
  iter_position = input_position.copy()
  radius_derivative = 1.0
  radius = 0.0
  for _ in range(num_iterations):
    radius = numpy.linalg.norm(iter_position)
    if radius > 2.0: break
    polar_angle = numpy.acos(iter_position[2] / radius)
    azimuthal_angle = numpy.atan2(iter_position[1], iter_position[0])
    radius_derivative = exponent * numpy.power(radius, exponent-1) * radius_derivative + 1.0
    iter_position = input_position + numpy.power(radius, exponent) * numpy.array([
      numpy.sin(polar_angle * exponent) * numpy.cos(azimuthal_angle * exponent),
      numpy.sin(polar_angle * exponent) * numpy.sin(azimuthal_angle * exponent),
      numpy.cos(polar_angle * exponent)
    ])
  return 0.5 * numpy.log(radius) * radius / radius_derivative


## END OF MODULE