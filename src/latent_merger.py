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

    # Check if the number of entries in the input and latent files match
    if len(df) != len(df_latent):
        print ('Error: input and latent files do not have the same number of entries.')
        exit()

    # Create the dataframe that will contain the merged data
    df_merged = pd.DataFrame()

    # Check if the --slim flag was provided. If so, only the relative_path, latitude [deg], longitude [deg] from the input file will be added
    if args.slim:
        df_merged = df[['relative_path', 'latitude [deg]', 'longitude [deg]']]
        # Print a message informing that only the relative_path, latitude [deg], longitude [deg] fields will be added because of the --slim flag
        print ('Flag --slim used. Only the relative_path, latitude [deg], longitude [deg] fields will be exported from the input file.')
    else:
        df_merged = df

    # From the original dataframe, get the index of the latitude and longitude columns
    lat_index = df.columns.get_loc('latitude [deg]')
    lon_index = df.columns.get_loc('longitude [deg]')

    # Check if the --utm flag was provided. If so, UTM coordinates will be generated from the input latitude and longitude
    if args.utm:
        # Print a message informing that UTM coordinates will be generated from the input latitude and longitude
        print ('Flag --utm used. UTM coordinates will be generated from the input latitude and longitude.')
        # Let's determine the UTM zone from the input longitude. Sample first entry
        lon = df['longitude [deg]'][0]
        # Determine the UTM zone
        utm_zone = int((lon + 180) / 6) + 1
        # Print the UTM zone
        print ('UTM zone: ' + str(utm_zone))
        # Create the UTM projection as a new object
        utm = pyproj.Proj(proj='utm', zone=utm_zone, ellps='WGS84', datum='WGS84')
        # For each entry in the dataframe, convert the latitude and longitude to UTM coordinates and add them to the dataframe
        # The UTM coluns are: "easting_utm", "northing_utm"
        easting, northing = utm(df['longitude [deg]'].values, df['latitude [deg]'].values)

        # Append the new columns to the dataframe df_merged (they are numpy.ndarrays)
        df_merged['northing_utm [m]'] = northing.tolist()
        df_merged['easting_utm [m]'] = easting.tolist()

    # Append the latent variables to the merged dataframe. Use only the fields starting with "latent_"
    # First we filter the latent dataframe to only contain the fields starting with "latent_"
    df_latent = df_latent.filter(regex='latent_')
    df_merged = pd.concat([df_merged, df_latent], axis=1)

    # Print the total number of entries in the merged dataframe. Also print the number of columns
    # It should match those from the input file
    print ('Merged dataframe has ' + str(len(df_merged)) + ' entries and ' + str(len(df_merged.columns)) + ' columns.')

    print ('Writing merged dataframe to file: ' + args.output)
    # Write the merged dataframe to a csv file``
    df_merged.to_csv(args.output, index=False)

# Add main as the entry point for the script
if __name__ == "__main__":
    main()