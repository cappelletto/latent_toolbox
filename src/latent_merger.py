# latent_merge.py

# Description: This script appends the latent variables to the original georeferenced dataset (e.g. sampled_images.csv)
# Author: Jose Cappelletto - Ocean Perception Lab - University of Southampton, UK
# Email: cappelletto [at] gmail.com
# Date: 2023-03-15
# The latent variables are assumed to be in the same order as the original dataset and stored in a csv file as:
# id, latent_0, latent_1,...., latent_n-1

# The original dataset is assumed to have at least one column acting as unique identifier and the georeferenced coordinates as latitude and longitude
# The oplab format is assumed, but the script can be easily modified to work with other formats
# -, relative_path, latitude [deg], longitude [deg], altitude [m], heading [deg], pitch [deg], roll [deg], timestamp [s] , ....

# The output is a csv file with the original dataset and the latent variables appended to it
# -, relative_path, latitude [deg], longitude [deg], ..., latent_0, latent_1, ..., latent_n-1

# Mandatory arguments:
# --input: path to the original dataset
# --latent: path to the latent variables csv file
# --output: path to the output file

# Optional arguments:
# --utm: flag to indicate that UTM coordinates will be generated from input latitude and longitude
# --slim: flag to indicate that the output file will only contain the id, relative_path, georeferencing fields and latent variables
# --key: name of the column acting as unique identifier in the original dataset. Default is 'relative_path'

# Include libraries for argument parsing, pyproj for coordinate transformations, and pandas for data manipulation
import argparse
import pyproj
import pandas as pd
import os, sys, csv