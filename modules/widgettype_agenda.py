import time
import operator

def show(modules, items, widgetID, preferences):
	global operator

	
	calendars = items
	
	
	
	print "++++show widget: "+str(widgetID)
	print "met items:"
	
	appointments = []
	
	# fetch all appointments from different calendars and modules
	for calendar in calendars:
		module = getattr(modules, str(calendar['serviceModule']))
		calendarItems = module.getCalendarItems(calendar['parameter'])
		
		appointments.extend(calendarItems)
	
	# sorting
	appointments.sort(key=operator.itemgetter("start"))
	
	# printing
	for appointment in appointments:
		print appointment

def add():
	ADDpreferences = raw_input("choose preferences: ")
	return ADDpreferences
