"""
Modify sequence file(s) in place.
"""

import argparse
import contextlib
import logging
import os
import os.path
import shutil
import tempfile

from . import convert

@contextlib.contextmanager
def atomic_write(path):
    """
    Open a file for atomic writing.

    Generates a temp file, renames to dest
    """
    base_dir = os.path.dirname(path)
    tf = tempfile.NamedTemporaryFile(dir=base_dir, delete=False)
    try:
        with tf:
            yield tf
        # Move
        os.rename(tf.name, path)
    except:
        os.remove(tf.name)
        raise

def build_parser(parser):
    """
    """
    convert.add_options(parser)

    parser.add_argument(
        'input_files', metavar="sequence_file", nargs='+',
        type=argparse.FileType('r+'),
        help="Sequence file(s) to mogrify")

    return parser


def action(arguments):
    """
    Run mogrify.  Most of the action is in convert, this just creates a temp
    file for the output.
    """
    for input_file in arguments.input_files:
        logging.info(input_file)
        bn = os.path.basename(input_file.name)
        # Generate a temporary file
        with tempfile.NamedTemporaryFile(prefix='smagick', suffix=bn,
                delete=False) as tf:
            convert.transform_file(input_file, tf, arguments)
        # Overwrite the original file
        shutil.move(tf.name, input_file.name)
