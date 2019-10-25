# Edgar-Analytics
Coding Challenge #1

Author: Nicholas Pena (dragontail)

## Usage

In the main directory, run the shell script `run.sh`. This will run `/src/sessionization.py`, which reads the log file located at `/input/log.csv` in order to determine the user sessions. The Python script will then write the output of all the sessions to `/output/sessionization.txt`.

A user's session begins when they first access a file on the EDGAR database. There will be a number, defined by `/input/inactivity_period.txt` where, after that many seconds, a user's session will end if there has not been any activity in that time.

## Approach

1) Read the inactivity_period.txt file in order to get the inactivity period
2) Read through log.csv to obtain logs
	- Read the first row in order to determine the order of columns for the proceeding rows
	- Start reading rows
		- Get the corresponding fields, create Session objects, return a list of sessions
3) Extract the sessions from the logs
	- Go through each line in the logs
		- Create a timestamp with the date + time fields
		- Keep track of the current ongoing sessions with a dictionary mapping ip addresses to tuples with the following:
			- `(timeOfFirstAccess, timeOfMostRecentAccess, numberOfAccesses)`
		- If the timestamp has changed from the previous time, check current sessions to remove inactive ones that have expired
		- Add the sessions to remove to a list called userSessions
	- At the end of the file, add all of the current sessions to userSessions as they have ended
3) With userSessions, write the sessions to outputFile
