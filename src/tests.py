from unittest import TestCase, main
from sessionization import readInactivity, readLogs, findSessions
from session import Session
from datetime import *

class TestLogFunctions(TestCase):

	def testReadInactivity(self):
		inactivityPeriod = readInactivity("./test_files/inactivity_period.txt")
		return self.assertEqual(inactivityPeriod, 5)

	def testReadLogs(self):
		logs = readLogs("./test_files/logs.csv")[0]
		session = Session("101.81.133.jja", 
			datetime(2017, 6, 30, 0, 0), 
			"1608552.0", 
			"0001047469-17-004337", 
			"-index.htm")
		
		ip = logs.ip == session.ip
		timestamp = logs.timestamp == session.timestamp
		cik = logs.cik == session.cik
		accession = logs.accession == session.accession
		extention = logs.extention == session.extention

		return self.assertTrue(ip 
			and timestamp and cik and accession and extention)
				
	def testFindSessions(self):
		logs = readLogs("./test_files/logs.csv")
		inactivityPeriod = readInactivity("./test_files/inactivity_period.txt")

		sessions = findSessions(logs, inactivityPeriod)
		return self.assertEqual(sessions, [(
				"101.81.133.jja", 
				"2017-06-30 00:00:00",
				"2017-06-30 00:00:00",
				"1",
				"1")])


if __name__ == '__main__':
	main()