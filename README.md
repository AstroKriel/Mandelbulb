# Mandelbulb

Small, simple project where I code a Mandelbulb-set renderer from scratch using both C++ and Python.

The cpp folder is the final product. The python folder was used for development, but does the same thing, just slower.

Compile the C++ code from within the cpp/srs folder uisng (windows): 
  g++ -Wall -Wextra -fopenmp .\srs\main.cpp -o program
and run it to generate data.

Plot data with python plotting file 'plot_data.' This code relies on ffmpeg to create mp4 animations. You can get it here: https://ffmpeg.org/download.html

This project combined some interesting topics:
- Ray marching: to find out what the camera sees.
- Signed Distance Functions: to find out how far a ray can safely march in a particular direction.
- Lots of Linear Algebra: for rotating the camera and light source.

You can read more on these topics here:
- http://blog.hvidtfeldts.net/index.php/2011/06/distance-estimated-3d-fractals-part-i/
- http://celarek.at/wp/wp-content/uploads/2014/05/realTimeFractalsReport.pdf
- https://www.3dgep.com/understanding-the-view-matrix/

![plot](./cpp/mandelbulb.gif)
<img src=./cpp/mandelbulb.gif width="100" height="100">
