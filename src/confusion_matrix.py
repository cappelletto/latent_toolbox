# Python script to read CSV file containin output for a multi-class classifier:
# Filename: valid_ce_loss_test_elbo0001_recon100.csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse

def main(args=None):
    parser = argparse.ArgumentParser(description="Calculate and plot the confusion matrix from a CSV file containing the predictions and targets")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to the input CSV file with the predictions and targets")
    # Output filename is optional
    parser.add_argument("--output", "-o", type=str, default=None, help="Path to the output file with the confusion matrix image")
    # Add option to define target labels, default target_
    parser.add_argument("--target", "-t", type=str, default="target_", help="Prefix for the target labels (ground truth)")
    # Add option to define predicted labels, default pred_
    parser.add_argument("--pred", "-p", type=str, default="pred_", help="Prefix for the predicted labels (predictions)")
    # Add flag to indicate if we want to show the plot
    parser.add_argument("--show", "-s", action="store_true", help="Flag to indicate if we want to show the plot")
    args = parser.parse_args()

    # Read CSV file
    # Check if the input file exists
    # If the file does not exist, the script will exit
    try:
        with open(args.input, 'r') as f:
            pass
    except FileNotFoundError as e:
        print ("Provided input file: [" + args.input + "] not found.")
        exit()
    filename = args.input
    df = pd.read_csv(filename)

    # the target (ground truth) labels are the columns starting with "target_"
    # the predicted labels are the columns starting with "pred_"

    # Get the target labels
    target_labels = [col for col in df.columns if col.startswith(args.target)]
    # Get the predicted labels
    pred_labels = [col for col in df.columns if col.startswith(args.pred)]
    # Get the number of classes
    num_classes = len(target_labels)
    print("Number of classes: ", num_classes)
    # Get the number of samples
    num_samples = len(df)
    print("Number of samples: ", num_samples)

    # We want to create a confusion matrix of size num_classes x num_classes
    # Initialize the confusion matrix
    confusion_matrix = np.zeros((num_classes, num_classes))
    # We also calculate the confusion_matrix using the raw values (not argmax)
    # This is useful for the Brier score
    confusion_matrix_raw = np.zeros((num_classes, num_classes))

    # We also want to calculate the Brier score (MSE between the target and predicted labels)
    # We have one Brier score for one-hot (argmax) encoding and one for the raw values
    brier_score_onehot = 0.0
    brier_score_raw = 0.0

    # Iterate over the samples
    for i in range(num_samples):
        # Get the target label
        target_label = df.iloc[i][target_labels].to_numpy().argmax()
        # Get the predicted label
        pred_label = df.iloc[i][pred_labels].to_numpy().argmax()
        # Update the confusion matrix
        confusion_matrix[target_label, pred_label] += 1

        # Update the confusion matrix, using the raw values
        confusion_matrix_raw += np.outer(df.iloc[i][target_labels].to_numpy(), df.iloc[i][pred_labels].to_numpy())

        # Update the Brier score, using the argmax (one-hot encoding)
        brier_score_onehot += (target_label - pred_label) ** 2
        # Update the Brier score, using the raw values
        brier_score_raw += (df.iloc[i][target_labels].to_numpy() - df.iloc[i][pred_labels].to_numpy()) ** 2

    # Normalize the confusion matrices
    confusion_matrix = confusion_matrix / confusion_matrix.sum(axis=1)[:, np.newaxis]
    confusion_matrix_raw = confusion_matrix_raw / confusion_matrix_raw.sum(axis=1)[:, np.newaxis]
    # Print the content of the confusion matrix
    print(confusion_matrix)
    print(confusion_matrix_raw)
    brier_score_onehot /= num_samples
    brier_score_raw /= num_samples
    # Print the Brier score
    print("Brier score (one-hot): ", brier_score_onehot)
    print("Brier score (one-raw): ", brier_score_raw)

    # Calculate the accuracy for each class
    accuracy = np.diag(confusion_matrix)
    # Print the accuracy for each class
    for i in range(num_classes):
        print("Accuracy for class {}: {:.2f}".format(i, accuracy[i]))

    # Generate a figure to plot the confusion matrix
    fig = plt.figure()
    # define the plot siz to be full width of the page
    fig.set_size_inches(12, 8)
    ax = fig.add_subplot(111)
    # Plot the confusion matrix
    cax = ax.matshow(confusion_matrix)
    fig.colorbar(cax)
    # Set the labels for the x-axis
    ax.set_xticklabels([''] + target_labels)
    # Set the labels for the y-axis
    ax.set_yticklabels([''] + pred_labels)
    # Rotate the labels for the x-axis
    plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")
    # Set the title
    # plt.title('Confusion matrix')
    plt.title('Confusion matrix for ' + filename)
    # Add subtitle with the Brier scores
    # plt.suptitle('Brier score (one-hot):' + str(brier_score_onehot) + '\n Brier score (raw): ' + str(brier_score_raw) + '\n Confusion matrix raw:' + str(confusion_matrix_raw))
    # Set the x-axis label
    plt.xlabel('Target')
    # Set the y-axis label
    plt.ylabel('Predicted')
    # Check if we want to show the plot
    if args.show:
        plt.show()
    # Save the figure
    # Output filename is optional, check if it was provided
    if args.output is None:
        # If not provided, then use the input filename with .png extension
        output_file = os.path.splitext(filename)[0]
        # remove any preceding path from the filename
        output_file = os.path.basename(output_file)
    else:
        output_file = args.output

    # print current directory
    print("Current directory: ", os.getcwd())

    # Use the current directory as output directory
    output_file = os.path.join(os.getcwd(), output_file)
    # print output file path
    print("Exporting to output file path (prefix): ", output_file)

    # save as PNG
    fig.savefig(output_file + '.png', bbox_inches='tight')
    # save as SVG
    fig.savefig(output_file + '.svg', bbox_inches='tight')

    # Export the confusion matrix and the Brier score to CSV
    # Create a dataframe with the confusion matrix
    df_confusion_matrix = pd.DataFrame(confusion_matrix)
    # Add the target labels as columns
    df_confusion_matrix.columns = target_labels
    # Add the predicted labels as index
    df_confusion_matrix.index = pred_labels
    # Save the dataframe to CSV
    df_confusion_matrix.to_csv(output_file + '_confusion_matrix.csv')

    # Export the Briser score to CSV
    # Create a dataframe with the Brier score
    df_brier_score = pd.DataFrame([brier_score_onehot, brier_score_raw, accuracy])
    # Add the target labels as columns
    df_brier_score.columns = ['Scores']
    # Add the predicted labels as index
    df_brier_score.index = ['brier_score_onehot', 'brier_score_raw', 'accuracy']
    # Save the dataframe to CSV
    df_brier_score.to_csv(output_file + '_scores.csv')

if __name__ == "__main__":
    main()