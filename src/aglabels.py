import pandas as pd
import argparse

def aggregate_labels(input_file, output_file, labels_column):
    # Load the CSV data into a DataFrame
    df = pd.read_csv(input_file)

    # Initialize an empty DataFrame to store the aggregated data
    output_df = pd.DataFrame(columns=df.columns)

    # Initialize variables to keep track of the current UUID and rows for aggregation
    current_uuid = None
    rows_to_aggregate = []

    # Iterate over each row in the input DataFrame
    for index, row in df.iterrows():
        if row['UUID'] != current_uuid:
            # If a new UUID is encountered, aggregate the labels for the previous UUID
            if current_uuid is not None:
                aggregated_labels = pd.DataFrame(rows_to_aggregate).mean()
                output_row = df.loc[index - 1, df.columns != 'UUID']  # Copy the first input row
                output_row[df.columns[df.columns.str.startswith(labels_column)]] = aggregated_labels
                output_df = output_df.append(output_row, ignore_index=True)

            # Reset variables for the new UUID
            current_uuid = row['UUID']
            rows_to_aggregate = []

        # Collect rows with the same UUID for aggregation
        rows_to_aggregate.append(row[df.columns.str.startswith(labels_column)])

    # Aggregate the labels for the last UUID encountered
    if current_uuid is not None:
        aggregated_labels = pd.DataFrame(rows_to_aggregate).mean()
        output_row = df.loc[len(df) - 1, df.columns != 'UUID']  # Copy the last input row
        output_row[df.columns[df.columns.str.startswith(labels_column)]] = aggregated_labels
        output_df = output_df.append(output_row, ignore_index=True)

    # Save the aggregated data to a new CSV file
    output_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate labels in a CSV file by UUID")
    parser.add_argument("--input", required=True, help="Input CSV file path")
    parser.add_argument("--output", required=True, help="Output CSV file path")
    parser.add_argument("--labels", required=True, help="Name of the labels column (e.g., labels_)")
    args = parser.parse_args()

    aggregate_labels(args.input, args.output, args.labels)
