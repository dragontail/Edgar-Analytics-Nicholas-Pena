from sys import argv
import csv
from datetime import *
from time import mktime
import heapq

'''
	read a file to obtain the inactivity period for sessions
	return: an int representing the min inactivity time
'''
def readInactivity(file):
	try:
		inactivityFile = open(file)
	except IOError:
		print("Unable to open file:", file)
		return

	inactivityPeriod = "".join(inactivityFile.readline().split())

	return int(inactivityPeriod)

'''
	read a log of all the users accessing EDGAR database=
'''
def readLogs(file, inactivityPeriod):
	try:
		logs = open(file)
	except IOError:
		print("Unable to open file:", file)
		return

	header = logs.readline().split(",")

	columns = {}
	sessions = {}
	expirations = {}
	userSessions = []

	for i in range(len(header)):
		columns.setdefault(header[i], i)

	line = logs.readline()

	ip, date, time, cik, accession, extention = 0, 0, 0, 0, 0, 0

	currentTime = 0
	previousTime = -1
	while line:
		for fields in csv.reader([line], skipinitialspace = True):
			try:
				ip = fields[columns["ip"]]
				date = fields[columns["date"]]
				time = fields[columns["time"]]
				timestamp = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
				cik = fields[columns["cik"]]
				accession = fields[columns["accession"]]
				extention = fields[columns["extention"]]
			except TypeError:
				print("There was an error in your data.")
				continue

		currentTime = timestamp
		if ip in expirations:
			expirations[ip] = (expirations[ip][0], timestamp, expirations[ip][2] + 1)
		else:
			expirations[ip] = (timestamp, timestamp, 1)

		if previousTime != currentTime:
			currentTime = timestamp
			sessionsToRemove = checkTimes(expirations, currentTime, inactivityPeriod)

			for user in sessionsToRemove:
				userSessions.append((user[1], user[0], user[2], str(user[3]), str(user[4])))

		line = logs.readline()
		previousTime = currentTime

	sessionsToRemove = checkTimes(expirations, currentTime + timedelta(seconds = inactivityPeriod + 1), inactivityPeriod)

	for user in sessionsToRemove:
		userSessions.append((user[1], user[0], user[2], str(user[3]), str(user[4])))

	return userSessions

'''
	check our current sessions' expirations against the current timestamp
	if the inactivity period has passed, then session has ended
	return: a list of any sessions that have ended (ip-specific)
			updated version of expirations
'''
def checkTimes(expirations, timestamp, inactivityPeriod):
	sessionsToRemove = []

	for ip in expirations:
		start = expirations[ip][0]
		last = expirations[ip][1]

		if timestamp > last + timedelta(seconds = inactivityPeriod):
			difference = (last - start).seconds + 1
			start = datetime.strftime(start, "%d-%b-%Y %H:%M:%S")
			last = datetime.strftime(last, "%d-%b-%Y %H:%M:%S")

			heapq.heappush(sessionsToRemove, (start, ip, last, difference, expirations[ip][2]))
			# sessionsToRemove.append((ip, start, last, difference, expirations[ip][2]))

	for user in sessionsToRemove:
		expirations.pop(user[1])

	return sessionsToRemove

'''

'''
def writeOutput(logs, outputFile):
	try:
		output = open(outputFile, 'w')
	except IOError:
		print("There was an error opening the file.")
		return

	# loop through the results, in increasing order of department #
	for user in logs:
		line = ",".join(list(user))
		output.write(line + "\n")

	output.close()

def main():
	if len(argv) != 4:
		print("Usage: ./sessionization.py [logFile inactivityFile outputFile]")
		return

	logFile = argv[1]
	inactivityFile = argv[2]
	outputFile = argv[3].rstrip()

	inactivityPeriod = readInactivity(inactivityFile)

	logs = readLogs(logFile, inactivityPeriod)
	
	writeOutput(logs, outputFile)

if __name__ == "__main__":
	main()