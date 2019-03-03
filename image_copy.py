import argparse
import os
import exifread
import datetime

parser = argparse.ArgumentParser(description='Copy Image Files into nob13 Format')
parser.add_argument('--input', dest='input', required=True, help='Input Directory')
parser.add_argument('--output', dest='output', required=True, help='Output Directory')
parser.add_argument('-s', action='store_true')

args = parser.parse_args()
print("Input  =   ", args.input)
print("Output =   ", args.output)
print("Simulate = ", args.s)

def get_file_date(filename: str) -> datetime.date :
    with open(file, "rb") as f:
        tags = exifread.process_file(f, details=False)
        creation = tags.get("EXIF DateTimeOriginal", None)
        if creation == None:
            print("Could not fetch time")
        else:
            print("Creation time", creation)
        return creation


for root, dirs, files in os.walk(args.input):
    for name in files:
        file = os.path.join(root, name)
        print("Processing file ", file)
        time = get_file_date(file)

