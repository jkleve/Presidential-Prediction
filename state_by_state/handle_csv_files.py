import os
import sys

TEST = 0

def move_zips(year):
    source = "tmp/"
    dest = "zips/"
    ending = "_" + str(year) + ".zip"

    files = os.listdir(source)

    for f in files:
        beginning = f.split('.')[0]
        if TEST:
            print("mv " + source + f + " " + dest + beginning + ending)
        else:
            os.system("mv " + source + f + " " + dest + beginning + ending)

def unzip_files(year):
    source = "tmp/"
    dest_dir = "csvs_" + str(year) + "/"

    files = os.listdir(source)

    s = ""
    for f in files:
        if TEST:
            print("unzip " + source + f + " -d " + dest_dir)
        else:
            os.system("unzip " + source + f + " -d " + dest_dir)

if __name__ == "__main__":
    year = 2008
    unzip_files(year)
    move_zips(year)
