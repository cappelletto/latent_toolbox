import argparse
import pandas as pd
import numpy as np
from scipy.stats import kurtosis, skew

def calculate_statistics(data):
    mean = np.mean(data)
    variance = np.var(data)
    std_dev = np.std(data)
    kurt = kurtosis(data)
    skewness = skew(data)
    return mean, variance, std_dev, kurt, skewness

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Calculate summary statistics for a CSV file.')
    parser.add_argument('--input', type=str, help='Input CSV file name')
    parser.add_argument('--output', type=str, default=None, help='Output CSV file name (default: stats_input.csv)')
    args = parser.parse_args()

    # Load the CSV data into a DataFrame, using the first row as the header
    df = pd.read_csv(args.input, header=0)

    # Create a new DataFrame for statistics
    statistics_df = pd.DataFrame(columns=['latent'] + ['mean', 'variance', 'std_dev', 'kurtosis', 'skewness'])

    # Calculate statistics for each column and add a row for each statistic
    # Iterate over each column in the DataFrame, retrieve the header and data
    for column in df.columns:
        column_data = df[column]
        stats = calculate_statistics(column_data)
        print ("-------------------")
        print (column)
        print (stats)
        statistics_df.loc[len(statistics_df)] = [column] + list(stats)

    # Define the output file name
    if args.output is None:
        args.output = 'stats_' + args.input

    # Export the statistics to a CSV file
    statistics_df.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
