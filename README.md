# Edgar-Analytics
Coding Challenge #1

Author: Nicholas Pena (dragontail)

Approach:

1) Read the inactivity_period.txt file in order to get the inactivity period
2) Read through log.csv to obtain logs
	- Read the first row in order to determine the order of columns for the proceeding rows
	- Start reading rows
		- Get the corresponding fields, create a timestamp with the date + time fields
		- If the timestamp has changed from the previous time, check sessions to remove inactive ones that have expired
		- Add the sessions to remove to a list called logs
	- At the end of the file, all of the current sessions to logs as they have ended
3) With logs, write logs to file
