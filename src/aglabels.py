import pandas as pd
import argparse


# Module that aggregates the ground truth or predicted labels from a 1-N mapping CSV
# The content of the labels are expected to be already available in one-hot-encoding format but no normalization is required nor enforced
# The rest of the fields (columns) are assumed to be repreated copies of the same content, so we use the first unique entry for such set
# Sets are defined as collection of rows sharing the same UUID (unique identifier)


def aggregate_labels(input_file, output_file, labels_column, uuid_column):
    # Load the CSV data into a DataFrame
    df = pd.read_csv(input_file)

    # Initialize an empty DataFrame to store the aggregated data
    output_df = pd.DataFrame(columns=df.columns)

    # Initialize variables to keep track of the current UUID and rows for aggregation
    current_uuid = None
    rows_to_aggregate = []

    print("Aggregating labels in the input CSV file...")
    N = len(df)
    print("Total number of rows: %d" % N)

    unique_rows = 1
    # Iterate over each row in the input DataFrame
    for index, row in df.iterrows():
        if row[uuid_column] != current_uuid:
            # If a new UUID is encountered, aggregate the labels for the previous UUID
            if current_uuid is not None:
                aggregated_labels = pd.DataFrame(rows_to_aggregate).mean()
                output_row = df.loc[index - 1].copy()  # Copy the first input row
                output_row[
                    df.columns[df.columns.str.startswith(labels_column)]
                ] = aggregated_labels
                # Let's append the output_row to the dataframe
                # output_df = output_df.append(output_row, ignore_index=True)
                # use concat to append the output_row to the dataframe
                # first convert the output_row to a dataframe
                output_row = pd.DataFrame(output_row).transpose()
                # then use concat to append the output_row to the dataframe
                output_df = pd.concat([output_df, output_row], ignore_index=True)

            # Reset variables for the new UUID
            current_uuid = row[uuid_column]
            rows_to_aggregate = []
            unique_rows += 1
            # print every 10 unique rows
            if unique_rows % 20 == 0:
                print("Unique rows processed: %d /" % unique_rows, N)

        # Collect rows with the same UUID for aggregation
        rows_to_aggregate.append(row[df.columns.str.startswith(labels_column)])

    # Aggregate the labels for the last UUID encountered
    if current_uuid is not None:
        aggregated_labels = pd.DataFrame(rows_to_aggregate).mean()
        output_row = df.loc[len(df) - 1].copy()  # Copy the last input row
        output_row[
            df.columns[df.columns.str.startswith(labels_column)]
        ] = aggregated_labels
        output_row = pd.DataFrame(output_row).transpose()
        # then use concat to append the output_row to the dataframe
        output_df = pd.concat([output_df, output_row], ignore_index=True)
        # output_df = output_df.append(output_row, ignore_index=True)

    print("Total number of unique rows: %d" % unique_rows)

    # Save the aggregated data to a new CSV file
    output_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Aggregate labels in a CSV file by UUID"
    )
    parser.add_argument(
        "--input", required=True, help="Input CSV file path [mandatory]"
    )
    parser.add_argument(
        "--output", required=True, help="Output CSV file path [mandatory]"
    )
    parser.add_argument(
        "--labels", required=True, help="Name of the labels column (e.g., labels_) that will be aggregated. They are expected to be numerical values"
    )
    parser.add_argument(
        "--uuid",
        required=True,
        help="Name of unique identifier column (e.g., relative_path, UUID). This key will be used to define the set of rows that will be aggregated into a single output row",
    )
    args = parser.parse_args()

    aggregate_labels(args.input, args.output, args.labels, args.uuid)
