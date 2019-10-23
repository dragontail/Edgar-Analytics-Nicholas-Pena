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
				userSessions.append(user)

		line = logs.readline()
		previousTime = currentTime

	sessionsToRemove = checkTimes(expirations, currentTime + timedelta(seconds = inactivityPeriod), inactivityPeriod)
	for user in sessionsToRemove:
		userSessions.append(user)

	return userSessions

'''
	check our current sessions against the current time
	if the inactivity period has passed, then session has ended
	return: a list of any sessions that have ended (ip-specific)
			updated version of times
'''
def checkTimes(expirations, timestamp, inactivityPeriod):
	sessionsToRemove = []

	for ip in expirations:
		start = expirations[ip][0]
		last = expirations[ip][1]

		if timestamp >= last + timedelta(seconds = inactivityPeriod):
			difference = (last - start).seconds + 1
			start = datetime.strftime(start, "%d-%b-%Y %H:%M:%S")
			last = datetime.strftime(last, "%d-%b-%Y %H:%M:%S")
			sessionsToRemove.append((ip, start, last, difference, expirations[ip][2]))

	for user in sessionsToRemove:
		expirations.pop(user[0])

	return sessionsToRemove


def main():
	if len(argv) != 4:
		print("Usage: ./sessionization.py [logFile inactivityFile outputFile]")
		return

	logFile = argv[1]
	inactivityFile = argv[2]
	outputFile = argv[3].rstrip()

	inactivityPeriod = readInactivity(inactivityFile)

	logs = readLogs(logFile, inactivityPeriod)
	
	for log in logs:
		print "User: ", log

if __name__ == "__main__":
	main()