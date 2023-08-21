import argparse
import numpy as np
import pandas as pd
import os

def main(args=None):
    parser = argparse.ArgumentParser(description="Convert Numpy file containing latent representation to CSV file.")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to the input Numpy file")
    # Output filename is optional
    parser.add_argument("--output", "-o", type=str, default=None, help="Path to the output CSV file")
    args = parser.parse_args()

    # Check if the input file exists
    # If the file does not exist, the script will exit
    try:
        with open(args.input, 'r') as f:
            pass
    except FileNotFoundError as e:
        print ("Provided input file: [" + args.input + "] not found.")
        exit()

    input_file = args.input

    # Check if output file has been provided - if not, then use the input filename with .csv extension
    if args.output is None:
        output_file = os.path.splitext(input_file)[0] + '.csv'
    else:
        output_file = args.output

    # Check if the output file exists, print a warning message and continue
    if os.path.isfile(output_file):
        print ('Provided output file: [' + output_file + '] already exists. Overwriting...')

    latents_np = np.load(input_file)
    latents_dim = latents_np.shape[1]
    entries = latents_np.shape[0]

    print("Total entries:", entries)
    print("Latents dimensions:", latents_dim)

    header = ["latent_" + str(i) for i in range(latents_dim)]
    df = pd.DataFrame(latents_np, columns=header)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()