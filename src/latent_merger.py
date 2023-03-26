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


def main(args=None):
    # Create the parser and add arguments
    description_str = "[latent_toolbox] Tool to append the latent variables to a CSV file containing georeferenced entries."
    formatter = lambda prog: argparse.HelpFormatter(prog, width=120)  # noqa: E731
    parser = argparse.ArgumentParser(description=description_str,
                                     formatter_class=formatter)

    # input #########################
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="CSV containing georeferenced entries to be matched against target entries using distance based criteria"
    )
    # latent
    parser.add_argument(
        "-l",
        "--latent",
        type=str,
        help="CSV containing the latent variables to be appended to the input dataset."
    )
    # output #########################
    parser.add_argument(
        "-o",
        "--output",
        default='merged_latents.csv',
        type=str,
        help="File containing a coopy of the "
    )
    # optional #########################
    parser.add_argument(
        "-k",
        "--key",
        default='relative_path',
        type=str,
        help="Keyword that defines the field (columns) from source that will be appended to target."
    )
    parser.add_argument(
        "-u",
        "--utm",
        action='store_true',
        help="Flag to indicate that UTM coordinates will be generated from input latitude and longitude."
    )
    parser.add_argument(
        "-s",
        "--slim",
        action='store_true',
        help="Flag to indicate that the output file will only contain the id, relative_path, georeferencing fields and latent variables."
    )

    # parse arguments
    args = parser.parse_args(args)

    # Check if the provided file exists
    # If the file does not exist, the script will exit
    try:
        with open(args.input, 'r') as f:
            pass
    except IOError:
        # Print error message with file name
        print ('Provided input file: [' + args.input + '] does not exist.')
        exit()

    # Check if the provided file exists
    # If the file does not exist, the script will exit
    try:
        with open(args.latent, 'r') as f:
            pass
    except IOError:
        print ('Provided latent file: [' + args.input + '] does not exist.')
        exit()

    # Check if the output file exists, print a warning message and continue
    if os.path.isfile(args.output):
        print ('Provided output file: [' + args.output + '] already exists. Overwriting...')


    # Read the input file as a pandas dataframe
    df = pd.read_csv(args.input)
    # Check if it has the required fields: relative_path, latitude [deg], longitude [deg]
    if not all(x in df.columns for x in ['relative_path', 'latitude [deg]', 'longitude [deg]']):
        print ('Input file: [' + args.input + '] does not have the required fields: relative_path, latitude [deg], longitude [deg].')
        exit()
    
    # Print the total number of entries in the input file. Also print the number of columns
    print ('Input has ' + str(len(df)) + ' entries and ' + str(len(df.columns)) + ' columns.')

    # Read the latent file as a pandas dataframe
    df_latent = pd.read_csv(args.latent)
    # Check if it has fields containing the latent key preffix: "latent_"
    if not any(x.startswith('latent_') for x in df_latent.columns):
        print ('Latent file: [' + args.latent + '] does not have any fields starting with "latent_"')
        exit()

    # Filter the latent dataframe to only contain the fields starting with "latent_"
    df_latent = df_latent.filter(regex='latent_')
    # Print the total number of entries in the latent file. Also print the number of latent columns
    print ('Latent file has ' + str(len(df_latent)) + ' entries and ' + str(len(df_latent.columns)) + ' columns.')
    
# Add main as the entry point for the script
if __name__ == "__main__":
    main()