#latent sampler
# import parser module
import argparse as par


# Create the parser and add arguments
def main(args=None):
    description_str = "[latents_toolbox] Tool to calculate and append the UTM coordinates to a CSV file containing georeferenced entries."
    formatter = lambda prog: argparse.HelpFormatter(prog, width=120)  # noqa: E731
    parser = argparse.ArgumentParser(description=description_str,
                                     formatter_class=formatter)

    # input #########################
    parser.add_argument(
        "-i",
        "--source",
        type=str,
        help="CSV containing georeferenced entries to be matched against target entries using distance based criteria"
    )
    # latent
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        # default=None,
        help="CSV containing the target georeferenced entries to be matched against source entries using distance based criteria"
    )
    parser.add_argument(
        "-k",
        "--key",
        # default='key',
        type=str,
        help="Keyword that defines the field (columns) from source that will be appended to target."
    )
    # output #########################
    parser.add_argument(
        "-o",
        "--output",
        default='merged_latents.csv',
        type=str,
        help="File containing a coopy of the "
    )

    # parse arguments
    args = parser.parse_args(args)
    print (args)