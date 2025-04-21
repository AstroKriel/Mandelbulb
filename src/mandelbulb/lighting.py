## ###############################################################
## DEPENDENCIES
## ###############################################################
import numpy
from . import mandelbulb, utils


## ###############################################################
## FUNCTIONS
## ###############################################################
def estimate_normal(pos, settings):
  d = mandelbulb.estimate_distance(pos, settings.power)
  dx = d - mandelbulb.estimate_distance(pos - numpy.array([settings.epsilon, 0, 0]), settings.power)
  dy = d - mandelbulb.estimate_distance(pos - numpy.array([0, settings.epsilon, 0]), settings.power)
  dz = d - mandelbulb.estimate_distance(pos - numpy.array([0, 0, settings.epsilon]), settings.power)
  return utils.norm_vec(numpy.array([dx, dy, dz]))

def soft_shadow(pos, light_pos, power, settings, max_steps=64):
  light_dir = light_pos - pos
  light_dist = numpy.linalg.norm(light_dir)
  light_dir = light_dir / light_dist
  t = 0.1 # small offset to avoid self-intersections
  res = 1.0
  for _ in range(max_steps):
    p = pos + light_dir * t
    d = mandelbulb.estimate_distance(p, power)
    # If we hit an object, complete shadow
    if d < settings.surf_dist:
      return 0.0
    # Soft shadow calculation
    res = min(res, settings.shadow_sharpness * d / t)
    t += d
    if t > light_dist:
      break
  return res

def ambient_occlusion(pos, normal, settings, samples=5, max_dist=1.0):
  occlusion = 0.0
  for i in range(samples):
    dist = (i + 1) * max_dist / samples
    sample_pos = pos + normal * dist
    occlusion += (dist - min(mandelbulb.estimate_distance(sample_pos, settings.power), max_dist)) / dist
  return max(0.0, 1.0 - occlusion / samples)

def calculate_specular(view_dir, light_dir, normal, shininess):
  ## Calculate Phong specular highlight
  reflect_dir = utils.norm_vec(2.0 * numpy.dot(normal, light_dir) * normal - light_dir)
  spec_angle = max(0.0, numpy.dot(view_dir, reflect_dir))
  return pow(spec_angle, shininess)

def fog_effect(dist, density=0.02):
  return numpy.exp(-dist * density)

def calculate_lighting(pos, ray_dir, settings, camera, hit_dist):
  """Calculate complete lighting including all effects."""
  normal = estimate_normal(pos, settings)
  # Get light position in scene
  light_pos = utils.rotate_ray_ver(settings.light_pos, camera.angle_ver)
  light_pos = utils.rotate_ray_hor(light_pos, camera.angle_hor)
  light_dir = utils.norm_vec(light_pos - pos)
  view_dir  = utils.norm_vec(-ray_dir)
  shadow = soft_shadow(pos, light_pos, settings.power, settings)
  ao = ambient_occlusion(pos, normal, settings)
  diffuse = max(0.0, numpy.dot(normal, light_dir)) * settings.diffuse
  specular = calculate_specular(view_dir, light_dir, normal, settings.shininess) * settings.specular
  # Apply shadow only to diffuse and specular, but keep some ambient light
  illumination = (settings.ambient * ao) + (diffuse + specular) * shadow
  # Apply fog based on distance
  fog_factor = fog_effect(hit_dist, settings.fog_density)
  return illumination * fog_factor, normal, view_dir


## END OF MODULE