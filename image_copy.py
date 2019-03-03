import argparse
import os
import exifread
import datetime
import pyexifinfo
import filecmp
import shutil

parser = argparse.ArgumentParser(description='Copy Image Files into nob13 Format')
parser.add_argument('--input', dest='input', required=True, help='Input Directory')
parser.add_argument('--output', dest='output', required=True, help='Output Directory')
parser.add_argument('--cache', dest='cache_file', help='Touched file cache')
parser.add_argument('-s', help='simulate', action='store_true')

args = parser.parse_args()
print("Input  =   ", args.input)
print("Output =   ", args.output)
print("Simulate = ", args.s)
print("Cache file=", args.cache_file)

touched_files = set()
if args.cache_file is not None:
    try:
        with open(args.cache_file, "r") as f:
            touched_files = set(f.read().splitlines())
    except:
        print("Could not read cache file")

if not os.path.isdir(args.output):
    print("Output is not a directory")
    exit(1)

cache_writer = None

if args.cache_file is not None:
    cache_writer = open(args.cache_file, "a+")

def add_to_cache(file):
    if cache_writer is not None:
        cache_writer.write(file)
        cache_writer.write("\n")

def get_exif_creation_date(filename: str) -> datetime.date:
    with open(file, "rb") as f:
        tags = exifread.process_file(f, details=False)
        cand = tags.get("EXIF DateTimeOriginal", None)
        if cand is not None:
            return datetime.datetime.strptime(cand.values, "%Y:%m:%d %H:%M:%S").date()
        return None


def get_exif_tool_create_date(filename: str) -> datetime.date:
    jsoninfo = pyexifinfo.get_json(filename)
    cand = jsoninfo[0].get("QuickTime:MediaCreateDate", None)
    if cand is not None:
        return datetime.datetime.strptime(cand, "%Y:%m:%d %H:%M:%S").date()
    # print("JSON ", jsoninfo)
    return jsoninfo.get("Media Create Date", None)


def get_file_date(filename: str) -> datetime.date:
    exif = get_exif_creation_date(filename)
    if exif is not None:
        return exif
    exif2 = get_exif_tool_create_date(filename)
    if exif2 is not None:
        return exif2
    print("Skipping to modification time for", filename)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filename)).time()
    return mtime

def get_destination_dir(filename, file_date: datetime.date):
    return os.path.join(args.output, "{:04d}".format(file_date.year), "{:02d}".format(file_date.month))

for root, dirs, files in os.walk(args.input):
    for name in files:
        file = os.path.join(root, name)
        if file in touched_files:
            print(file, "Already in touched files")
            continue

        file_date = get_file_date(file)
        destination_dir = get_destination_dir(file, file_date)
        destination_file = os.path.join(destination_dir, os.path.basename(file))
        # print("File ", file, " Date ", file_date, " ---> ", destination_file)


        if os.path.exists(destination_file):
            if filecmp.cmp(file, destination_file):
                print("File ", file, " already exists, same content")
                add_to_cache(file)
            else:
                print("File differs!!!!")
        else:
            print("Copying", file, " --> ", destination_file)
            if not args.s:
                if not os.path.isdir(destination_dir):
                    os.makedirs(destination_dir)
                shutil.copy2(file, destination_file)
                add_to_cache(file)

if cache_writer is not None:
    cache_writer.close()