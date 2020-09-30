# photosorter
Python utility to sort photos according to when they were taken.

It will recursively go through a folder, look at the Exif data of the photos and sort them into folders
according to year and month.


How to use
-----
1. Download the files using the Code / Download Zip folder function on GitHub (upper right corner)
2. Install the latest python here: https://www.python.org/downloads/
3. Extract the contents of the zip to a folder
4. Open the Python terminal and navigate to the folder where the photosorter.py file is
5. type pip install -r requirements.txt. It should install a bunch of packages successfully
6. Type python photosorter.py -i <inputfolder> -o <outputfolder>