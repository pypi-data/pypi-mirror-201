import subprocess
from pathlib import Path
from typing import List


def write(file: Path, tags: List[str]):
    """Write image metadata tags to an image file using ExifTool. Existing file
    will be overwritten.

    :param file: Path to image file.
    :param tags: List of ExifTool tag assignment strings.
    """
    # Setup metadata copy
    cmd = ['exiftool', '-q', '-overwrite_original', str(file)]

    # Map all the other tags
    cmd.extend(tags)

    # Run exiftool
    subprocess.run(cmd, check=True)


def copy_all(src: Path, dest: Path, extra_tags: List[str] = None,
             overwrite=True):
    """Copy tag metadata from source image to destination image.

    :param src: Path to image file containing source metadata.
    :param dest: Path to destination image file.
    :param extra_tags: If provided, write additional tags to :code:`dest`.
    :param overwrite: If :code:`True`, overwrite the destination image file.
    """
    # Setup metadata copy
    cmd = ['exiftool', '-q']

    # Overwrite original destination file
    if overwrite:
        cmd.append('-overwrite_original')

    # Skip tags that don't make sense in JPGs
    if dest.suffix not in ['.tif', '.tiff']:
        cmd.extend(['-XMP-tiff:all=', '-ExifIFD:BitsPerSample=',
                    '-IFD0:BitsPerSample='])

    # Original tags from original files
    cmd.extend(['-TagsFromFile', str(src)])

    # Map all the other tags
    cmd.append('-all:all')

    # Project specific tags
    if extra_tags is not None:
        cmd.extend(extra_tags)

    # Add target
    cmd.append(str(dest))

    # Run exiftool
    subprocess.run(cmd, check=True)
