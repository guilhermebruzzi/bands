#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import nose

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
        params = ["nosetests", "--with-xcoverage", "--with-xunit", "-w", "tests", "--cover-package", "bands", "--match", "(?:^|[\b_\./-])[Tt]est"]
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