#encoding:utf-8

import os
import re

# from chars to three octal number
def char23octal(chars):

    result = ''

    for char in chars:

        oct_num = oct(ord(char))[1:]
        if len(oct_num) == 2:
            oct_num = '0' + oct_num
        oct_num = '\\' + oct_num

        result += oct_num

    return result

# from chars to two hex number
def char22hex(chars):

    result = ''

    for char in chars:

        hex_num = hex(ord(char))[2:]
        if len(hex_num) == 1:
            hex_num = '0' + hex_num
        hex_num = '\\x' + hex_num

        result += hex_num

    return result

# html character
def char2htmldec(chars):

    result = ''

    for char in chars:

        dec_num = str(ord(char))
        if len(dec_num) == 1:
            dec_num += '00' + dec_num
        if len(dec_num) == 2:
            dec_num += '0' + dec_num
        dec_num = '&#' + dec_num + ';'

        result += dec_num

    return result


def main():
    chars = raw_input('please enter chars: ')
    chars = chars.strip()
    functions = [char23octal, char22hex, char2htmldec]

    print '----------------------------------------------'
    print '---------please choose translate ways---------'
    print '----------1. from chars to three oct----------'
    print '----------2. from chars to two hex------------'
    print '----------3. from chars to html dec-----------'
    print '----------------------------------------------'

    ways = input('please enter 1, 2, 3: ')
    print functions[ways-1](chars)


if __name__ == '__main__':
    os.system('clear')

    main()
