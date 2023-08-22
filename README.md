# Latent Toolbox

Welcome to the **Latent Toolbox** repository! This collection of Python modules is designed to facilitate various geospatial data processing tasks for your projects. Whether you're dealing with feature extraction, georeferencing, or spatial sampling, these modules provide efficient solutions to enhance your geospatial data pipeline.

## Modules

### 1. latent2csv

The `latent2csv` module simplifies the process of converting extracted features from datasets that use geoCLR or LGA into a more manageable CSV representation. This representation includes a suitable header, making it convenient for integration into Bayesian learning pipelines.

### 2. append_utm

The `append_utm` module offers a standalone script that addresses the common scenario of augmenting georeferencing information. It reads a CSV file containing latitude and longitude coordinates and appends the corresponding UTM coordinates (northing and easting) when they are missing. This module helps ensure your geospatial data is comprehensive and ready for further analysis.

### 3. latent_sampler

The `latent_sampler` module simplifies the process of sampling properties from one layer and aggregating them into another layer using spatial information, preferably in UTM coordinates. This operation resembles the concept of a join operation in Geographic Information System (GIS) solutions. The module streamlines this process, making it efficient and straightforward.

## Installation

To install the packages from this repository, you can use the provided `pyproject.toml` file along with the `pip` tool. Here's how:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/cappelletto/latent_toolbox.git
   ```

2. Navigate to the repository directory:

   ```bash
   cd latent_toolbox
   ```

3. Use `pip` to install the packages using the `pyproject.toml` file:

   ```bash
   pip install .
   ```

This will install all the necessary modules and dependencies for the Latent Toolbox.

## Usage

For detailed usage instructions and examples for each module, refer to the individual module's documentation within their respective directories.

---

Feel free to explore, utilize, and contribute to the Latent Toolbox repository as part of your geospatial data processing workflows compatible with the *oplab* pipeline. If you encounter any issues or have suggestions for improvements, please don't hesitate to open an issue or pull request.
