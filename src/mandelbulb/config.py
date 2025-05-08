## ###############################################################
## DEPENDENCIES
## ###############################################################
import numpy
from dataclasses import dataclass, field
from . import utils


## ###############################################################
## FUNCTIONS
## ###############################################################
@dataclass
class Camera:
  pos       : numpy.ndarray
  angle_ver : float # vertical angle in radians
  angle_hor : float # horizontal angle in radians
  fov       : float # field of view in radians
  global_up : numpy.ndarray

  def view_matrix(self, target_pos: numpy.ndarray):
    forward = utils.norm_vec(target_pos - self.pos)
    right   = utils.norm_vec(numpy.cross(forward, self.global_up))
    up      = numpy.cross(right, forward)
    return numpy.array([right, up, forward])

@dataclass
class SceneSettings:
  resolution       : int = 100
  max_steps        : int = 300
  max_dist         : float = 150.0
  surf_dist        : float = 0.001
  epsilon          : float = 0.001
  power            : float = 8.0
  target_pos       : numpy.ndarray = field(default_factory=lambda: numpy.array([0.0, 0.0, 0.0])) # new array per instance
  light_pos        : numpy.ndarray = field(default_factory=lambda: numpy.array([2.0, 2.0, 2.0])) # new array per instance
  light_intensity  : float = 1.2  # increase light brightness
  ambient          : float = 0.15 # ambient light level
  diffuse          : float = 0.7  # diffuse lighting strength
  specular         : float = 0.4  # specular highlight intensity
  shininess        : float = 30.0 # specular highlight size (higher = smaller)
  reflection       : float = 0.3  # reflection strength
  glossiness       : float = 0.7  # reflection glossiness (1.0 = mirror)
  max_reflections  : int = 1      # maximum reflection depth
  fog_density      : float = 0.03 # fog density for atmospheric effect
  shadow_sharpness : float = 16.0 # higher = sharper shadows

  @property
  def width(self):
    return 4 * self.resolution

  @property
  def height(self):
    return 4 * self.resolution


## END OF MODULE