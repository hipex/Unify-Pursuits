

# show header
def header(os, message=False):
	os.system('clear')
	print "commands: q=quit, s=show all g=show groups, u=parent, a=add item, c=update items"
	
	if message != False:
		print message
# end header

# choose itemID or command
def ask(con):
	
	# get input
	answer = raw_input("choose itemID or command: ")
	
	# fetch items with input id
	cur = con.cursor()
	cur.execute("SELECT EXISTS(SELECT 1 FROM items WHERE itemID='"+str(answer)+"')")
	rows = cur.fetchall()
	
	
	# check if correct command
	if answer == 'q' or answer == 'g' or answer == 'a' or answer == 's' or answer == 'u' or answer == 'c':
		return answer
	
	elif rows[0][0] == 1:
		# item exists
		return int(answer)
	
	else:
		# no command, no item. Print error
		print "wrong answer, choose itemID or command"
		return ask(con)

# end ask()

# Get a parents item from the database
def getParent(con, itemID):

	cur = con.cursor()
	cur.execute("SELECT parentID FROM items WHERE itemID='"+str(itemID)+"'")
	rows = cur.fetchall()

	if len(rows) > 0:
		parentID = rows[0][0]
		return parentID
	else: 
		return False
	
# end getParent()

# Show a list of available services and print id and name
def showservices(con):
	cur = con.cursor()
	cur.execute("SELECT * FROM services")
	rows = cur.fetchall()

	# run through te services
	for value in rows:
		print "-"+str(value[0])+": "+str(value[1])
	
# end showservices()

# add a new item to the database
def addItem(con, modules, ADDparent="undefined"):
	print "add item"
	
	if ADDparent == "undefined":
		showItemsAsTree(con)
		ADDparent = int(raw_input("choose parentID: "))
	else:
		print "add to parent: "+str(ADDparent)
	
	showservices(con)
	ADDservice = int(raw_input("choose serviceID: "))
	
	cur = con.cursor()
	cur.execute("SELECT * FROM services WHERE serviceID='"+str(ADDservice)+"'")
	rows = cur.fetchall()
	
	if len(rows) == 0:
		print "module does not exist"
		return False
	else:
		serviceModule = rows[0][2]
		
		module = getattr(modules, serviceModule)
		ADDparameterlist = module.add()
		
		for ADDparameter in ADDparameterlist:
			print ADDparameter
			cur = con.cursor()
			cur.execute("INSERT INTO items (serviceID, parameter, parentID) VALUES ("+str(ADDservice)+", '"+str(ADDparameter)+"', '"+str(ADDparent)+"')")
	
		return True
	
# end addItem()	


# show an item
def showItem(con, modules, itemID):
	cur = con.cursor()
	cur.execute("SELECT * FROM items WHERE itemID='"+str(itemID)+"'")
	rows = cur.fetchall()
	
	if len(rows) > 0:
		serviceID = rows[0][1]
		parameter = rows[0][2]
	
	
		cur = con.cursor()
		cur.execute("SELECT * FROM services WHERE serviceID='"+str(serviceID)+"'")
		rows = cur.fetchall()
	
		serviceModule = rows[0][2]
	
		module = getattr(modules, serviceModule)
		module.show(parameter)

		print "========== CHILDREN ==========="
		showItemsByParent(con, modules, itemID)
		
		return True
		
	else:
		return False
# end showItem()

# show items children of specified parent
def showItemsByParent(con, modules, parentID=0):
	cur = con.cursor()
	query = "SELECT items.itemID, services.serviceID, items.parameter, items.parentID, services.module, services.name FROM items INNER JOIN services ON items.serviceID=services.serviceID  WHERE parentID='"+str(parentID)+"' ORDER BY serviceID ASC"
	cur.execute(query)
	rows = cur.fetchall()
	
	if len(rows) == 0: 
		print "er zijn geen items"
	else:
		# run through items with this parent
		for value in rows:
			itemID = value[0]
			serviceID = value[1]
			parameter = value[2]
			parentID = value[3]
			serviceModule = value[4]
			serviceName = value[5]
			
			print "++ "+serviceName+": "+str(itemID)	
			module = getattr(modules, serviceModule)
			module.show(parameter)
			
# end showItemsByParent()

level = 0
# show items as a tree
def showItemsAsTree(con, parent=0, service="all"):
	global level
		
	query = "SELECT * FROM items WHERE parentID='"+str(parent)+"'"
	if service != "all":
		query = "SELECT * FROM items WHERE serviceID='"+str(service)+"' and parentID='"+str(parent)+"'"
	
	cur = con.cursor()
	cur.execute(query)
	rows = cur.fetchall()

	# run through items with the parent
	for value in rows:
		#level up
		level=level+1
		
		curinfo = con.cursor()
		curinfo.execute("select * FROM services WHERE serviceID='"+str(value[1])+"'")
		serviceinfo = curinfo.fetchall()
		
		#print the item
		print '-'*level+str(value[0])+": ",
		if service == "all":
			print str(serviceinfo[0][1])+", ",
		print str(value[2])
			
		#run again for the groups below
		if value[0] != 0:
			showItemsAsTree(con, value[0], service)
			
		#lebel back
		level=level-1		

# end showItemsAsTree()

def updateItems(mdb, con, modules):
	cur = con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT items.itemID, items.parameter, services.serviceID, services.module FROM items INNER JOIN services ON items.serviceID=services.serviceID  WHERE items.doUpdate = '1'")
	rows = cur.fetchall()
	
	inserts = []
	deletes = []
	
	count = 0
	for label in rows:
		
		module = getattr(modules, str(label['module']))
		answer = module.update(con, label['parameter'], label['itemID'])
		if answer != False:
			ChildServiceModule = answer[0]
			inserts = answer[1]
			deletes = answer[2]
			
			
			cur = con.cursor()
			cur.execute("SELECT serviceID FROM services WHERE module='"+ChildServiceModule+"'")
			ChildServiceID = cur.fetchall()[0][0]
			
			# do inserts
			insert_query_parts = []
			for parameter in inserts:
				insert_query_parts.append("('"+str(ChildServiceID)+"', '"+str(parameter)+"', '"+str(label['itemID'])+"')")
				count=count+1
		
			if insert_query_parts != []:
				insert_query = "INSERT INTO items (serviceID, parameter, parentID) VALUES %s" %  ",".join(insert_query_parts)
		
				cur = con.cursor()
				cur.execute(insert_query)
			
			# do deletes
			delete_query_parts = []
			for parameter in deletes:
				delete_query_parts.append("'"+str(parameter)+"'")
				count=count+1
				
			if delete_query_parts != []:
				delete_query = "DELETE FROM items WHERE serviceID='"+str(ChildServiceID)+"' AND parameter IN (%s)" %  ",".join(delete_query_parts)
				
				cur = con.cursor()
				cur.execute(delete_query)
			
	return count
# end updateItems




