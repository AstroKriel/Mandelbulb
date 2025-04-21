## ###############################################################
## DEPENDENCIES
## ###############################################################
import os
import numpy
from mandelbulb import config, rendering


## ###############################################################
## PROGRAM MAIN
## ###############################################################
def main():
  output_dir = "gallery"
  os.makedirs(output_dir, exist_ok=True)
  settings = config.SceneSettings(
    resolution       = 150,
    power            = 8.0,  # power parameter for mandelbulb fractal
    light_pos        = numpy.array([2.0, 2.0, 2.0]),
    ambient          = 0.15, # ambient light level
    diffuse          = 0.7,  # diffuse lighting strength
    specular         = 0.4,  # specular highlight intensity
    shininess        = 30.0, # specular highlight size
    reflection       = 0.3,  # reflection strength
    glossiness       = 0.7,  # reflection glossiness
    max_reflections  = 2,    # limit recursion depth
    fog_density      = 0.03, # atmospheric fog effect
    shadow_sharpness = 16.0, # shadow edge sharpness
  )
  num_frames    = 16 # number of frames for a full loop (2 orbits)
  orbit_radius  = 2.5 # distance from center
  height_offset = 0.5 # height above orbit plane
  print(f"Rendering with resolution {settings.width}x{settings.height}...")
  for frame_index in range(num_frames):
    angle  = 2 * numpy.pi * frame_index / num_frames
    camera = config.Camera(
      angle_hor = -angle,              # look toward center
      angle_ver = 20 * numpy.pi / 180, # look down slightly
      fov       = 45 * numpy.pi / 180, # field of view (in radians)
      global_up = numpy.array([0.0, 1.0, 0.0]),
      pos       = numpy.array([
        orbit_radius * numpy.sin(angle),
        height_offset,
        orbit_radius * numpy.cos(angle)
      ]),
    )
    print(f"Rendering frame {frame_index+1}/{num_frames}")
    rendering.draw_scene(camera, settings, save_path=output_dir, frame_num=frame_index)
  print(f"Orbit animation rendered. {num_frames} frames saved to {output_dir}")
  print(f"Images saved to: {os.path.abspath(output_dir)}")


## ###############################################################
## SCRIPT ENTRY POINT
## ###############################################################
if __name__ == "__main__":
  main()


## END OF SCRIPT