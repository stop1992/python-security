#!/usr/bin/env python
# encoding: utf-8

import os

import forgi.graph.bulge_graph as fgb


def count_stems_loops():

    while True:

        handle_dir = raw_input('please enter the abosolute directory that need to handle \n>')
        if handle_dir == 'exit':
            break
        if handle_dir == '.' or handle_dir == '':
            continue

        bg = fgb.BulgeGraph()

        if os.path.exists(handle_dir):
            print 'directory exists, so start counting...'
            for dirpath, dirnames, filenames in os.walk(handle_dir):

                result_fp = ''

                if len(filenames) != 0:
                    # store result in result.txt
                    result_fp = open(dirpath + os.sep + 'result.txt', 'w')
                    result_fp.write('filename stems loops\n')
                else:
                    continue

                for filename in filenames:

                    if filename == 'result.txt':
                        continue

                    all_data = open(dirpath + os.sep + filename, 'r').readlines()
                    try:
                        # handle third line data
                        data = all_data[2].split()[0].strip()
                        bg.from_dotbracket(data)

                        # get the number of stems, interior loops \
                        # hairpin loop, multiple loop
                        stems = len(list(bg.stem_iterator()))
                        iloops = len(list(bg.iloop_iterator()))
                        hloops = len(list(bg.hloop_iterator()))
                        mloops = len(list(bg.mloop_iterator()))

                        # get all loops
                        loops = iloops + hloops + mloops
                        result_fp.write(filename + ' ' + str(stems) + ' ' + str(loops) + '\n')

                        print filename, stems, loops
                    except Exception,e:
                        print '[*] ', filename, e
                        raw_input('occur a error, so stop...')

                result_fp.close()

def main():
    count_stems_loops()


if __name__ == '__main__':
    os.system('clear')

    main()
