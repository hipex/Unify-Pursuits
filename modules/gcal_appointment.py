import google_services

def show(parameter):
	global google_services
	
	parameter_part = parameter.partition("$$")
	calendarId=parameter_part[0]
	eventId=parameter_part[2]
	
	event = google_services.service.events().get(calendarId=calendarId, eventId=eventId).execute()
	print event['summary']
	
	
def add():
	global service
	
	parameter = raw_input("choose parameter: ")
	return [parameter]

def update(con, parameter, parentID):
	return False
