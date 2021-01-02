//==============================================
// PACKAGES
//==============================================
#include <chrono>    // high_resolution_clock
#include <iostream>  // std::cout
#include <iomanip>   // setting precision of output strings
#include <sstream>   // converting numbers to strings streams
#include <string>    // std::string
#include <fstream>   // creating string streams
#include <algorithm> // std::clamp
#include <stdlib.h>  // srand, rand
#include <math.h>    // trig functions : sin, cos


//==============================================
// COMPILIATION
//==============================================
/* g++ -Wall -Wextra -fopenmp .\srs\main.cpp -o program */


//==============================================
// PARAMETERS
//==============================================
// math constants / conversions
#define PI 3.141592653589793238462643
#define deg2rad(deg) (deg * PI/180.0)

// raymarching properties
#define MAX_STEPS 100
#define MAX_DIST  5.0
#define SURF_DIST 0.001
#define EPSILON   0.0001

// screen properties
#define RESOLUTION 1000
#define WIDTH  RESOLUTION
#define HEIGHT RESOLUTION

// camera properties
double CAM_FOV      = deg2rad(45);
double CAM_ANG_VER  = deg2rad(-15.0);
double CAM_ANG_HOR  = deg2rad(25.0);
double GLOBAL_UP[3] = {1.0, 0.0, 0.0};
double CAM_POS[3]   = {0.0, 0.0, 2.5}; 
double LIGHT_POS[3] = {2.0, 0.0, 5.0}; // (x, y, z)

// mandelbulb properties
double POWER = 8.0;
double TARGET_POS[3] = {0.0, 0.0, 0.0};


//==============================================
// FUNCTION DEFINITIONS
//==============================================
void printVec(double vec[], int num=3) {
    for (int i = 0; i < num; ++i) { std::cout << vec[i] << ", "; }
    std::cout << std::endl;
}

void copyVec(double vec[], double vec_copy[], int num=3) {
    for (int i = 0; i < num; ++i) { vec_copy[i] = vec[i]; }
}

double myClamp(double val) {
    if (val >= 1.0) { return 1.0; }
    if (val <= 0.0) { return 0.0; }
    return val;
}

double dotVec3s(double vec1[], double vec2[]) {
    return (vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2]);
}

double magVec(double vec[]) {
    return sqrt(vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2]);
}

void subVec3s(double vec1[], double vec2[], double result[]) {
    result[0] = vec1[0] - vec2[0];
    result[1] = vec1[1] - vec2[1];
    result[2] = vec1[2] - vec2[2];
}

void addVec3s(double vec1[], double vec2[], double result[]) {
    result[0] = vec1[0] + vec2[0];
    result[1] = vec1[1] + vec2[1];
    result[2] = vec1[2] + vec2[2];
}

void multNumVec3(double val, double vec[], double result[]) {
    result[0] = val * vec[0];
    result[1] = val * vec[1];
    result[2] = val * vec[2];
}

void moveVec3(double vec[], double dir[], double step, double result[]) {
    result[0] = vec[0] + step * dir[0];
    result[1] = vec[1] + step * dir[1];
    result[2] = vec[2] + step * dir[2];
}

void normVec3(double vec[]) {
    double vec_mag = magVec(vec);
    if (vec_mag == 0) vec_mag = 1; // just return the original vector
    vec[0] = vec[0] / vec_mag;
    vec[1] = vec[1] / vec_mag;
    vec[2] = vec[2] / vec_mag;
}

void multMatrixVec3(double matrix[], double vec3[], double result[]) {
    result[0] = matrix[0]*vec3[0] + matrix[1]*vec3[1] + matrix[2]*vec3[2];
    result[1] = matrix[3]*vec3[0] + matrix[4]*vec3[1] + matrix[5]*vec3[2];
    result[2] = matrix[6]*vec3[0] + matrix[7]*vec3[1] + matrix[8]*vec3[2];
}

void crossVec3s(double vec1[], double vec2[], double result[]) {
    result[0] = vec1[1] * vec2[2] - vec1[2] * vec2[1];
    result[1] = vec1[2] * vec2[0] - vec1[0] * vec2[2];
    result[2] = vec1[0] * vec2[1] - vec1[1] * vec2[0];
}

void rotateVec3Ver(double vec[], double angle) {
    double rotation_matrix[9] = {
        1, 0, 0, 
        0, cos(angle), -sin(angle), 
        0, sin(angle), cos(angle)
    };
    double rot_vec[3];
    multMatrixVec3(rotation_matrix, vec, rot_vec);
    vec[0] = rot_vec[0];
    vec[1] = rot_vec[1];
    vec[2] = rot_vec[2];
}

void rotateVec3Hor(double vec[], double angle) {
    double rotation_matrix[9] = {
        cos(angle),  0, sin(angle),
        0, 1, 0,
        -sin(angle), 0, cos(angle)
    };
    double rot_vec[3];
    multMatrixVec3(rotation_matrix, vec, rot_vec);
    vec[0] = rot_vec[0];
    vec[1] = rot_vec[1];
    vec[2] = rot_vec[2];
}

double* view_matrix() {
    // working with arrays : https://stackoverflow.com/questions/31180470/declaring-a-double-array-in-c-using-brackets-or-asterisk
    // basis vectors : https://www.3dgep.com/understanding-the-view-matrix/
    // forward basis vector
    double cam2obj[3];
    subVec3s(TARGET_POS, CAM_POS, cam2obj);
    normVec3(cam2obj);
    // right basis vector
    double x_axis[3];
    crossVec3s(cam2obj, GLOBAL_UP, x_axis);
    normVec3(x_axis);
    // up basis vector
    double y_axis[3];
    crossVec3s(x_axis, cam2obj, y_axis);
    // store view matrix as array
    static double v_matrix[9] = {
        x_axis[0],  x_axis[1],  x_axis[2],
        y_axis[0],  y_axis[1],  y_axis[2],
        cam2obj[0], cam2obj[1], cam2obj[2]
    };
    return v_matrix;
}

double DEMandelbulb(double ray_pos[]) {
    double tmp_pos[3];
    for (int i = 0; i < 3; ++i) { tmp_pos[i] = ray_pos[i]; }
    double cart_pos[3];
    double dr = 1.0;
    double r;
    double theta;
    double phi;
    double zr;
    for (int tmp_iter = 0; tmp_iter < 15; tmp_iter++) {
        r = magVec(tmp_pos);
        if (r > 2.0) { break; }
        // approximate the distance differential
        dr = POWER * pow(r, POWER-1.0) * dr + 1.0;
        // calculate fractal surface
        // convert to polar coordinates
        theta = POWER * acos(tmp_pos[2] / r);
        phi   = POWER * atan2(tmp_pos[1], tmp_pos[0]);
        zr    = pow(r, POWER);
        // convert back to cartesian coordinated
        cart_pos[0] = zr * sin(theta) * cos(phi);
        cart_pos[1] = zr * sin(theta) * sin(phi);
        cart_pos[2] = zr * cos(theta);
        addVec3s(ray_pos, cart_pos, tmp_pos);
    }
    // distance estimator
    return 0.5 * log(r) * r / dr;
}

void getNormal(double ray_pos[], double surf_normal[]) {
    double epsilon_x[3] = {EPSILON, 0, 0};
    double epsilon_y[3] = {0, EPSILON, 0};
    double epsilon_z[3] = {0, 0, EPSILON};
    double ray_perb_x1[3];
    double ray_perb_y1[3];
    double ray_perb_z1[3];
    addVec3s(ray_pos, epsilon_x, ray_perb_x1);
    addVec3s(ray_pos, epsilon_y, ray_perb_y1);
    addVec3s(ray_pos, epsilon_z, ray_perb_z1);
    double ray_perb_x2[3];
    double ray_perb_y2[3];
    double ray_perb_z2[3];
    subVec3s(ray_pos, epsilon_x, ray_perb_x2);
    subVec3s(ray_pos, epsilon_y, ray_perb_y2);
    subVec3s(ray_pos, epsilon_z, ray_perb_z2);
    surf_normal[0] = DEMandelbulb(ray_perb_x1) - DEMandelbulb(ray_perb_x2);
    surf_normal[1] = DEMandelbulb(ray_perb_y1) - DEMandelbulb(ray_perb_y2);
    surf_normal[2] = DEMandelbulb(ray_perb_z1) - DEMandelbulb(ray_perb_z2);
    normVec3(surf_normal);
}

double getLight(double ray_pos[]) {
    // copy the light source position
    double light_pos[3];
    copyVec(LIGHT_POS, light_pos);
    // rotate light source along with camera
    rotateVec3Hor(light_pos, CAM_ANG_HOR);
    rotateVec3Ver(light_pos, CAM_ANG_VER);
    // measure angle of intesection of light with surface
    double light2surface_angle[3];
    subVec3s(light_pos, ray_pos, light2surface_angle);
    normVec3(light2surface_angle);
    // measure angle of surface normal
    double surface_normal[3];
    getNormal(ray_pos, surface_normal);
    // calculate how intense light consentration is at point on surface
    return myClamp( dotVec3s(surface_normal, light2surface_angle) );
}

void rayMarching(int x, int y, double tmp_output_arr[]) {
    // compute vector from camera to object
    // in world coordinates
    double dist_cam2obj = HEIGHT / tan(CAM_FOV);
    double vec2obj[3]   = { floor(WIDTH/2), floor(HEIGHT/2), dist_cam2obj };
    double vec2pixel[3] = { (double)x, (double)y, 0.0 };
    double ray_dir_world[3];
    subVec3s(vec2obj, vec2pixel, ray_dir_world);
    normVec3(ray_dir_world);
    // in camera (view matrix) coordinates
    double ray_dir_cam[3];
    multMatrixVec3(view_matrix(), ray_dir_world, ray_dir_cam);
    double ray_dist = 0; // initialise distance travelled by ray
    // find how far ray can travel along direction
    double ray_pos[3];
    double ray_dir_cam_rot[3];
    double ray_back_step[3];
    double tmp_dist;
    // initialise output array
    tmp_output_arr[0] = MAX_DIST;
    tmp_output_arr[1] = 0;
    tmp_output_arr[2] = 0;
    for (int tmp_iter = 0; tmp_iter < MAX_STEPS; tmp_iter++) {
        // integrate the ray forwards
        moveVec3(CAM_POS, ray_dir_cam, ray_dist, ray_pos);
        // apply camera rotations
        rotateVec3Ver(ray_pos, CAM_ANG_VER);
        rotateVec3Hor(ray_pos, CAM_ANG_HOR);
        // check how far the ray can step safely
        tmp_dist = DEMandelbulb(ray_pos);
        ray_dist += tmp_dist;
        // check if sufficiently close to mandelbulb
        // if somewhat close, make a save, incase you don't get closer
        for (double mult = 2; mult < 4; ++mult) {
            if (tmp_dist < mult*SURF_DIST) {
                copyVec(ray_dir_cam, ray_dir_cam_rot);
                rotateVec3Ver(ray_dir_cam_rot, CAM_ANG_VER);
                rotateVec3Hor(ray_dir_cam_rot, CAM_ANG_HOR);
                moveVec3(ray_pos, ray_dir_cam_rot, -EPSILON, ray_back_step);
                tmp_output_arr[0] = MAX_DIST - ray_dist;
                tmp_output_arr[1] = getLight(ray_back_step);
                break;
            }
        }
        if (tmp_dist < SURF_DIST) {
            copyVec(ray_dir_cam, ray_dir_cam_rot);
            rotateVec3Ver(ray_dir_cam_rot, CAM_ANG_VER);
            rotateVec3Hor(ray_dir_cam_rot, CAM_ANG_HOR);
            moveVec3(ray_pos, ray_dir_cam_rot, EPSILON, ray_back_step);
            tmp_output_arr[0] = MAX_DIST - ray_dist;
            tmp_output_arr[1] = getLight(ray_back_step);
            break;
        }
        // check if the ray is a lost cause (travelled too far)
        if (ray_dist > MAX_DIST) { break; } 
    }
}

void calcScene(int iter=0) {
    // allocate memory for pixels information
    double* dist_matrix = new double[HEIGHT * WIDTH];
    double* light_matrix = new double[HEIGHT * WIDTH];
    // calculate the intensity of each pixel on the screen
    std::cout << "\t" << iter << ". Calculating points." << std::endl;
    #pragma omp parallel
    {
        double tmp_output_ptr[3];
        #pragma omp for
        for (int y = 0; y < HEIGHT; y++) {
            for (int x = 0; x < WIDTH; x++) {
                rayMarching(x, y, tmp_output_ptr);
                dist_matrix[y*WIDTH + x] = tmp_output_ptr[0];
                light_matrix[y*WIDTH + x] = tmp_output_ptr[1];
            }
        }
    }
    std::string str_iter = std::to_string(iter);
    str_iter.insert(str_iter.begin(), 3-str_iter.length(), '0');
    // save mandelbulb distance data
    std::cout << "\t> Saving distance data." << std::endl;
    std::ofstream file_dist_data("data/dist_" + str_iter + ".txt");
    if (file_dist_data.is_open()) {
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
                if (y < HEIGHT-1) { file_dist_data << dist_matrix[y*WIDTH + x] << ", "; }
                else { file_dist_data << dist_matrix[y*WIDTH + x] << "\n"; }
            }
        }
        file_dist_data.close();
    } else {
        std::cout << "ERROR: Unable to open distance txt file.\n";
        throw std::runtime_error("ERROR: Unable to open distance txt file.\n");
    }
    // save mandelbulb light data
    std::cout << "\t> Saving light data." << std::endl;
    std::ofstream file_light_data("data/light_" + str_iter + ".txt");
    if (file_light_data.is_open()) {
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
                if (y < HEIGHT-1) { file_light_data << light_matrix[y*WIDTH + x] << ", "; }
                else { file_light_data << light_matrix[y*WIDTH + x] << "\n"; }
            }
        }
        file_light_data.close();
    } else {
        std::cout << "ERROR: Unable to open light txt file.\n";
        throw std::runtime_error("ERROR: Unable to open light txt file.\n");
    }
    // deallocate memory
    delete[] dist_matrix;
    delete[] light_matrix;
}

//==============================================
// MAIN
//==============================================
int main() {
    std::cout << "Started program." << std::endl;

    // calcScene();

    int ITERS = 500; 
    for (int iter = 0; iter < ITERS; ++iter) {
        CAM_ANG_HOR = (double)iter * (2.0*PI / (double)ITERS);
        CAM_ANG_VER = deg2rad(20.0) * cos(2 * CAM_ANG_HOR);
        calcScene(iter);
        std::cout << std::endl;
    }

    std::cout << "Finished program." << std::endl;
    return 0;
}
