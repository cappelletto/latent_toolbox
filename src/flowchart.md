1. **Start:** The script begins execution.

2. **Parse Arguments:** The script parses command-line arguments using the `argparse` library.

3. **Check Source File:** The script checks if the source CSV file exists. If not, it displays a message and exits.

4. **Check Target File:** The script checks if the target CSV file exists. If not, it displays a message and exits.

5. **Check Output File:** The script checks if the specified output file exists. If it does, it displays a message about overwriting.

6. **Read Source Data:** The script reads the source CSV file using Pandas, creating a DataFrame `df_source`.

7. **Read Target Data:** The script reads the target CSV file using Pandas, creating a DataFrame `df_target`.

8. **Check Key Field:** The script checks if the specified key field exists in the source DataFrame. If not, it displays a message and exits.

9. **Check UTM Fields:** The script checks if the UTM fields 'northing_utm [m]' and 'easting_utm [m]' exist in both the source and target DataFrames. If not, it displays a message and exits.

10. **Create Results DataFrame:** A new DataFrame `df_results` is created to store the results.

11. **Loop Over Target Entries:** For each entry in the target DataFrame:
    - Calculate Euclidean Distance: The script calculates the Euclidean distance between the current target entry and all source entries using the UTM coordinates.
    - Sort Source Entries: The source entries are sorted by distance in ascending order.
    - Filter Source Entries: Entries from the source DataFrame are filtered based on the distance threshold.
    - If No Matches Found: If no matches are found, the script displays a message and continues to the next target entry.
    - If Matches Found:
        - For Closest Mode: The closest match is selected from the filtered source entries.
            - Append Source Fields: The fields specified by the key are appended to the target entry in the results DataFrame.
            - Record Match Distance: The distance of the match is recorded.
        - For All Mode: All matches are appended to the target entry in the results DataFrame.
            - Append Source Fields: The fields specified by the key are appended for each match.
            - Record Match Distance: The distance of each match is recorded.

12. **Interrupt Handling:** The script checks for a KeyboardInterrupt signal (CTRL+C) and displays a message if it's received.

13. **Save Results:** The results DataFrame is saved to the specified output file as a CSV.

14. **End:** The script ends.
