import passwords

import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
	
# Contact to client
FLOW = OAuth2WebServerFlow(
	client_id=passwords.client_id,
	client_secret=passwords.client_secret,
	scope='https://www.googleapis.com/auth/calendar',
	user_agent='unify/1')

# create storage if offline
storage = Storage('calendar.dat')
credentials = storage.get()	
if credentials is None or credentials.invalid == True:
	credentials = run(FLOW, storage)

# authorize
http = httplib2.Http()
http = credentials.authorize(http)
service = build(serviceName='calendar', version='v3', http=http,
	   developerKey=passwords.developerKey)
			   

def show(parameter):
	global service
	event = service.events().get(calendarId='primary', eventId=parameter).execute()
	print event['summary']
	
	
def add():
	global service
	
	choice = raw_input("individual or entire calender: (i/c)")
	
	if choice == 'i':
		parameter = [raw_input("choose parameter: ")]
		return parameter
	
	
	elif choice == 'c':
		
		# display calender list
		page_token = None
		count = 0
		calendars = []
		while True:
			calendar_list = service.calendarList().list(pageToken=page_token).execute()
			if calendar_list['items']:
				for calendar_list_entry in calendar_list['items']:
					calendars.append(calendar_list_entry['id'])
					print str(count)+": "+calendar_list_entry['summary']
					count = count+1
					
			page_token = calendar_list.get('nextPageToken')
			if not page_token:
				break
		
		calendarno = int(raw_input("choose calendar: "))
		calendarID = calendars[calendarno]
		print calendarID
		
		page_token = None
		items = []
		while True:
			events = service.events().list(calendarId=calendarID, pageToken=page_token).execute()
			if events['items']:
				for event in events['items']:
					items.append(event['id'])
					if event.has_key("summary"):
						print event['summary']
					
			page_token = events.get('nextPageToken')
			if not page_token:
				break
		
		return items
		
	
	else:
		print "wrong answer"
		return "False"
	
	

