# Mandelbulb

Small project where I code a Mandelbulb-set renderer from scratch using both C++ and Python.

The cpp folder is the final product. The python folder was used for development, but does the same thing, just slower.

Compile the C++ code in the cpp/srs folder and run it to generate data. Compile with: g++ -Wall -Wextra -fopenmp .\srs\main.cpp -o program
Read the code's comments to understand what variables do -- useful if you want to play around and create different renderings. 

Plot data with python file: plot_data, which uses ffmpeg to create mp4 animations if you have rendered a series of frames. 
