# Read Comment Crew daily report and parse out URLs
from sys import argv
from datetime import datetime

# Define a method to replace multiple strings in the matching text 
def replace_things(text, dic):
	for original, altered in dic.iteritems():
		text = text.replace(original,altered)
	return text

# Dictionary of strings to replace
rep = {'hxxp':'http', '[.]':'.'}
# Take the first arg from command line as the file to parse
daily_report = argv[1]
# Open the file
ccreport = open(daily_report, 'rb') 
# Create outfile (append to existing results file, "results.txt"
cctotal = open('results.txt', 'a')
# Print the date + time when the script is run and write to the results file
report_time = str(datetime.now())
cctotal.write(report_time)
# Iterate over the file, looking for lines that start with URL
# For lines that start with URL, replace the text as defined
# by the dict named rep
for line in ccreport:
	if line.startswith('URL'):
		replaced = replace_things(line, rep)
# This removes the "URL: " and trailing colon + newline		
		replaced = replaced[5:-4]
		print replaced
# Write the list to resutls.txt
		cctotal.write("\n"+replaced)
# Create a newline between each days' results
cctotal.write("\n\n")
# Close the file objects
daily_report.close()
cctotal.close()
