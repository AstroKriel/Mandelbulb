## ###############################################################
## DEPENDENCIES
## ###############################################################
import numpy


## ###############################################################
## FUNCTIONS
## ###############################################################
def estimate_distance(pos, power, num_iterations=10):
  z = pos.copy()
  dr = 1.0
  r = 0.0
  for _ in range(num_iterations):
    r = numpy.linalg.norm(z)
    if r > 2.0:
      break
    theta = numpy.acos(z[2] / r)
    phi = numpy.atan2(z[1], z[0])
    zr = r ** power
    dr = power * r ** (power - 1) * dr + 1.0
    z = pos + zr * numpy.array([
      numpy.sin(theta * power) * numpy.cos(phi * power),
      numpy.sin(theta * power) * numpy.sin(phi * power),
      numpy.cos(theta * power)
    ])
  return 0.5 * numpy.log(r) * r / dr


## END OF MODULE