#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
if not os.getenv('PYTHONIOENCODING', None): # PyInstaller workaround
    os.environ['PYTHONIOENCODING'] = 'utf_8'

import urllib.request #Python 3
import logging
import zipfile
import sys

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

url = "http://unicode.org/udhr/assemblies/udhr_xml.zip"
FILENAME = 'udhr_xml.zip'

scripts_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(scripts_path)
os.chdir("..")
repo = os.getcwd()
print (repo)
os.chdir(scripts_path)


# Specifying the locale of the source
import locale
locale.setlocale(locale.LC_NUMERIC, 'English') #'English_United States.1252'


def download():
    path="archive"
    archive_path = os.path.join(repo, path)
    zip_path = os.path.join(archive_path, FILENAME)

    print ("{}\t{}\t{}\t".format(scripts_path, archive_path, zip_path))

    logger.info('Retrieving source database: {} ...'.format(url))
    #urllib.request.urlretrieve fp)
    f=urllib.request.urlopen(url)
    output=f.read() #.decode('cp1252')

    os.chdir(repo)
    if not os.path.exists(path):
        os.makedirs(path)
   
    os.chdir(archive_path)

    with open(FILENAME, "wb") as temp:
        temp.write(output)

    os.chdir(scripts_path)
    logger.info('Source database downloaded to: {}'.format(zip_path))

    return zip_path



def extract(fn):
    os.chdir(repo)
    path='xml'
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    extract_path = os.path.join(repo, path)
    os.chdir(extract_path)

    logger.info('Extracting UDHR to {}'.format(extract_path))
    z = zipfile.ZipFile(fn)
    z.extractall()
    z.close()

if __name__ == '__main__':
    zip_path=download()
    extract(zip_path)
    

