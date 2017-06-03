import os
import argparse

def convert_to_flac(filename):
    #adding quotes around the filename so it is sent to the command line with quotes around it
    filename = "\"" + filename + "\""
    os.system("start /wait cmd /c ffmpeg -i {} audio.flac".format(filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='Add file path')
    args = parser.parse_args()
    convert_to_flac(args.path)
