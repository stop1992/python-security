#encoding:utf-8

import os
import re

class Jinwen(object):

    def __init__(self):
        pass

    def handle_file(self, file_name):

        header = True
        dash_sign = re.compile('^---')
        before_sort = []
        data = ''
        energy = []
        # is_energy = re.compile('^mfe')
        is_energy = re.compile('mfe: (.*?) kcal/mol')
        is_target = re.compile('^target:')
        is_mirna = re.compile('^miRNA :')

        for line in open(file_name):

            if not line.strip():
                # print 'empty line...'
                continue

            is_dash = dash_sign.search(line)

            # first dash line
            if is_dash and header:
                header = False
                data = ''
                continue

            if is_dash:
                before_sort.append(data)
                data = ''
            else:
                if is_target.search(line):
                    data += line.split('|')[2]
                if is_mirna.search(line):
                    data += line.split(':')[1].strip()
                # data += line
                energy_num= is_energy.search(line)
                if energy_num:
                    energy_num = energy_num.groups()[0]
                    data += '\n' + line
                    energy.append(float(energy_num))

        # print len(before_sort)
        # for i in before_sort:
            # print i
            # print '#' * 60
        energy.sort()
        energy_50 = energy[:50]

        sorted_file_name = file_name.split('.')[0] + '_50.txt'
        fp = open(sorted_file_name, 'w')
        i = 1

        for tmp_energy in energy_50:
            for out in before_sort:
                mfe = is_energy.search(out)
                if mfe:
                    mfe = mfe.groups()[0]
                    # print mfe
                    if float(mfe) == tmp_energy:
                        fp.write(str(i)+'\n')
                        fp.write(out)
                        # fp.write(str(out.split('\n')[:1]))
                        i += 1
                        if i > 50:
                            break
                else:
                    'no result'
                    raw_input('wait....')
            if i > 50:
                break
        fp.close()

        # for i in open(sorted_file_name, 'r'):
            # print i


    def get_all_files(self):

        for file_name in os.listdir('.'):
            if '.txt' in file_name and '_50' not in file_name:
                print 'handling', file_name
                self.handle_file(file_name)


def main():

    jinwen = Jinwen()
    jinwen.get_all_files()


if __name__ == '__main__':

    main()
