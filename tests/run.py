#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import traceback
import nose
from optparse import OptionParser

def add_path():
    global project_root
    file_path = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath("%s/../" % file_path)
    sys.path.insert(0, project_root)
    return project_root

project_root = add_path()

os.environ["MONGODB_DB"] = "bands_test"
os.environ["SECRET_KEY"] = "test key"

def import_folder(folder_name, base_path = None):
    full_path = os.path.join(base_path, folder_name)
    folder = os.path.abspath(full_path)
    sys.path.insert(0, folder)


import_folder(folder_name='bands', base_path=project_root)

def run_tests():
    result = None
    try:
        parser = OptionParser()
        parser.add_option("-f", "--file", dest="filename", help="Nome dos arquivos para rodar", default=None)
        (parsed, args) = parser.parse_args()
        params = ["nosetests", "--with-xcoverage", "--with-xunit", "-w", "tests", "--cover-package", "bands.*", "--match", "(?:^|[\b_\./-])[Tt]est"]
        if parsed.filename:
            params.insert(0, "--tests=")
            params.insert(0, parsed.filename)
        result = nose.run(argv=params)

    except Exception as e:
        print ""
        print e
        print ""

        traceback.print_last()
    finally:
        if result:
            exit(0)
        exit(1)

if __name__ == '__main__':
    run_tests()