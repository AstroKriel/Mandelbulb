## ###############################################################
## DEPENDENCIES
## ###############################################################
import numpy
import itertools
import multiprocessing
import matplotlib.pyplot as mpl_plot
from . import utils, config, mandelbulb, lighting


## ###############################################################
## FUNCTIONS
## ###############################################################
def ray_marching(x, y, camera, settings, depth=0):
  width        = settings.width
  height       = settings.height
  distance     = height / numpy.tan(camera.fov)
  pixel_pos    = numpy.array([x, y, 0])
  center       = numpy.array([width / 2, height / 2, distance])
  ray_dir      = utils.norm_vec(center - pixel_pos)
  ray_dir_cam  = ray_dir @ camera.view_matrix(settings.target_pos)
  ray_dist     = 0.0
  # Apply small offset to avoid banding artifacts
  ray_dist = 0.01 * ((x * 12.9898 + y * 78.233) % 1.0)
  for _ in range(settings.max_steps):
    pos = camera.pos + ray_dir_cam * ray_dist
    pos = utils.rotate_ray_hor(utils.rotate_ray_ver(pos, camera.angle_ver), camera.angle_hor)
    dist = mandelbulb.estimate_distance(pos, settings.power)
    if dist < settings.surf_dist:
      # Hit surface, calculate lighting
      light, normal, _ = lighting.calculate_lighting(pos, ray_dir_cam, settings, camera, ray_dist)
      # Calculate reflection if depth allows
      reflection = 0.0
      if depth < settings.max_reflections and settings.reflection > 0:
        # Create reflection ray with offset to avoid self-intersection
        reflect_pos = pos + normal * settings.surf_dist * 2.0
        # Create a camera for the reflection ray
        reflect_camera = config.Camera(
          pos       = reflect_pos,
          angle_ver = 0,
          angle_hor = 0,
          fov       = camera.fov,
          global_up = camera.global_up
        )
        # Recursively ray march the reflection
        _, reflection_light = ray_marching(width//2, height//2, reflect_camera, settings, depth+1)
        reflection = reflection_light * settings.reflection
      # Combine direct lighting with reflection
      total_light = light * (1.0 - settings.reflection) + reflection
      return settings.max_dist - ray_dist, total_light
    ray_dist += dist
    if ray_dist > settings.max_dist:
      break
  # No hit, return background (black)
  return settings.max_dist, 0

def compute_pixel(args):
  x, y, camera, settings, depth = args
  dist, light = ray_marching(x, y, camera, settings, depth)
  return x, y, dist, light

def draw_scene(camera, settings, save_path=None, frame_num=None):
  width, height = settings.width, settings.height
  dist_pixels   = numpy.zeros((height, width))
  light_pixels  = numpy.zeros((height, width))
  args = [
    (x, y, camera, settings, 0)
    for x, y in itertools.product(range(width), range(height))
  ]
  with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    results = pool.map(compute_pixel, args)
  for x, y, dist, light in results:
    dist_pixels[y, x] = dist
    light_pixels[y, x] = light
  # Apply contrast enhancement to light pixels
  light_min = numpy.min(light_pixels)
  light_max = numpy.max(light_pixels)
  if light_max > light_min:
    light_pixels = (light_pixels - light_min) / (light_max - light_min)
  # Create distance visualization
  dist_min = numpy.min(dist_pixels)
  dist_max = numpy.max(dist_pixels)
  if dist_max > dist_min:
    dist_pixels = (dist_pixels - dist_min) / (dist_max - dist_min)
  # Create combined visualization
  combined = dist_pixels * 0.3 + light_pixels * 0.7
  fig, axs = mpl_plot.subplots(ncols=3, figsize=(15, 5))
  axs[0].imshow(dist_pixels, cmap="Greys_r", origin="upper")
  axs[0].axis("off")
  axs[1].imshow(light_pixels, cmap="Greys_r", origin="upper")
  axs[1].axis("off")
  axs[2].imshow(combined, cmap="Greys_r", origin="upper")
  axs[2].axis("off")
  mpl_plot.tight_layout()
  if save_path:
    if frame_num is not None:
      filename = f"{save_path}/mandelbulb_frame_{frame_num:04d}.png"
    else: filename = f"{save_path}/mandelbulb.png"
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    mpl_plot.close(fig)
  else: mpl_plot.show()


## END OF MODULE