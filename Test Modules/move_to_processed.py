import os
import shutil
import argparse


def move_to_processed(file_path):
    destination = "C:/Users/craig/Google Drive/CaptainsLog/Processed"
    shutil.move(file_path, destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help="none - you're on your own")
    args = parser.parse_args()
    move_to_processed(args.path)