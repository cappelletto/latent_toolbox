# Python script that reads a CSV file containing rows with georeferenced entries. There are two columns named latitude and longitude.
# The script reads the CSV file and convert the latitude and longitude values to northing and easting values using the UTM projection. The UTM zone is determined by the longitude value.
# The first row contains the header, we use the header to determine the column index of the latitude and longitude values.
# Data is stored in a pandas dataframe and written to a new CSV file.

import sys
import csv
import pyproj
import pandas as pd
import argparse

#TODO: Refactor to add main function as entrypoint (required for pyproject.toml console script installation)

def main(args=None):
    parser = argparse.ArgumentParser(
        description="Calculate and plot the confusion matrix from a CSV file containing the predictions and targets"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Path to the input CSV file with the predictions and targets",
    )
    # Output filename is optional
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Path to the output file with the confusion matrix image",
    )

    args = parser.parse_args()
    # Check if the provided file exists
    # If the file does not exist, the script will exit
    try:
    try:
        with open(args.input, "r") as f:
            pass
    except FileNotFoundError as e:
        print("Provided input file: [" + args.input + "] not found.")
        exit()
    filename = args.input
        
    # Check if an output filename is provided (second argumnt)
    # If no output filename is provided, we append '_utm' to the input filename
    if args.output is None:
        print ('No output filename provided. The output filename will be the input filename with _utm appended to it.')
        # It can be a relative path, so we look for folder separators and split the filename
        filename_out = filename.split('/')[-1].split('.')[0] + '_utm.csv'
    else:
        print ('Output filename provided.')
        filename_out = args.output

    # Read the CSV file
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Get the header and determine the column index of the latitude and longitude values
    header = data[0]
    # TODO: User configurable header keys. This could be retrieved from oplab config.yaml
    # Check if the header contains the latitude and longitude keys
    if 'latitude [deg]' not in header or 'longitude [deg]' not in header:
        print('The header does not contain the "latitude [deg]" and/or "longitude [deg]" keys.')
        exit()

    lat_index = header.index('latitude [deg]')
    lon_index = header.index('longitude [deg]')

    # Create a pandas dataframe
    df = pd.DataFrame(data[1:], columns=header)

    # Determine the UTM zone using the latitude and longitude values
    utm_zone = int((float(df.iloc[0, lon_index]) + 180) / 6) + 1
    # Print the UTM zone
    print ('UTM zone: ' + str(utm_zone))

    # Create a UTM projection
    utm = pyproj.Proj(proj='utm', zone=utm_zone, ellps='WGS84', datum='WGS84')

    # Convert the latitude and longitude values to northing and easting values
    df['northing_utm [m]'], df['easting_utm [m]'] = utm(df.iloc[:, lon_index].values, df.iloc[:, lat_index].values)

    # Print summary information about northen and easting values. Let's print min, mean, max, and standard deviation.
    print ('Northing UTM [m]:')
    print (df['northing_utm [m]'].describe())
    print ('Easting UTM [m]:')
    print (df['easting_utm [m]'].describe())


    # Write the dataframe to a new CSV file
    df.to_csv(filename_out, index=False)

    # Print the total number of rows processed
    print ('\n------------------\nTotal number of rows processed: ' + str(len(df)))


if __name__ == "__main__":
    main()
