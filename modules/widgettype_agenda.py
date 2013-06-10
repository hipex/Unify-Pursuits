import time
import operator

def show(mdb, modules, widgetID, preferences):
	global operator

	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT items.itemID, items.serviceID, items.parameter, services.serviceModule \
	FROM items, WidgetToItem, services \
	WHERE items.itemID=WidgetToItem.itemID \
	AND items.serviceID=services.serviceID \
	AND WidgetToItem.widgetID='"+str(widgetID)+"'")
	calendars = cur.fetchall()	
	
	
	
	
	print "++++show widget: "+str(widgetID)
	print "met items:"
	
	appointments = []
	
	# fetch all appointments from different calendars and modules
	for calendar in calendars:
		module = getattr(modules, str(calendar['serviceModule']))
		calendarItems = module.getCalendarItems(mdb, calendar['parameter'])
		
		appointments.extend(calendarItems)
	
	# sorting
	appointments.sort(key=operator.itemgetter("start"))
	
	# printing
	for appointment in appointments:
		print appointment

def add():
	ADDpreferences = raw_input("choose preferences: ")
	return ADDpreferences
