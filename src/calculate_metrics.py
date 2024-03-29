# Python script to read CSV file containin output for a multi-class classifier:
# Filename: valid_ce_loss_test_elbo0001_recon100.csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse


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
    # Add option to define target labels, default target_
    parser.add_argument(
        "--target",
        "-t",
        type=str,
        default="target_",
        help="Prefix for the target labels (ground truth)",
    )
    # Add option to define predicted labels, default pred_
    parser.add_argument(
        "--pred",
        "-p",
        type=str,
        default="pred_",
        help="Prefix for the predicted labels (predictions)",
    )
    # Add option to define predicted labels, default pred_
    parser.add_argument(
        "--uncert",
        "-u",
        type=str,
        default="uncertainty_",
        help="Prefix for the uncertainty of predictions",
    )
    # Add flag to indicate if we want to show the plot
    parser.add_argument(
        "--show",
        "-s",
        action="store_true",
        help="Flag to indicate if we want to show the plot",
    )
    # Add flag to indicate if we want to show the plot
    parser.add_argument(
        "--noplot",
        "-n",
        action="store_true",
        help="Flag to disable generation and saving plots",
    )
    args = parser.parse_args()

    # Read CSV file
    # Check if the input file exists
    # If the file does not exist, the script will exit
    try:
        with open(args.input, "r") as f:
            pass
    except FileNotFoundError as e:
        print("Provided input file: [" + args.input + "] not found.")
        exit()
    filename = args.input
    df = pd.read_csv(filename)

    # the target (ground truth) labels are the columns starting with "target_"
    # the predicted labels are the columns starting with "pred_"

    # Get the target labels
    target_labels = [col for col in df.columns if col.startswith(args.target)]
    # From the target labels, get the class names. They are the labels after the last underscore _
    class_names = [label.split("_")[-1] for label in target_labels]
    # Get the predicted labels
    pred_labels = [col for col in df.columns if col.startswith(args.pred)]
    # Get the predicted labels
    uncert_labels = [col for col in df.columns if col.startswith(args.uncert)]
    # Get the number of classes
    num_classes = len(target_labels)
    print("Number of classes: ", num_classes)
    print("Class names: ", class_names)
    # Get the number of samples
    num_samples = len(df)
    print("Number of samples (rows): ", num_samples)

    # We want to create a confusion matrix of size num_classes x num_classes
    # Initialize the confusion matrix
    confusion_matrix = np.zeros((num_classes, num_classes))
    # We also calculate the confusion_matrix using the raw values (not argmax)
    # This is useful for the Brier score
    confusion_matrix_raw = np.zeros((num_classes, num_classes))

    # We also want to calculate the Brier score (MSE between the target and predicted labels)
    # We have one Brier score for one-hot (argmax) encoding and one for the raw values
    # brier_score_onehot = 0.0
    brier_score_raw = 0.0
    uncertainty = 0.0

    # Iterate over the samples
    for i in range(num_samples):
        target_label_index = df.iloc[i][target_labels].to_numpy().argmax()
        # Get the predicted label, in one-hot encoding winner takes all reduction of predicted probabilities
        pred_label_index = df.iloc[i][pred_labels].to_numpy().argmax()
        # Update the confusion matrix
        confusion_matrix[target_label_index, pred_label_index] += 1

        # TODO: Brier score, using the argmax (one-hot encoding) [ that seems to be only valid if using binary predictor, single class ]
        # Update the Brier score, using the raw values. This is the MSE between the target and predicted labels
        brier_score_raw += (
            df.iloc[i][target_labels].to_numpy() - df.iloc[i][pred_labels].to_numpy()
        ) ** 2

        # Accumulate the uncertainty
        uncertainty += df.iloc[i][uncert_labels].to_numpy()

    print("Confusion matrix:")
    print(confusion_matrix)
    # Print the Brier score
    brier_score_raw /= num_samples
    print("Brier score (raw-MSE):\t\t", brier_score_raw)
    # Normalize and then print the uncertainty
    uncertainty /= num_samples
    print("Uncertainty:\t\t", uncertainty)

    # Calculate each component TP, TN, FP, FN
    TP = np.diag(confusion_matrix)
    TN = np.sum(confusion_matrix) - (
        np.sum(confusion_matrix, axis=0) + np.sum(confusion_matrix, axis=1) - TP
    )
    FP = np.sum(confusion_matrix, axis=0) - TP
    FN = np.sum(confusion_matrix, axis=1) - TP

    # Normalize the confusion matrices (normalizing before or after calculating the components does not change the results)
    confusion_matrix = confusion_matrix / confusion_matrix.sum(axis=1)[:, np.newaxis]
    mcc = (TP * TN - FP * FN) / np.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))
    print("MCC:\t\t", mcc)

    # Calculate the accuracy for each class from the confusion matrix
    accuracy = np.diag(confusion_matrix)
    # Calculate the recall for each class
    recall = np.diag(confusion_matrix) / np.sum(confusion_matrix, axis=1)
    # Calculate the precision for each class
    precision = np.diag(confusion_matrix) / np.sum(confusion_matrix, axis=0)
    # print("Precision:\t\t", precision)
    # From teh recall and precision, calculate the F1 score
    f1 = 2 * (precision * recall) / (precision + recall)
    # calculate the class frequency
    class_frequency = np.sum(confusion_matrix, axis=1) / np.sum(confusion_matrix)
    # calculate the weighted accuracy
    weighted_accuracy = np.sum(accuracy * class_frequency)
    # calculate the weighted F1 score (micro)
    weighted_f1 = np.sum(f1 * class_frequency)
    # Calculate the Matthews Correlation Coefficient (MCC)
    # MCC = (TP * TN - FP * FN) / sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))

    # Print the accuracy for each class
    for i in range(num_classes):
        print("Accuracy for class ", class_names[i], ":\t", accuracy[i])

    print("F1 score for ALL classes: ", f1)
    print("micro F1 score: {:.2f}".format(weighted_f1))
    # Output filename is optional, check if it was provided
    if args.output is None:
        # If not provided, then use the input filename with .png extension
        output_file = os.path.splitext(filename)[0]
        # remove any preceding path from the filename
        output_file = os.path.basename(output_file)
    else:
        output_file = args.output

    # Use the current directory as output directory
    output_file = os.path.join(os.getcwd(), output_file)
    # print output file path
    print("Exporting to output file path (prefix): ", output_file)

    # Check if plotting is disabled
    if args.noplot is not True:
        # Generate a figure to plot the confusion matrix
        fig = plt.figure()
        # define the plot siz to be full width of the page
        fig.set_size_inches(12, 8)
        ax = fig.add_subplot(111)
        # Plot the confusion matrix
        cax = ax.matshow(confusion_matrix, cmap=plt.cm.inferno)
        # Print the confusion matrix values in the plot
        for (i, j), z in np.ndenumerate(confusion_matrix):
            ax.text(j, i, "{:0.2f}".format(z), ha="center", va="center", color="white")

        # set the colorbar, and the ticks values every 0.25
        fig.colorbar(cax, ticks=[0, 0.25, 0.5, 0.75, 1])
        # set the colorbar limits to 0.0 and 1.0
        cax.set_clim(0.0, 1.0)

        # Set the labels for the x-axis
        ax.set_xticklabels(["pred_"] + class_names)
        # Set the labels for the y-axis
        ax.set_yticklabels(["target_"] + class_names)
        # Rotate the labels for the x-axis
        plt.setp(ax.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")
        # Set the title
        # plt.title('Confusion matrix')
        plt.title("Confusion matrix for " + filename)
        # Add subtitle with the Brier scores
        # plt.suptitle('Brier score (one-hot):' + str(brier_score_onehot) + '\n Brier score (raw): ' + str(brier_score_raw) + '\n Confusion matrix raw:' + str(confusion_matrix_raw))
        # Set the x-axis label
        plt.xlabel("Target")
        # Set the y-axis label
        plt.ylabel("Predicted")
        # Check if we want to show the plot
        if args.show:
            plt.show()
        # Save the figure

        # save as PNG
        fig.savefig(output_file + ".png", bbox_inches="tight")
        # save as SVG
        fig.savefig(output_file + ".svg", bbox_inches="tight")

    print("------------------------")
    print("Exporting confusion matrix and scores to CSV")
    # Export the confusion matrix and the Brier score to CSV
    # Create a dataframe with the confusion matrix
    df_confusion_matrix = pd.DataFrame(confusion_matrix)
    # Add the target labels as columns
    df_confusion_matrix.columns = target_labels
    # Add the predicted labels as index
    df_confusion_matrix.index = pred_labels
    # Save the dataframe to CSV
    df_confusion_matrix.to_csv(output_file + "_confusion_matrix.csv")

    # Export a summary of the scores: Brier score and accuracy
    # The output CSV will be parsed by a batch script to generate a summary of the scores for all the experiments
    # Here is a sample of the output CSV file:
    # input_file, brier_score_onehot, brier_score_raw_label_0, brier_score_raw_label_1, ..., accuracy_label_0, accuracy_label_1, ...
    # valid_mean_20m_ae_L15m_h16_1841.csv, 0.0, 0.0, 0.0, ..., 1.0, 1.0, ...

    # Prepare the information to be saved to CSV. Note that we need to add the input filename
    # The input filename is the basename of the input file, without the extension
    # Get the basename of the input file
    input_file = os.path.basename(filename)
    # Remove the extension
    input_file = os.path.splitext(input_file)[0]

    # Create a dataframe with the input filename and the Brier score one-shot. The Brier score raw is a vector, we need to add each element as a column

    # Create the output dataframe, appending as columns the input filename and the Brier score one-hot
    df_scores = pd.DataFrame([[input_file, weighted_f1]])

    # Add the target labels as columns
    df_scores.columns = ["input_file", "mF1"]

    for i in range(num_classes):
        df_scores["F1_" + class_names[i]] = f1[i]

    for i in range(num_classes):
        df_scores["MCC_" + class_names[i]] = mcc[i]

    # Add the Brier MSE raw value (each element is an individual column of the dataframe)
    for i in range(num_classes):
        df_scores["brier_mse_" + class_names[i]] = brier_score_raw[i]
    df_scores["brier_mse"] = brier_score_raw.mean()

    # Insert uncertainties per class, and mean uncertainty
    for i in range(num_classes):
        df_scores["uncertainty_" + class_names[i]] = uncertainty[i]
    df_scores["mean_uncertainty"] = uncertainty.mean()

    # Add the accuracy (each element is an individual column of the dataframe)
    for i in range(num_classes):
        df_scores["accuracy_" + class_names[i]] = accuracy[i]

    # Save the dataframe to CSV
    df_scores.to_csv(output_file + "_scores.csv")


if __name__ == "__main__":
    main()
