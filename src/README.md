# Latent Sampler Python Script

This repository contains a Python script designed for spatial sampling between two datasets loaded from CSV files. The sampling process is based on UTM coordinates (northing_utm and easting_utm). The script is useful for matching georeferenced entries from a source dataset to corresponding entries in a target dataset using distance-based criteria.

## Table of Contents

- [Introduction](#introduction)
- [Usage](#usage)
- [Requirements](#requirements)
- [Installation](#installation)
- [Examples](#examples)
- [Options](#options)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The **Latent Sampler Python Script** facilitates spatial sampling of georeferenced entries between a source dataset and a target dataset. It calculates the distance between UTM coordinates of entries and applies a distance threshold to identify matching entries. Depending on the selected mode, the script appends matching entries from the source dataset to the target dataset.

## Usage

To use the script, provide the paths to the source and target CSV files, specify the UTM key columns, set the distance threshold, and choose a sampling mode. The script will then perform spatial sampling and generate a new CSV file with the sampled results appended to the target dataset.

## Requirements

- Python 3.x
- Pandas
- NumPy

## Installation

1. Clone this repository or download the script directly.
2. Ensure you have the required libraries installed using the following command:
   
   ```bash
   pip install pandas numpy
   ```

## Examples

Here's an example of how to run the script:

```bash
python latent_sampler.py -s source_data.csv -t target_data.csv -k key_column -o sampled_results.csv -d 100 -m closest
```

In this example, the script will sample entries from `source_data.csv` to append to the corresponding entries in `target_data.csv` based on the UTM key column. The maximum distance for matching is set to 100 units, and the closest matching entries will be appended.

## Options

The script accepts several command-line options:

- `-s`, `--source`: Path to the CSV file containing the source dataset.
- `-t`, `--target`: Path to the CSV file containing the target dataset.
- `-k`, `--key`: Keyword specifying the key field(s) from the source dataset to match against the target dataset.
- `-o`, `--output`: Path to the output CSV file where results will be saved.
- `-d`, `--distance`: Distance threshold [m] for matching entries. Set to a negative value to disable distance filtering.
- `-m`, `--mode`: Mode of the sampler. Options are: 'closest', 'random', 'all'.

## Output

The script generates an output CSV file containing the sampled results appended to the target dataset. The columns from the source dataset that match the specified key are included in the output.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.
