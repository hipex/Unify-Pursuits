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
	# database items
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	query = "SELECT items.itemID, services.serviceID, items.parameter, items.parentID, services.serviceModule, services.serviceTitle FROM items INNER JOIN services ON items.serviceID=services.serviceID  WHERE parentID='"+str(parentID)+"' ORDER BY serviceID ASC"
	cur.execute(query)
	items = list(cur.fetchall())
	itemparameters = tuple(x['parameter'] for x in items)
	
	
	# virtual items
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	query = "SELECT items.itemID, items.parameter, items.serviceID, services.serviceTitle, services.serviceModule FROM items \
			 JOIN services ON items.serviceID=services.serviceID \
			 WHERE items.itemID='"+str(parentID)+"'"
	cur.execute(query) # get parent data
	parent = cur.fetchone()
	
	
	
	virtualitems = []
	
	if parent:
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		query = "SELECT serviceID, serviceModule FROM services WHERE parentServiceID='"+str(parent['serviceID'])+"'"
		cur.execute(query) # get parent data
		child = cur.fetchone()
		module = getattr(modules, parent['serviceModule'])
		if hasattr(module, 'getVirtualItems'):
			virtualItemlist = module.getVirtualItems(parent['parameter'], parent['itemID'], parent['itemID'], child['serviceID'], child['serviceModule'])
			virtualitems.extend(virtualItemlist)
	
	filteredVirtualitems = []
	
	virtualitems = [x for x in virtualitems if x['parameter'] not in itemparameters]
	
	
	return [items,virtualitems]

# show items as a tree
def showItemsAsTree(mdb, modules, parent=0, service="all", level=0):
		
	result = getItemsByParent(mdb, modules, parent)
	items = result[0]
	virtualitems = result[1]
	
	items.extend(virtualitems)
	
	
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
def addItem(mdb, modules, CURRENTitem="undefined", virtualitems=[]):
	print "add item"

	if CURRENTitem[0] == "undefined":
		showItemsAsTree(mdb, modules)
		ADDparent = int(raw_input("choose parentID: "))
	
	elif CURRENTitem[1] != "none":
		# virtual item, create database entry
		parent = virtualitems[CURRENTitem[1]]
		
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("INSERT INTO items (serviceID, parameter, parentID) VALUES \
					 ('"+str(parent['serviceID'])+"', '"+str(parent['parameter'])+"', '"+str(parent['parentID'])+"')")
		ADDparent = cur.lastrowid
		
		print "add to virtual item: "+str(CURRENTitem[1])+" which is now: "+str(ADDparent)
		
	else:
		ADDparent = CURRENTitem[0]
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
def showItem(mdb, modules, CURRENTitem, virtualitems={}):
	
	if CURRENTitem[1] != "none":
		# virtual item
		item = virtualitems[CURRENTitem[1]]
		
	
	else:
		# database item
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT items.itemID, items.serviceID, items.parameter, services.serviceModule, services.serviceTitle FROM items INNER JOIN services ON items.serviceID=services.serviceID WHERE itemID='"+str(CURRENTitem[0])+"'")
		item = cur.fetchone()
		if len(item) == 0:
			return "error-item"
	

	module = getattr(modules, item['serviceModule'])
	# show header via module
	module.showHeader(item['parameter'])
	
	if CURRENTitem[1] != "none":
		# virutal items have no stuff on page
		return [True,virtualitems]
		
	else: 
		print "========== WIDGETS ==========="
	
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT widgets.widgetID, widgets.preferences, widgettypes.widgettypeModule \
		FROM widgets, widgettypes \
		WHERE widgets.parentID='"+str(item['itemID'])+"' \
		AND widgets.widgettypeID = widgettypes.widgettypeID ")
		widgets = cur.fetchall()
	
		for widget in widgets:
			cur = mdb.con.cursor(mdb.cursors.DictCursor)
			cur.execute("SELECT items.itemID, items.serviceID, items.parameter, services.serviceModule \
			FROM items, WidgetToItem, services \
			WHERE items.itemID=WidgetToItem.itemID \
			AND items.serviceID=services.serviceID \
			AND WidgetToItem.widgetID='"+str(widget['widgetID'])+"'")
			items = cur.fetchall()	
		
		
			widgettype = getattr(modules, widget['widgettypeModule'])
			widgettype.show(modules, items, widget['widgetID'], widget['preferences'])
		
	
		print "=========== SUB ITEMS =========="
	
		result = getItemsByParent(mdb, modules, item['itemID'])
		subitems=result[0]
		virtualitems=result[1]
		
		
		if len(subitems)+len(virtualitems) == 0: 
			print "er zijn geen items"
		else:
			# run through items with this parent
		
			for item in subitems:
				print "++ "+str(item['itemID'])+"; "+str(item['serviceTitle'])+": ",
				
				module = getattr(modules, item['serviceModule'])
				print module.getTitle(item['parameter'])
			
			if virtualitems != []:
				print "virtualitems: "
			
				for no,item in enumerate(virtualitems):
					print "++ v"+str(no)+"; "+str(item['serviceTitle'])+": ",
				
					module = getattr(modules, item['serviceModule'])
					print module.getTitle(item['parameter'])
				
		return [item['itemID'], virtualitems]
# end showItem()


		

# end showItemsAsTree()

def updateItems(mdb, modules):
	
	
		
		
		 
				 
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT items.itemID, items.parameter, services.serviceID, services.serviceModule \
				 FROM items, services \
				 WHERE items.serviceID=services.serviceID")
	items = cur.fetchall()
	
	
	count = 0
	
	removequery_parts = []
	for item in items:
		
				 
		
		
		module = getattr(modules, str(item['serviceModule']))
		result = module.check(item['parameter'])

		if result == False:
			removequery_parts.append("'"+str(item['itemID'])+"'")
			count=count+1
		
	if removequery_parts != []:
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		query = "DELETE FROM items WHERE itemID IN ("+",".join(removequery_parts)+")"
		cur.execute(query)
	
	
	# remove items where parentID is pointing no where
	while True:
		cur = mdb.con.cursor(mdb.cursors.DictCursor)
		cur.execute("DELETE items FROM items LEFT JOIN items AS parent ON items.parentID = parent.itemID WHERE parent.itemID is NULL")
		if cur.rowcount == 0:
			break
		else:
			count=count+cur.rowcount
	
	return count
# end updateItems

def removeItem(mdb, modules, CURRENTitem):
	print "remove item"
	
	# can only remove with database parent; no virtual since they don't have childs
	parentID=CURRENTitem[0]
	
	result = getItemsByParent(mdb, modules, parentID)
	items=result[0]
	virtualitems=result[1]
	
	print "c: cancel"
	for item in items:

		module = getattr(modules, str(item['serviceModule']))
		itemTitle = module.getTitle(item['parameter'])
		
		print str(item['itemID'])+": ",
			
		print item['serviceModule']+": "+itemTitle
	
	
	print "virtualitems:"
	for no,item in enumerate(virtualitems):
		module = getattr(modules, str(item['serviceModule']))
		itemTitle = module.getTitle(item['parameter'])
		
		print "v"+str(no)+": "+itemTitle
	
		
	REMOVEitemID = raw_input("choose itemID to remove: ")
	
	if str(REMOVEitemID) == "c":
		return "error-user"
	else:
		if str(REMOVEitemID)[0] == 'v':
			item = virtualitems[str(REMOVEitemID)[1:]]
		
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


