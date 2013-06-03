import google_services

def show(parameter):
	print "calendar: "+parameter
	
	
def add():
	global google_services
	# display calender list
	page_token = None
	count = 0
	calendars = []
	while True:
		calendar_list = google_services.service.calendarList().list(pageToken=page_token).execute()
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

def update(con, parameter, parentID):
	calendarID = parameter
	
	page_token = None
	online_items = []
	while True:
		events = google_services.service.events().list(calendarId=calendarID, pageToken=page_token).execute()
		if events['items']:
			for event in events['items']:
				parameter = str(calendarID)+"$$"+str(event['id'])
				online_items.append(parameter)	
								
		page_token = events.get('nextPageToken')
		if not page_token:
			break

	cur = con.cursor()
	cur.execute("SELECT parameter FROM items WHERE parentID='"+str(parentID)+"'")
	offline_items = cur.fetchall()
	offline_items = [val for subl in offline_items for val in subl]
		
	inserts = [x for x in online_items if x not in offline_items]
	deletes = [x for x in offline_items if x not in online_items]
	
	return ["gcal_appointment", inserts, deletes]
