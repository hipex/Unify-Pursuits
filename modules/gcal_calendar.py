import googleInit
import time

childServiceModule = "gcal_appointment"

def showHeader(parameter):
	print "calendar: "+parameter
	
def showSubItems(mdb, parentID, parameter):
	
	calendarID = parameter
	
	page_token = None
	items=[]
	while True:
		events = googleInit.service.events().list(calendarId=calendarID, pageToken=page_token).execute()
		if events['items']:
			for event in events['items']:
				parameter = "'"+str(calendarID)+"$$"+str(event['id'])+"'"
				
				item = {"itemID":"virtual", "parameter":parameter}
				
				items.append(item)	
								
		page_token = events.get('nextPageToken')
		if not page_token:
			break
	
	######### todo: remove duplicates from online and offline
	
	cur = mdb.con.cursor()
	cur.execute("SELECT itemID, parameter \
				 FROM items, services \
				 WHERE items.serviceID=services.serviceID \
				 AND parentID = '"+parentID+"'")
	databaseItems = cur.fetchall()
	
	items.extend(databaseItems)
	

	

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

def update(mdb, parameter, parentID):
	global childServiceModule
	
	calendarID = parameter
	
	page_token = None
	online_items = []
	while True:
		events = googleInit.service.events().list(calendarId=calendarID, pageToken=page_token).execute()
		if events['items']:
			for event in events['items']:
				parameter = "'"+str(calendarID)+"$$"+str(event['id'])+"'"
				online_items.append(parameter)	
								
		page_token = events.get('nextPageToken')
		if not page_token:
			break
	
	if online_items != []:
		query = "DELETE FROM items \
		WHERE parentID='"+str(parentID)+"' \
		AND serviceID = (SELECT serviceID FROM services WHERE serviceModule='"+str(childServiceModule)+"')  \
		AND parameter NOT IN ("+','.join(online_items)+")"
	
	
		cur = mdb.con.cursor()
		cur.execute(query)
	
		return cur.rowcount
	else:
		return 0

def getTitle(parameter):
	global googleInit

	calendar_list_entry = googleInit.service.calendarList().get(calendarId=parameter).execute()
	return calendar_list_entry['summary']

def getVirtualItems(parameter, itemID, serviceID, serviceTitle):
	global googleInit
	global childServiceModule
	
	googleCalendarId = parameter
	
	page_token = None
	items = []
	while True:
		events = googleInit.service.events().list(calendarId=googleCalendarId, pageToken=page_token).execute()
		if events['items']:
			for event in events['items']:
				parameter = str(googleCalendarId)+"$$"+str(event['id'])
				item = {"itemID":"virtual??"+parameter, "serviceID": serviceID, "parentID": itemID, "serviceModule": childServiceModule, "serviceTitle": "gcal appointment", "parameter":parameter}
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



