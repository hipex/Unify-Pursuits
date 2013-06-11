import googleInit
import time

def showHeader(parameter):
	global googleInit

	calendar_list_entry = googleInit.service.calendarList().get(calendarId=parameter).execute()
	print "gcal calendar: "+ calendar_list_entry['summary']
	

def add(parentParameter):
	global googleInit
	# display calender list
	page_token = None
	count = 0
	calendars = []
	while True:
		calendar_list = googleInit.service.calendarList().list(pageToken=page_token).execute()
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
	
	return [calendarID]

def remove(parameter):
	global googleInit
	
	googleCalendarId = parameter
	googleInit.service.calendars().delete(parameter).execute()
	return True

def update(mdb, parameter, itemID):
	global googleInit
	
	
	page_token = None
	while True:
		calendar_list = googleInit.service.calendarList().list(pageToken=page_token).execute()
		if calendar_list['items']:
			for calendar_list_entry in calendar_list['items']:
				if calendar_list_entry['id'] == parameter:
					return 'none'
		page_token = calendar_list.get('nextPageToken')
		if not page_token:
			break
	
	# calendar is not existend online, remove from database
	
	return itemID

def getTitle(parameter):
	global googleInit

	calendar_list_entry = googleInit.service.calendarList().get(calendarId=parameter).execute()
	return calendar_list_entry['summary']

def getVirtualItems(parentParameter, parentItemID, parentServiceID, parentServiceTitle, childServiceID, childServiceModule):
	global googleInit
	
	googleCalendarId = parentParameter
	
	page_token = None
	items = []
	while True:
		events = googleInit.service.events().list(calendarId=googleCalendarId, pageToken=page_token).execute()
		if events['items']:
			for event in events['items']:
				parameter = str(googleCalendarId)+"$$"+str(event['id'])
				item = {"itemID":"virtual", "parentServiceID": parentServiceID, "parentID": parentItemID, "serviceID": childServiceID, "serviceModule": childServiceModule, "serviceTitle": "gcal appointment", "parameter":parameter}
				items.append(item)		
								
		page_token = events.get('nextPageToken')
		if not page_token:
			break

	return items

def getCalendarItems(mdb, calendarID):
	global googleInit
	global time
	
	page_token = None
	items = []
	while True:
		events = googleInit.service.events().list(calendarId=calendarID, pageToken=page_token).execute()
		if events['items']:
			for event in events['items']:
				# work on: uniform timestamp of date and dateTime
				if 'date' in event['start']:
					start = event['start']['date']
					end = event['end']['date']
				elif 'dateTime' in event['start']:
					start = event['start']['dateTime']
					end = event['end']['dateTime']
				else:
					print "could not read time"
					exit()
				
				item = {"start":start, "end":end, "summary":event['summary']}
				items.append(item)		
								
		page_token = events.get('nextPageToken')
		if not page_token:
			break


	return items



