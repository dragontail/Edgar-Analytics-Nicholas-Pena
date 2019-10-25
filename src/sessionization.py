from sys import argv
from datetime import *
from session import Session
import csv
import heapq

def openFile(file, mode):
	try:
		f = open(file, mode)
	except IOError:
		print("Unable to open file:", file)
		return

	return f

def readInactivity(file):
	inactivityFile = openFile(file, "r")
	inactivityPeriod = "".join(inactivityFile.readline().split())
	inactivityFile.close()

	return int(inactivityPeriod)


'''
	read a log of all the users accessing EDGAR database
	return: a list of tuples describing each of the user sessions
'''
def readLogs(file):
	logFile = openFile(file, "r")

	header = logFile.readline().split(",")
	columns = getColumnPositions(header)

	ip, date, time, cik, accession, extention = 0, 0, 0, 0, 0, 0
	logs = []

	line = logFile.readline()
	while line:
		for fields in csv.reader([line], skipinitialspace = True):
			ip = fields[columns["ip"]]
			date = fields[columns["date"]]
			time = fields[columns["time"]]
			timestamp = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
			cik = fields[columns["cik"]]
			accession = fields[columns["accession"]]
			extention = fields[columns["extention"]]

			session = Session(ip, timestamp, cik, accession, extention)

		logs.append(session)
		line = logFile.readline()

	return logs


def getColumnPositions(header):
	columns = {}
	for i in range(len(header)):
		columns.setdefault(header[i], i)

	return columns

'''
	determines each user session from the given logs and inactivityPeriod

'''
def findSessions(logs, inactivityPeriod, outputFile):
	sessions = {}
	userSessions = []

	output = openFile(outputFile, "w")

	currentTime, previousTime = 0, -1

	for log in logs:
		recentTime = log.timestamp
		startTime = log.timestamp
		numberAccesses = 1

		if log.ip in sessions:
			numberAccesses = sessions[log.ip][2]
			sessions[log.ip] = (sessions[log.ip][0], 
				recentTime, 
				numberAccesses + 1)
		else:
			sessions[log.ip] = (startTime, recentTime, numberAccesses)

		if previousTime != recentTime:
			recentTime = log.timestamp
			sessionsToRemove = checkTimes(sessions, recentTime, inactivityPeriod)

			for session in sessionsToRemove:
				session = (session[1], 
					session[0], session[2], session[3], session[4])

				output.write(",".join(list(session)) + "\n")
				userSessions.append(session)

		previousTime = currentTime
		currentTime = recentTime

	sessionsToRemove = checkTimes(sessions, 
		currentTime + timedelta(seconds = inactivityPeriod + 1), 
		inactivityPeriod)

	for session in sessionsToRemove:
		session = (session[1], session[0], session[2], session[3], session[4])
		output.write(",".join(list(session)) + "\n")
		userSessions.append(session)

	return userSessions


'''
	check our current sessions' last access times against the current timestamp
	if the inactivity period has passed, then session has ended
		sessions: a dictionary that's structured as follows:
		{
			ip : (firstAccessTime, mostRecentAccessTime, numberAccesses)
		}
	return: a list of any sessions that have ended (ip-specific)
			updated version of sessions
'''
def checkTimes(sessions, timestamp, inactivityPeriod):
	sessionsToRemove = []

	for ip in sessions:
		start = sessions[ip][0]
		last = sessions[ip][1]

		if timestamp > last + timedelta(seconds = inactivityPeriod):
			duration = str((last - start).seconds + 1)
			start = datetime.strftime(start, "%Y-%m-%d %H:%M:%S")
			last = datetime.strftime(last, "%Y-%m-%d %H:%M:%S")

			heapq.heappush(sessionsToRemove, 
				(start, ip, last, duration, str(sessions[ip][2])))

	for user in sessionsToRemove:
		sessions.pop(user[1])

	return sessionsToRemove


# def writeOutput(sessions, outputFile):
# 	try:
# 		output = open(outputFile, 'w')
# 	except IOError:
# 		print("There was an error opening the file.")
# 		return

# 	for session in sessions:
# 		line = ",".join(list(session))
# 		output.write(line + "\n")

# 	output.close()


def main():
	if len(argv) != 4:
		print("Usage: ./sessionization.py [logFile inactivityFile outputFile]")
		return

	logFile = argv[1]
	inactivityFile = argv[2]
	outputFile = argv[3].rstrip()

	inactivityPeriod = readInactivity(inactivityFile)
	logs = readLogs(logFile)
	sessions = findSessions(logs, inactivityPeriod, outputFile)
	# writeOutput(sessions, outputFile)

if __name__ == "__main__":
	main()