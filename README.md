# Mandelbulb

Small, simple project where I code a Mandelbulb-set renderer from scratch using both C++ and Python.

The cpp folder is the final product. The python folder was used for development, but does the same thing, just slower.

Compile the C++ code in the cpp/srs folder and run it to generate data.
Compile from within the cpp folder uisng (windows): g++ -Wall -Wextra -fopenmp .\srs\main.cpp -o program
Read the code's comments to understand what variables do -- useful if you want to play around and create different renderings.

Plot data with python file: plot_data, which uses ffmpeg to create mp4 animations if you have rendered a series of frames.
Get it here: https://ffmpeg.org/download.html

![plot](./cpp/mandelbulb.gif)

This project combined some interesting topics:
> Ray marching: to find out what the camera sees.
> Signed Distance Functions: to find out how far a ray can safely march in a particular direction.
> Lots of Linear Algebra: for rotating the camera and light source.

You can read more on these topics here:
> http://blog.hvidtfeldts.net/index.php/2011/06/distance-estimated-3d-fractals-part-i/
> http://celarek.at/wp/wp-content/uploads/2014/05/realTimeFractalsReport.pdf
> https://www.3dgep.com/understanding-the-view-matrix/
