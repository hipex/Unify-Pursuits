import googleInit

def show(parameter):
	global googleInit
	
	parameter_part = parameter.partition("$$")
	calendarId=parameter_part[0]
	eventId=parameter_part[2]
	
	event = googleInit.service.events().get(calendarId=calendarId, eventId=eventId).execute()
	print event['summary']
	
	
def add():
	global service
	
	parameter = raw_input("choose parameter: ")
	return [parameter]

def update(con, parameter, parentID):
	return False
