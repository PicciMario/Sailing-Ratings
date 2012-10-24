import csv, getopt, sys, os

def usage():
	print("")
	print("Sailing rating calculator.")
	print("by PicciMario <mario.piccinelli@gmail.com>")
	print("")
	print("Options:")
	print("-h          this help")
	print("-f file     file containing the rating table")
	print("-r value    reference rating (default: 0.75)")
	print("")
	print("Race length in real time for the reference boat")
	print("(if more than one are present they are added):")
	print("-s value    seconds")
	print("-m value    minutes")
	print("-t value    hours")
	print("")
	print("The rating table must be a CSV file in the form:")
	print("   boat class, rating coefficient")
	print("")

# read command line options
ratingsFile = None
seconds = 0
refrating = 0.8098

try:
	opts, args = getopt.getopt(sys.argv[1:], "hf:r:s:m:t:")
except getopt.GetoptError:
	usage()
	sys.exit(0)

for o,a in opts:
	if o == "-h":
		usage()
		sys.exit(0)
	elif o == "-f":
		ratingsFile = a
	elif o == "-r":
		try:
			refrating = float(a)
		except:
			usage()
			print("ERROR: Reference rating must be numeric.\n")
			sys.exit(1)
	elif o == "-s":
		try:
			newSeconds = float(a)
			seconds = seconds + newSeconds
		except:
			usage()
			print("ERROR: Seconds must be numeric integer.\n")
			sys.exit(1)
	elif o == "-m":
		try:
			newMinutes = float(a)
			seconds = seconds + (newMinutes * 60)
		except:
			usage()
			print("ERROR: Minutes must be numeric integer.\n")
			sys.exit(1)
	elif o == "-t":
		try:
			newHours = float(a)
			seconds = seconds + (newHours * 3600)
		except:
			usage()
			print("ERROR: Hours must be numeric integer.\n")
			sys.exit(1)
	
# race length defaults to 1 h
if (seconds == 0):
	seconds = 3600

# check existence of ratings file
if (ratingsFile == None):
	usage()
	print("ERROR: You must provide a valid ratings file from command line.\n")
	sys.exit(1)

if (os.path.isfile(ratingsFile) == False):
	usage()
	print("ERROR: The ratings file you provided does not exist.\n")
	sys.exit(1)

# import ratings table from csv (boat type, rating)
ratings = csv.reader(open(ratingsFile, 'rb'), delimiter=',', quotechar="|")

# function to convert seconds number into formatted string
def printTime(sec):

	hour = 0 
	min = 0
	
	sign = "+"
	if (sec < 0): sign = "-"
	
	try:
		sec = abs(int(sec))
	except:
		print sec
	
	if (sec >= 60):
		min = int(sec/60)
		sec = sec - (min*60)
	
	if (min >= 60):
		hour = int(min/60)
		min = min - (hour * 60)
	
	return "%s%i:%02i:%02i"%(sign, hour, min, sec)

# list to store results (boat type and seconds in comp. time)
results = []

# calculating comp. time for each boat
try:
	for rating in ratings:
		boat = rating[0]
		value = float(rating[1])
		results.append([boat, int(float(seconds) * float(refrating) / float(value)) - seconds, value])
except:
	usage()
	print("Error while reading csv file.")
	print('file %s, line %d: %s' % (ratingsFile, ratings.line_num, sys.exc_info()[1]))
	print("")
	sys.exit(1)

# print header
print("")
print("Sailing rating calculator.")
print("by PicciMario <mario.piccinelli@gmail.com>")
print("")
print("Over a %s long race."%(printTime(seconds)))
print("(in real time for reference boat with rating %s)"%(refrating))
print("Ratings file: %s"%ratingsFile)
print("")

# calculate max length of boat type name
# (for formatting output)
maxLen = 0
for result in results:
	newLen = len(result[0])
	if (newLen > maxLen):
		maxLen = newLen

# print results
for result in sorted(results, key=lambda result: result[1]):
	
	# format time (---- for reference boat)
	if (result[1] == 0):
		time = "--------"
	else:
		time = printTime(result[1])
	
	# add arrow indicator for reference boat
	indicator = ""
	if (result[2] == refrating):
		indicator = "<---- ref. boat" 
	
	# print a result
	print("%s%s    (%s * %.4f = %s)  %s")%(
		result[0].ljust(maxLen + 2), 
		time, 
		printTime(seconds + result[1]), 
		result[2], 
		printTime((seconds + result[1])*result[2]),
		indicator
	)

print("")
