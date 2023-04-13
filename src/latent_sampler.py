#latent sampler
# import parser module
import argparse
import pandas as pd
import numpy as np
import os 
import sys
import signal

# Add handler for the SIGINT signal
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
#    sys.exit(0)


# Create the parser and add arguments
def main(args=None):

    # # Register the signal handler
    # signal.signal(signal.SIGINT, signal_handler)

    description_str = \
        "[latents_toolbox] Tool to sample rows from a SOURCE to append to the matching entry in the TARGET layer. Matching algorithms are based on the UTM georef information"
    formatter = lambda prog: argparse.HelpFormatter(prog, width=120)  # noqa: E731
    parser = argparse.ArgumentParser(description=description_str,
                                     formatter_class=formatter)

    # input #########################
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        help="CSV containing the SOURCE of georeferenced entries to be matched against target entries using distance based criteria"
    )
    # latent
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        # default=None,
        help="CSV containing the TARGET of georeferenced entries to be matched against source entries using distance based criteria"
    )
    parser.add_argument(
        "-k",
        "--key",
        # default=None,
        type=str,
        help="Keyword that defines the field (columns) from source that will be appended to target. If None, then all the fields wil be appended."
    )
    # output #########################
    parser.add_argument(
        "-o",
        "--output",
        default='sampled_latents.csv',
        type=str,
        help="File containing a copy of the TARGET layer with the sampled (matching) entries from the SOURCE layer appended to it."
    )

    # distance #########################
    parser.add_argument(
        "-d",
        "--distance",
        default=-1.0,
        type=float,
        help="Distance threshold that defines the maximum distance between the SOURCE and TARGET entries to be considered a match. Set to negative value if you do not want a limit."
    )

    # mode #########################
    parser.add_argument(
        "-m",
        "--mode",
        default='closest',
        type=str,
        help="Mode of the sampler. Options are: 'closest' (default), 'random', 'all'."
    )

    # parse arguments
    args = parser.parse_args(args)
    print (args)

    # Check if the provided SOURCE file exists
    # If the file does not exist, the script will exit
    try:
        with open(args.source, 'r') as f:
            print ("SOURCE file found")
    except IOError:
        print ("SOURCE file not found")
        exit()
    
    # Check if the provided file exists
    # If the file does not exist, the script will exit
    try:
        with open(args.target, 'r') as f:
            print ("TARGET file found")
    except IOError:
        print ("TARGET file not found")
        exit()
    
    # Check if the output file exists, print a warning message and continue
    if os.path.isfile(args.output):
        print ('Provided output file: [' + args.output + '] already exists. Overwriting...')

    # Read the input SOURCE file as a pandas dataframe
    df_source = pd.read_csv(args.source)

    # Read the input TARGET file as a pandas dataframe
    df_target = pd.read_csv(args.target)

    # Check if the provided key exists in the SOURCE file
    if args.key is not None:
        # Check if the provided key exists in the df_source.columns using regex for string expansion (e.g. 'key' will match 'key_1', 'key_2', etc.)
        if not any(args.key in s for s in df_source.columns):
            print ("Provided key: [" + args.key + "] not found in SOURCE file.")
            exit()
        else:
            print ("Provided key: [" + args.key + "] found in SOURCE file.")

        # If the key does not exist, the script will exit

        # if args.key not in df_source.columns:
        #     print ("Provided key: [" + args.key + "] not found in SOURCE file.")
        #     exit()
        # else:
        #     print ("Provided key: [" + args.key + "] found in SOURCE file.")

    # Check if the SOURCE dataframe contains the UTM fields: 'northing_utm [m]' and 'easting_utm [m]'
    # We could calculate them, but for now we will assume that they are already there. External tools to convert to UTM is already provided twice
    if 'northing_utm [m]' not in df_source.columns:
        print ("SOURCE file does not contain the northing_utm [m] field.")
        exit()
    if 'easting_utm [m]' not in df_source.columns:
        print ("SOURCE file does not contain the easting_utm [m] field.")
        exit()

    # Check if the TARGET dataframe contains the UTM fields: 'northing_utm [m]' and 'easting_utm [m]'
    if 'northing_utm [m]' not in df_target.columns:
        print ("TARGET file does not contain the northing_utm [m] field.")
        exit()
    if 'easting_utm [m]' not in df_target.columns:
        print ("TARGET file does not contain the easting_utm [m] field.")
        exit()
    
    # The sampler algorithm (for now) consists in the closest match using the euclidean distance between the UTM coordinates
    # The distance parameter is used to filter out the matches that are too far away. If distance < 0.0 then no filtering is applied
    # The algorithm will iterate over the TARGET entries and find the closest match in the SOURCE entries. The mapping is unidirectional so the direction matters
    # Then, append the SOURCE entry to the TARGET entry. If the key is provided, then only the fields that match the key will be appended. If the key is None, then all the fields will be appended

    # Create a new dataframe to store the results
    df_results = pd.DataFrame(columns=df_target.columns)
    # Iterate over the TARGET entries
    try:
        # the keys to append are known in advance
        if args.key is not None:
            fields_to_append = df_source.filter(regex=args.key + "*").columns
        else:
            fields_to_append = df_source.columns

        for index, row in df_target.iterrows():
            # Print the number of the current entry being processed
            # print ("Processing TARGET entry: " + str(index))
            # Calculate the euclidean distance between the current TARGET entry and all the SOURCE entries
            df_source['distance'] = np.sqrt((df_source['northing_utm [m]'] - row['northing_utm [m]'])**2 + (df_source['easting_utm [m]'] - row['easting_utm [m]'])**2)
            # Sort the SOURCE entries by distance
            df_source = df_source.sort_values(by=['distance'])
            
            # We check if the distance threshold is met. If args.distance < 0.0, then no filtering is applied
            # Create a new dataframe with the entries that are within the threshold distance
            if args.distance < 0.0:
                df_source_filtered = df_source
            else:
                df_source_filtered = df_source[df_source['distance'] < args.distance]

            # If there are no matches, then we skip the entry
            if df_source_filtered.empty:
                print ("No match found for TARGET entry: " + str(index))
                continue

            # Check args.mode for options: closest, random (uninplemented), all
            # If mode is closest, then we only append the closest match from df_source_filtered
            if args.mode == 'closest':
                # Get the closest match (single entry)
                closest_match = df_source_filtered.iloc[0]
                print ("Match found for TARGET entry: " + str(index))

                for field in fields_to_append:
                    row['source_' + field] = closest_match[field]


                # Append the TARGET entry to the results dataframe
                df_results = pd.concat([df_results, row.to_frame().T], ignore_index=True)

            elif args.mode == 'all':
                # Append all the matches from df_source_filtered to the TARGET entry
                n = len(df_source_filtered.index)
                print ("Appending [" + str(n) + "] matches from SOURCE to TARGET: " + str (index))
                # Iterate over the matches
                for index, match in df_source_filtered.iterrows():
                    # If the key is provided, then only the fields that match the key will be appended. If the key is None, then all the fields will be appended
                    for field in fields_to_append:
                        row['source_' + field] = match[field]
                    # Append the TARGET entry to the results dataframe
                    df_results = pd.concat([df_results, row.to_frame().T], ignore_index=True)


        # Interrupt the execution if the SIGNAL was received
    except KeyboardInterrupt:
        print("Search interrupted by user (CTRL + C)")

    # Save the results dataframe to the provided output file
    print ("Saving results to: " + args.output)
    df_results.to_csv(args.output, index=False)

# Add main as the entry point for the script
if __name__ == "__main__":
    main()