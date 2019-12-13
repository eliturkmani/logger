import sys
import time
import os
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re

class LogMonitor:
	
	def __init__(self):
		pass

	#check if date change while inside while loop
		#if date changed log file name also changed
	def checkDateChanged(self,startedAt, today):
		if(startedAt != today):
			return True
		else:
			return False
			
		
	def tailLog(self, file):
		#put cursor at end of file and repeatedly try to read new lines.
		file.seek(0, 2) ## A whence value of 0 measures from the beginning of the file, 1 uses the #current file position, and 2 uses the end of the file
		
		startedAt = datetime.datetime.today().date()
		dateChanged = False
		counter = 0
		
		while True:
			time.sleep(1)
			counter= counter+1
			line = file.read()
			
			dateChanged = self.checkDateChanged(startedAt,datetime.datetime.today().date());
	
			if(dateChanged): #log file name probably change
				break

			if not line:
				time.sleep(0.1)
			else:
				findError = line.find(' ERROR ')
				
				if(findError > -1):
					self.formatText(line)
					
					
		main() #restart the program to get the new logfile name
		
	def formatText(self,error):

		regex = '([0-9]:[0-9]{2}:[0-9]{2} [AaPp][Mm] \[[#0-9])'
		startOfLine = re.findall(regex, error)
		findIndex = 0;
		matchesIndexes = []
		for x in startOfLine:
			findLineBreak = error.find(x,findIndex)
			findIndex = findLineBreak+2
			matchesIndexes.append(findLineBreak)
			
		findErrorIndex = error.find(' ERROR ')
		errorFormatted = ''
		bolded = '0'

		for x in range(len(matchesIndexes)):
			if(x < len(matchesIndexes) -1):
				stringyy = error[matchesIndexes[x]:matchesIndexes[x+1]]
				if(matchesIndexes[x+1] > findErrorIndex and bolded != '2' and findErrorIndex > -1):
					bolded = '1'
			else:
				stringyy = error[matchesIndexes[x]:]
			
			style = "margin:0"
			if(bolded == '1'):
				bolded = '2'
				style = "margin:0; font-weight: bold; color: red;"
			errorFormatted += '<p style="'+style+'">' +stringyy + '</p>'
	
		self.emailError(errorFormatted)
		
	def emailError(self, error):
		message = Mail(
			from_email='iparadoxloger@noone.ca',
			to_emails='eli.turkmani@soth.ca',
			subject='iparadox error detected',
			html_content=error
			)
		try:
			sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
			response = sg.send(message)
			#print(response.status_code)
			#print(response.body)
			#print(response.headers)
		except Exception as e:
			print(e.message)

def getFileName():
	date = datetime.datetime.now()
	year = str(date.year)
	month = '{:02d}'.format(date.month)
	
	day = '{:02d}'.format(date.day)
	dayOfWeek = date.strftime("%A")
	
	return year + '.' + month + '/' + day + '.' + dayOfWeek + '.LOG'
	
	
def main():
	print('IPARADOX LOG MONITORING STARTED..')
	print('LISTENING FOR ERRORS...')
	if(len(sys.argv) < 2):
		script_dir = os.path.dirname(os.path.abspath(__file__)) #<-- absolute dir the script is in
		fileName = getFileName()
		filePath = os.path.join(script_dir, fileName)
	else:
		filePath = sys.argv[1]
		
	try:
		file = open(filePath,'r')
		logMonitor = LogMonitor()
		logMonitor.tailLog(file)
		#logMonitor.formatText('')
		#testString()
	except IOError:
		print('file not accessible')
		time.sleep(10)
		main()

if __name__ == '__main__':
	main()
	#print("This only executes when %s is executed rather than imported" % __file__)
	
else:
    print ('I am being imported from another module')
		
		
		

		
''' def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11)) '''
