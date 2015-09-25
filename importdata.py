#!/usr/bin/env python
# encoding: utf-8

def importdat():
    directorys = ['db_01', 'db_02', 'db_03', 'db_05', 'db_06', 'db_07', 'db_08', 'db_09', 'db_10']
    for direc in directorys:
        files = os.listdir(direc)
        for file_name in files:
            data = open(direc + '/' + files)
