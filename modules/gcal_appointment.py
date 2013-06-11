import googleInit

def showHeader(parameter):
	global googleInit
	
	parameter_part = parameter.partition("$$")
	calendarId=parameter_part[0]
	eventId=parameter_part[2]
	
	event = googleInit.service.events().get(calendarId=calendarId, eventId=eventId).execute()
	print "gcal event: "+event['summary']


	
def getTitle(parameter):
	global googleInit 
	
	parameter_part = parameter.partition("$$")
	calendarId=parameter_part[0]
	eventId=parameter_part[2]
	
	event = googleInit.service.events().get(calendarId=calendarId, eventId=eventId).execute()
	return event['summary']

def getCalendarItems(mdb, parameter):
	global googleInit 
	
	parameter_part = parameter.partition("$$")
	calendarId=parameter_part[0]
	eventId=parameter_part[2]
	
	event = googleInit.service.events().get(calendarId=calendarId, eventId=eventId).execute()
	if 'date' in event['start']:
		start = event['start']['date']
		end = event['end']['date']
	elif 'dateTime' in event['start']:
		start = event['start']['dateTime']
		end = event['end']['dateTime']
	else:
		print "could not read time"
		exit()

	return [{"start":start, "end":end, "summary":event['summary']}]
	
	
def add(parentParameter):
	global googleInit
	
	if parentParameter == False:
		# chooose calendar manually
		
		print "To which calendar: "
	
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
		googleCalendarId = calendars[calendarno]
	
	else:
		# already in calendar
		googleCalendarId = parentParameter
	
	summary = raw_input("give summary: ")
	timezone = raw_input("give timezone like: +HH or -HH ")
	startDate = raw_input("give start date like: YYYY-MM-DD ")
	startTime = raw_input("give start time like: HH:MM:SS.SSS ")
	
	start = startDate+"T"+startTime+timezone+":00"
	
	endDate = raw_input("give end date like: YYYY-MM-DD ")
	endTime = raw_input("give end time like: HH:MM:SS.SSS ")
	
	end = endDate+"T"+endTime+timezone+":00"
	
	event = {
	  'summary': summary,
	  'start': {
		'dateTime': start
	  },
	  'end': {
		'dateTime': end
	  }
	}

	created_event = googleInit.service.events().insert(calendarId=googleCalendarId, body=event).execute()
		
	parameter = str(googleCalendarId)+"$$"+str(created_event['id'])
	
	return [parameter]

def remove(parameter):
	global googleInit
	
	parameter_part = parameter.partition("$$")
	googleCalendarId=parameter_part[0]
	eventId=parameter_part[2]
	
	googleInit.service.events().delete(calendarId=googleCalendarId, eventId=eventId).execute()
	
	return True

def update(mdb, parameter, itemID):
	global googleInit
	
	parameter_part = parameter.partition("$$")
	calendarId=parameter_part[0]
	eventId=parameter_part[2]
	
	page_token = None
	while True:
		events = googleInit.service.events().list(calendarId=calendarId, pageToken=page_token).execute()
		if events['items']:
			for event in events['items']:
				if event['id'] == eventId:
					return 'none'
		page_token = events.get('nextPageToken')
		if not page_token:
			break
	
	
	return itemID

