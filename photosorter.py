
#!/usr/bin/python

import os
import sys
import time
import os.path
import pathlib
import exifread
import argparse
import PIL.Image
import dateparser
from PIL import Image
from shutil import copyfile


def move_file_by_tag(path, filename, dest_folder):

    source_path = os.path.join(path, filename)

    # Try to read with exifread
    f = open(source_path, 'rb')
    tags = exifread.process_file(f)


    if (len(tags) == 0):
        # If it does not work, let's fall back to file creation date
        f.close()

        file_creation = time.ctime(os.path.getctime(source_path)) # windows specific! 
        # print("File created: %s" % file_creation)
        tags = {"EXIF DateTimeOriginal" : file_creation}

    for key in tags.keys():
        if key == "EXIF DateTimeOriginal":

            # Get date from exif data in the file
            exif_date = str(tags[key])
            exif_date = exif_date[ : exif_date.find(' ') ]
            exif_date = exif_date.replace(':', '-')
            img_date = dateparser.parse(exif_date)

            # Construct new path
            new_path = os.path.join(dest_folder, str(img_date.year), str(img_date.strftime("%B")))

            # Create folder if does not exist
            pathlib.Path(new_path).mkdir(parents=True, exist_ok=True)

            # Move
            new_path = os.path.join(new_path, filename)
            copyfile(source_path, new_path)

            print("Moved: " + source_path + " -> " + new_path)

    f.close()
    return tags

def move_files_by_tag(source_folder, dest_folder):
    
    for root, subdirs, files in os.walk(source_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            print(file_path)
            move_file_by_tag(root, filename, dest_folder)

def print_help():
    print("Welcome to photo sorter")
    print("Usage: photosorter.py -i <sourcefolder> -o <destfolder>")


if __name__ == "__main__":
    print("*_*_*_* Welcome to photosorter *_*_*_*\n")
    
    if (len(sys.argv) < 5):
        print("Too few arguments. Specify input and output folders.")
        print_help()
        sys.exit(2)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = vars(parser.parse_args())

    inputfolder = args["input"]
    outputfolder = args["output"]
    
    inputfolder = os.path.join(inputfolder, '')
    outputfolder = os.path.join(outputfolder, '')

    print('Input folder is ' + inputfolder)
    print('Output folder is ' + outputfolder)

    if os.path.exists(inputfolder) == False:
        print("The input folder does not exist")
        sys.exit()

    files = next(os.walk(inputfolder))[2]
    file_count = len(files)
    if (file_count  == 0):
        print("There are no files in the source folder")

    print("Performing operation on " + str(file_count) + " files")
    move_files_by_tag(inputfolder, outputfolder)