from sys import argv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--foo', help='foo help', type=str)
args = parser.parse_args()

filename = argv[0]

print "The name of your file is %s" % filename
# Print the contents of the parameters passed to "--foo"
print "The parameter issued to foo is {}".format(args.foo)
