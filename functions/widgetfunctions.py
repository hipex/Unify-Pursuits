def showWidgettypes(mdb):
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT * FROM widgettypes")
	widgettypes = cur.fetchall()

	# run through te services
	for widgettype in widgettypes:
		print "-"+str(widgettype["widgettypeID"])+": "+str(widgettype["widgettypeTitle"])
# end showWidgettypes()


def addWidget(mdb, modules, ADDparent="undefined"):
	print "add widget"
	
	if ADDparent == "undefined":
		showItemsAsTree(mdb)
		ADDparent = int(raw_input("choose parentID: "))
	else:
		print "add to parent: "+str(ADDparent)
	
	# choose widgettype
	showWidgettypes(mdb)
	ADDwidgettypeID = int(raw_input("choose widgettypeID: "))
	
	# check if widgettypeID exists and get Module
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT widgettypeID, widgettypeModule FROM widgettypes WHERE widgettypeID='"+str(ADDwidgettypeID)+"'")
	widgettype = cur.fetchone()
	
	if len(widgettype) == 0:
		print "widgettype does not exist"
		return False
	else:
		# widgettype exists, run add function of the module for preferences and add widget to database
		module = getattr(modules, str(widgettype['widgettypeModule']))
		ADDpreferences = module.add()
		
		ADDquery = "INSERT INTO widgets (widgettypeID, preferences, parentID) VALUES (%r, %r, %r)" % (str(ADDwidgettypeID), str(ADDpreferences), str(ADDparent))
	
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute(ADDquery)
		ADDwidgetID = cur.lastrowid
		
		
		addToWidget(mdb, modules, ADDparent, ADDwidgetID, widgettype['widgettypeID'])
		
		return True
# end addWidget()


def removeWidget(mdb, modules, parentID):
	print "remove widget"
	
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT widgetID, preferences FROM widgets WHERE parentID='"+str(parentID)+"'")
	widgets = cur.fetchall()
	
	print "c: cancel"
	for widget in widgets:
		print str(widget['widgetID'])+": "+widget['preferences']
		
	REMOVEwidgetID = raw_input("choose widgetID to remove: ")
	
	if str(REMOVEwidgetID) == "c":
		return False
	else:
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("DELETE FROM widgets WHERE widgetID='"+REMOVEwidgetID+"'")
		return True



def alterWidget(mdb, modules, parentID):
	print "alter widget"
	
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT widgetID, preferences, widgettypeID FROM widgets WHERE parentID='"+str(parentID)+"'")
	widgets = cur.fetchall()
	
	print "c: cancel"
	for widget in widgets:
		print str(widget['widgetID'])+": "+widget['preferences']
		
	ALTERwidgetID = raw_input("choose widgetID to alter: ")
	
		
	if str(ALTERwidgetID) == "c":
		return False
	else:
		# check if widgettypeID exists and get Module
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT widgettypeID FROM widgets WHERE widgets.widgetID='"+str(ALTERwidgetID)+"'")
		widget = cur.fetchone()
		
		
		alterOption = raw_input("add or remove item from widget (a/r): ")
		
		if alterOption == 'a':
			addToWidget(mdb, modules, parentID, ALTERwidgetID, widget['widgettypeID'])
			
		elif alterOption == 'r':
			removeFromWidget(mdb, modules, ALTERwidgetID)
			
		else:
			return "error-user"

		return True

def addToWidget(mdb, modules, parentID, widgetID, widgettypeID):
	# select compatible items for widget in this parentID
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT items.itemID, items.serviceID, items.parameter, services.serviceTitle, services.serviceModule \
				 FROM items, services \
				 WHERE items.serviceID = services.serviceID \
				 AND parentID='"+str(parentID)+"' \
				 AND (SELECT COUNT(1) from WidgettypeToService \
				 	  WHERE widgettypeID='"+str(widgettypeID)+"' \
					  AND serviceID=items.serviceID \
					 ) = 1 \
				 AND (SELECT COUNT(1) from WidgetToItem \
				 	  WHERE WidgetToItem.widgetID = '"+str(widgetID)+"' \
				 	  AND WidgetToItem.itemID = items.itemID \
				 	 ) = 0")
	items = cur.fetchall()
	
	# ask which items should be added
	ADDitems = []
	for item in items:
		module = getattr(modules, str(item['serviceModule']))
		title = module.getTitle(str(item['parameter']))
		
		
		answer = raw_input("Add "+str(item['serviceTitle'])+": "+str(title)+" to widget? (y/n): ")
		if answer == 'y':
			ADDitems.append(item)
		elif answer != 'n':
			print "foutief antwoord, negeer item"
		
	if ADDitems == []:
		return "no-items"
	
	# add item references to the widget
	ADDqueryParts = []
	for item in ADDitems:
		ADDqueryParts.append("('"+str(widgetID)+"', '"+str(item['itemID'])+"')")
		
		
	ADDquery = "INSERT INTO WidgetToItem (widgetID, ItemID) VALUES " + ",".join(ADDqueryParts)

	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute(ADDquery)

	return True

def removeFromWidget(mdb, modules, widgetID):
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT items.itemID, items.parameter, services.serviceTitle, services.serviceModule FROM WidgetToItem, items, services \
				 WHERE WidgetToItem.itemID=items.itemID \
				 AND items.serviceID=services.serviceID \
				 AND WidgetToItem.widgetID='"+str(widgetID)+"'")
	items = cur.fetchall()
	
	REMOVEitems = []
	for item in items:
		module = getattr(modules, str(item['serviceModule']))
		title = module.getTitle(str(item['parameter']))
		
		
		answer = raw_input("Remove "+str(item['serviceTitle'])+": "+str(title)+" from widget? (y/n): ")
		if answer == 'y':
			REMOVEitems.append(str(item['itemID']))
		elif answer != 'n':
			print "foutief antwoord, negeer item"
	
	if REMOVEitems == []:
		return "no-items"
	
	# add item references to the widget	
	print REMOVEitems
	REMOVEquery = "DELETE FROM WidgetToItem WHERE itemID IN (" + ",".join(REMOVEitems) +")"
	print REMOVEquery
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute(REMOVEquery)





