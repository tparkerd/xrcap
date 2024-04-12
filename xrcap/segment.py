from __future__ import annotations

import argparse
import logging
import os
import re
from multiprocessing import cpu_count
from pprint import pformat
from typing import List, NamedTuple, Sequence

import cv2
import numpy as np
from rich.logging import RichHandler


SUPPORTED_INPUT_FILETYPES = ["raw", "png", "tif"]
SUPPORTED_OUTPUT_FILETYPES = ["raw", "png", "tif"]

class Threshold(NamedTuple):
    min : int = 1
    max : int = 255

__version__ = "0.0.0"

# TODO: REMOVE
def configure(*args, **kwargs):
    verbose = kwargs.get("verbose", False)
    path = kwargs.get("path", ["."])
    write_log_files = kwargs.get("write_log_files", True)

    # Configure logging, stderr and file logs
    logging_level = logging.INFO
    if verbose:
        logging_level = logging.DEBUG

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    consoleHandler = RichHandler()
    consoleHandler.setLevel(logging_level)
    rootLogger.addHandler(consoleHandler)

# TODO: Move to package.cli module
def __add_global_options(parser: argparse.ArgumentParser):
    """Add arguments common to all sub-commands (e.g., -V, -f, -n, etc.)"""
    parser.add_argument("-V", "--version", action="version", version=f'%(prog)s {__version__}')
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    parser.add_argument("-t", "--threads", metavar="N", type=int, default=cpu_count(), help="Specify upper limit for number of threads used during processing")
    parser.add_argument("-r", "-R", "--recursive", action="store_true", help="Perform action recursively")
    # parser.add_argument("--strict", action="store_true", help="Enable strict mode for matching file and directory names.")
    parser.add_argument("--no-log-files", dest="write_log_files", action="store_false", help="Disable writing log files")

    mutex_opts = parser.add_mutually_exclusive_group(required=False)
    mutex_opts.add_argument("-f", '--force', action="store_true", help="Force file creation and overwrite existing files (cannot be used in conjunction with -n)")
    mutex_opts.add_argument("-n", '--dry-run', dest='dryrun', action="store_true", help="Perform a trial run with no changes made (logs are still produced)")


def is_counting_number(x: str) -> int:
    err_msg = f"Downsample factor, '{x}', is invalid. It must be a positive integer."
    try:
        x = int(x)
    except ValueError:
        raise argparse.ArgumentTypeError(err_msg)
    else:
        if x <= 0:
            raise argparse.ArgumentTypeError(err_msg)
    return x


def is_valid_threshold(user_input: str) -> Threshold:
    err_msg = f"Invalid thresholds: '{user_input}'"
    # Case: a single value is specified
    try:
        x = int(user_input)
        print(f"{x=}")
    except ValueError:
        pass
    else:
        # Disallow negative values
        if x < 0:
            raise argparse.ArgumentTypeError(f"'{user_input}', cannot be a negative number")
        user_input = f"{x},"

    # Extract lowerbound and upperbounds from user input
    try:
        bounds = user_input.split(",")

        # Trim whitespace
        bounds = [s.strip() for s in bounds]

        # Adjust wonky values
        lbound, ubound = bounds
        if not lbound:  # undefined lowerbound threshold
            lbound = 1  # TODO: generalized this for any image bitdepth
        if not ubound:  # undefined upperbound threshold
            ubound = 255  # TODO: generalized this for any image bitdepth
        lbound, ubound = int(lbound), int(ubound)
        bounds = (lbound, ubound)
    except ValueError:
        raise argparse.ArgumentTypeError(err_msg)
    else:
        # If more than two values were provided, it's invalid
        if len(bounds) > 2:
            raise argparse.ArgumentTypeError(err_msg)

        # The lowerbound cannot be greater than the upperbound
        if lbound >= ubound:
            raise argparse.ArgumentTypeError(f"{user_input}, lowerbound ({lbound}) cannot be greater than or equal to the upperbound ({ubound}) threshold")
        return Threshold(*bounds)


def cli():
    parser = argparse.ArgumentParser(description="segmentation module")
    __add_global_options(parser)
    parser.add_argument("path",
                        metavar='PATH',
                        type=str,
                        nargs=1,
                        help='Input directory to process')  # grayscale image directory
    parser.add_argument("-s", "--sampling", metavar="N", action="store", type=is_counting_number, default=2, help="Downsampling factor. Must be a positive integer.")
    parser.add_argument("--remove-soil", action="store_true", help="Attempt to remove soil")
    parser.add_argument("--threshold", action="store", type=is_valid_threshold, help="Manually selected thresholds for segmentation. Inclusive for both bounds.")
    opts = parser.parse_args()
    return opts


def main() -> int:
    # Runtime arguments
    opts = cli()
    # TODO: remove log
    # configure log
    configure(**vars(opts))

    logging.debug(f"{pformat(vars(opts))}")

    # DO THE THING


def __identify_input_format(path: str) -> str:
    """Given ./data/a.raw or ./data/slice/directory, return raw or slices"""
    dname = os.path.dirname(path)
    bname = os.path.basename(path)
    name, ext = os.path.splitext(bname)
    if ext not in SUPPORTED_OUTPUT_FILETYPES:
        raise ValueError(f"'{ext}' is not a support filetype ({SUPPORTED_OUTPUT_FILETYPES})")


def __determine_output_formats(input_format: str | Sequence[str], output):
    print(f"{input_format=}")
    print(f"{output=}")
    for ofp in output:
        output_dname = os.path.dirname(ofp)
        output_basename = os.path.basename(ofp)
        output_name, output_ext = os.path.splitext(output_basename)
        # if output_ext not in


def segment(path: str,
            output_path: str | Sequence[str] = None,
            lowerbound: int = 1,
            uppebound: int = 255,
            remove_soil: bool = False):
    """Perform segmentation task

    Args:
        path (str): input file (e.g., data.raw)
        output (str | Sequence[str], optional): output filetypes Defaults to None.
        lowerbound (int, optional): lowest value kept, inclusive. Defaults to 1.
        uppebound (int, optional): highest value kept, inclusive. Defaults to 255.
        remove_soil (bool, optional): omit relatively higher/denser objects, typically soil. Defaults to False.
    """
    # Identify input file format
    # .raw or folder (.png, .tif)
    input_format = __identify_input_format(path)

    # Identify output file format(s)
    # If none, use the input file format
    output_format = __determine_output_formats(input_format, output)
    output_path = __

    # If soil,


if __name__ == "__main__":
    raise SystemExit(main())