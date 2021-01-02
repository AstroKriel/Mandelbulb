##############################################
## MODULES
##############################################
import numpy as np
import matplotlib.pyplot as plt
from pylab import cm

from math import *

##############################################
## PARAMETERS
##############################################
## ray marching properties
global MAX_STEPS, MAX_DIST, SURF_DIST, EPSILON, PI
PI = 3.141592653589793238462643
MAX_STEPS = 300
MAX_DIST  = 150.0
SURF_DIST = 0.001
EPSILON   = 0.001

## figure / screen properties
global WIDTH, HEIGHT
resolution = 30
WIDTH  = 4*resolution
HEIGHT = 3*resolution

## camera properties
global CAM_FOV, CAM_POS, CAM_ANG_VER, CAM_ANG_HOR, GLOBAL_UP, LIGHT_POS
CAM_FOV     = 45 * PI/180 # radians
CAM_ANG_VER = 20 * PI/180 # radians
CAM_ANG_HOR = 10 * PI/180 # radians
GLOBAL_UP = np.array([0.0, 1.0, 0.0])
CAM_POS   = np.array([0.0, 0.0, 2.5])
LIGHT_POS = np.array([1.0, 1.0, 1.0])

## mandelbulb properties
global TARGET_POS, POWER
TARGET_POS = np.array([0.0, 0.0, 0.0])
POWER = 8.0

##############################################
## FUNCTIONS
##############################################
def rotate_ray_ver(vec, angle):
    matrix = np.array([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)]
    ])
    result = matrix.dot(vec)
    return result

def rotate_ray_hor(vec, angle):
    matrix = np.array([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])
    result = matrix.dot(vec)
    return result

def normVec(vec):
    if np.linalg.norm(vec) == 0: return vec
    return vec / np.linalg.norm(vec)

def view_matrix():
    global CAM_POS, GLOBAL_UP, TARGET_POS
    ## basis vectors : https://www.3dgep.com/understanding-the-view-matrix/
    cam2obj = normVec(TARGET_POS - CAM_POS) # forward
    vec_cross = np.cross(cam2obj, GLOBAL_UP)
    x_axis = normVec(vec_cross) # right
    y_axis = np.cross(x_axis, cam2obj) # up
    return np.array([x_axis, y_axis, cam2obj])

def getNormal(ray_pos):
    global EPSILON
    safe_dist = DEMandelbulb(ray_pos)
    vec_x = safe_dist - DEMandelbulb(ray_pos - np.array([EPSILON, 0, 0]))
    vec_y = safe_dist - DEMandelbulb(ray_pos - np.array([0, EPSILON, 0]))
    vec_z = safe_dist - DEMandelbulb(ray_pos - np.array([0, 0, EPSILON]))
    return normVec([vec_x, vec_y, vec_z])

def getLight(ray_pos):
    global LIGHT_POS, CAM_ANG_VER, CAM_ANG_HOR
    light_pos = LIGHT_POS
    light_pos = rotate_ray_ver(light_pos, CAM_ANG_VER)
    light_pos = rotate_ray_hor(light_pos, CAM_ANG_HOR)
    light2surface_angle = normVec(light_pos - ray_pos)
    surface_normal = getNormal(ray_pos)
    return max(0.0, min(1.0, np.dot(surface_normal, light2surface_angle)))

def DEMandelbulb(ray_pos):
    global POWER
    tmp_pos = ray_pos
    dr = 2.0
    for tmp_iter in range(10):
        r = np.linalg.norm(tmp_pos)
        if r > 2.0: break
        ## approximate the distance differential
        dr = POWER * pow(r, POWER-1.0) * dr + 1.0
        ## calculate fractal surface
        ## convert to polar coordinates
        theta = acos( tmp_pos[2] / r )
        phi   = atan2(tmp_pos[1], tmp_pos[0])
        zr    = pow(r, POWER)
        ## convert back to cartesian coordinated
        x = zr * sin(theta * POWER) * cos(phi * POWER)
        y = zr * sin(theta * POWER) * sin(phi * POWER)
        z = zr * cos(theta * POWER)
        tmp_pos = ray_pos + np.array([x, y, z])
    ## distance estimator
    return 0.5 * np.log(r) * r / dr

def rayMarching(x, y):
    global WIDTH, HEIGHT
    global MAX_STEPS, MAX_DIST, SURF_DIST
    global CAM_FOV, CAM_POS, CAM_ANG_VER, CAM_ANG_HOR
    dist_cam2obj = HEIGHT / tan(CAM_FOV)
    vec2obj      = np.array([ (WIDTH // 2), (HEIGHT // 2), dist_cam2obj ])
    vec2pixel    = np.array([x, y, 0])
    ## compute vector from camera to object
    ray_dir_world = normVec( vec2obj - vec2pixel ) # in world coordinates
    ray_dir_cam = view_matrix().dot(ray_dir_world) # in camera (view matrix) coordinates
    ray_dist = 0 # initialise distance travelled by ray
    ## find how far ray can travel along direction
    for tmp_iter in range(MAX_STEPS):
        ## integrate the ray forwards
        ray_pos = CAM_POS + ray_dir_cam * ray_dist
        ## apply camera rotations
        ray_pos = rotate_ray_hor(rotate_ray_ver(ray_pos, CAM_ANG_VER), CAM_ANG_HOR)
        ## check how far the ray can step safely
        tmp_dist = DEMandelbulb(ray_pos)
        ## check if sufficiently close to mandelbulb
        if tmp_dist < SURF_DIST: return ((MAX_DIST-ray_dist), getLight(ray_pos))
        ray_dist += tmp_dist
        if ray_dist > MAX_DIST: break
    return (MAX_DIST, 0)

def drawScene():
    global WIDTH, HEIGHT
    ## initialise screen pixels
    dist_pixels  = np.zeros((HEIGHT, WIDTH))
    light_pixels = np.zeros((HEIGHT, WIDTH))
    ## calculate the inensity of each pixel on the screen
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            dist, light = rayMarching(x, y)
            dist_pixels[y][x] = dist
            light_pixels[y][x] = light
    ## plot distances
    fig, ax = plt.subplots()
    ax.imshow(dist_pixels, cmap=cm.gray, origin='upper') # plot dist data
    ax.axis('off') # remove axis labels
    plt.tight_layout() # minimise white space
    plt.show()
    ## plot lighting
    fig, ax = plt.subplots()
    ax.imshow(light_pixels, cmap=cm.gray, origin='upper') # plot light data
    ax.axis('off') # remove axis labels
    plt.tight_layout() # minimise white space
    plt.show()


##############################################
## MAIN PROGRAM
##############################################
if __name__ == "__main__":
    plt.close('all')
    drawScene()
