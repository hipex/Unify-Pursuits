# Show a list of available services and print id and name
def showservices(mdb):
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT * FROM services")
	services = cur.fetchall()

	# run through te services
	for service in services:
		print "-"+str(service["serviceID"])+": "+str(service["serviceTitle"])
	
# end showservices()


def getItemsByParent(mdb, modules, parentID):
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	query = "SELECT items.itemID, services.serviceID, items.parameter, items.parentID, services.serviceModule, services.serviceTitle FROM items INNER JOIN services ON items.serviceID=services.serviceID  WHERE parentID='"+str(parentID)+"' ORDER BY serviceID ASC"
	cur.execute(query)
	items = list(cur.fetchall())
	
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	query = "SELECT items.itemID, items.parameter, items.serviceID, services.serviceTitle, services.serviceModule FROM items \
			 JOIN services ON items.serviceID=services.serviceID \
			 WHERE items.itemID='"+str(parentID)+"'"
	cur.execute(query)
	parent = cur.fetchone()
	
	if parent:
		module = getattr(modules, parent['serviceModule'])
		if hasattr(module, 'getVirtualItems'):
			virtualItems = module.getVirtualItems(parent['parameter'], parent['serviceID'], parent['serviceTitle'], parent['itemID'])
			items.extend(virtualItems)
	
	return items

# show items as a tree
def showItemsAsTree(mdb, modules, parent=0, service="all", level=0):
		
	items = getItemsByParent(mdb, modules, parent)

	# run through items with the parent
	for item in items:
		if service == 'all' or item['serviceID'] == service:
			#level up
			level=level+1
		
			#print the item
			print '-'*level+str(item['itemID'])+": ",
			if service == "all":
				print str(item['serviceTitle'])+", ",
			print str(item['parameter'])
			
			#run again for the groups below
			if item['parentID'] != item['itemID'] and item['itemID'] != 'virtual':
				showItemsAsTree(mdb, modules, item['itemID'], service, level)
			
			#lebel back
			level=level-1

# add a new item to the database
def addItem(mdb, modules, ADDparent="undefined"):
	print "add item"
	
	if ADDparent == "undefined":
		showItemsAsTree(mdb, modules)
		ADDparent = int(raw_input("choose parentID: "))
	else:
		print "add to parent: "+str(ADDparent)
	
	showservices(mdb)
	ADDserviceID = int(raw_input("choose serviceID: "))
	
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT serviceID, serviceModule, parentServiceID FROM services WHERE serviceID='"+str(ADDserviceID)+"'")
	service = cur.fetchone()
	
	if len(service) == 0:
		print "module does not exist"
		return False
	else:
		
		
		# check if need to be added to database or can be virtual
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT COUNT(1) AS count, items.parameter, services.serviceID FROM items \
					 JOIN services ON items.serviceID=services.serviceID \
					 WHERE services.serviceID='"+str(service['parentServiceID'])+"' \
					 AND itemID='"+str(ADDparent)+"'")
		parent = cur.fetchone()
		
		if parent['count'] == 1 and service['parentServiceID'] != 0:
			# matching parent child
			parentChildMatch = True
			parentParameter = parent['parameter']	
			
		else: 
			parentChildMatch = False
			parentParameter = False
		
		# add to server via module	
		module = getattr(modules, service['serviceModule'])
		ADDparameterlist = module.add(parentParameter)
		
		
		
		if parentChildMatch == False:
			for ADDparameter in ADDparameterlist:
				cur = mdb.con.cursor()
				cur.execute("INSERT INTO items (serviceID, parameter, parentID) VALUES ('"+str(ADDserviceID)+"', '"+str(ADDparameter)+"', '"+str(ADDparent)+"')")
	
		return True
	
# end addItem()	


# show an item
def showItem(mdb, modules, itemID, isvirtual=False):
	
	if isvirtual == True:
		item = itemID
		
	
	else:
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT items.itemID, items.serviceID, items.parameter, services.serviceModule, services.serviceTitle FROM items INNER JOIN services ON items.serviceID=services.serviceID WHERE itemID='"+str(itemID)+"'")
		item = cur.fetchone()
		if len(item) == 0:
			return "error-item"
	

	module = getattr(modules, item['serviceModule'])
	#module.showHeader(item['parameter'])
	
	print "show header from::"
	print item
	
	if isvirtual == True:
		return True
	else: 
		print "========== WIDGETS ==========="
	
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT widgets.widgetID, widgets.preferences, widgettypes.widgettypeModule \
		FROM widgets, widgettypes \
		WHERE widgets.parentID='"+str(itemID)+"' \
		AND widgets.widgettypeID = widgettypes.widgettypeID ")
		widgets = cur.fetchall()
	
		for widget in widgets:
			widgettype = getattr(modules, widget['widgettypeModule'])
			widgettype.show(mdb, modules, widget['widgetID'], widget['preferences'])
		
	
		print "=========== SUB ITEMS =========="
	
		subItems = getItemsByParent(mdb, modules, itemID)
		virtualitems = {}
		
		if len(subItems) == 0: 
			print "er zijn geen items"
		else:
			# run through items with this parent
			virtualcount = 0
			
		
			for item in subItems:
				print "++ "+str(item['serviceTitle'])+": ",
			
			
				if item['itemID'] == 'virtual':
					virtualitems['v'+str(virtualcount)] = item
				
					print "virtual: v"+str(virtualcount)
					virtualcount = virtualcount+1
				
				else:
					print str(item['itemID'])
				
				module = getattr(modules, item['serviceModule'])
				print module.getTitle(item['parameter'])
	
		return [itemID, virtualitems]
# end showItem()


		

# end showItemsAsTree()

def updateItems(mdb, modules):
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT items.itemID, items.parameter, services.serviceID, services.serviceModule \
				 FROM items, services \
				 WHERE items.serviceID=services.serviceID")
	rows = cur.fetchall()
	
	count = 0
	for label in rows:
		
		module = getattr(modules, str(label['serviceModule']))
		rowcount = module.update(mdb, label['parameter'], label['itemID'])
		count=count+rowcount
	
	return count
# end updateItems

def removeItem(mdb, modules, parentID):
	print "remove item"
	
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT items.itemID, items.parameter, services.serviceModule \
				 FROM items, services \
				 WHERE items.serviceID=services.serviceID \
				 AND parentID='"+str(parentID)+"'")
	items = cur.fetchall()
	
	print "c: cancel"
	for item in items:
		print item['serviceModule']
		module = getattr(modules, str(item['serviceModule']))
		itemTitle = module.getTitle(item['parameter'])
		
		print str(item['itemID'])+": "+itemTitle
		
	REMOVEitemID = raw_input("choose itemID to remove: ")
	
	if str(REMOVEitemID) == "c":
		return "error-user"
	else:
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT items.parameter, services.serviceModule FROM items, services WHERE items.serviceID=services.serviceID AND items.itemID='"+REMOVEitemID+"'")
		item = cur.fetchone()
		
		answer = raw_input("remove from server? ")
		if answer == 'y' :
			module = getattr(modules, str(item['serviceModule']))
			result = module.remove(item['parameter'])
			if result: 
				print "removed from server"
			else:
				print "something went wrong while removing from server"
		
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("DELETE FROM items WHERE itemID='"+REMOVEitemID+"'")
		return True


