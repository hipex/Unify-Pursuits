

# show header
def header(os, message=False):
	os.system('clear')
	print "commands: q=quit, s=show all g=show groups, u=parent, a=add item"
	
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
	if answer == 'q' or answer == 'g' or answer == 'a' or answer == 's' or answer == 'u':
		return answer
	
	elif rows[0]:
		# item exists
		return int(answer)
	
	else:
		# no command, no item. Print error
		print "wrong answer"
		return ask(con)

# end ask()

# Get a parents item from the database
def getParent(con, itemID):

	cur = con.cursor()
	cur.execute("SELECT parentID FROM items WHERE itemID='"+str(itemID)+"'")
	rows = cur.fetchall()

	if len(rows) == 1:
		parentID = rows[0][0]
		return parentID
	else: 
		return "Item does not exist"
	
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
def additem(con, modules, ADDparent="undefined"):
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
	
# end additem()	


# show an item
def showItem(con, modules, itemID):

	cur = con.cursor()
	cur.execute("SELECT * FROM items WHERE itemID='"+str(itemID)+"'")
	rows = cur.fetchall()
	
	if len(rows) == 0:
		print "this item does not exist"
	
	serviceID = rows[0][1]
	parameter = rows[0][2]
	
	
	cur = con.cursor()
	cur.execute("SELECT * FROM services WHERE serviceID='"+str(serviceID)+"'")
	rows = cur.fetchall()
	
	serviceModule = rows[0][2]
	
	module = getattr(modules, serviceModule)
	module.show(parameter)

	print "========== CHILDREN ==========="
	showItemsByParent(con, itemID)

# end showItem()

# show items children of specified parent
def showItemsByParent(con, parentID=0):
	cur = con.cursor()
	cur.execute("SELECT * FROM items WHERE parentID='"+str(parentID)+"' ORDER BY serviceID ASC")
	rows = cur.fetchall()
	
	if len(rows) == 0: 
		print "er zijn geen items"
	else:
		# run through items with this parent
		for value in rows:
			itemID = value[0]
			serviceID = value[1]
			parameter = value[2]
			groupID = value[3]
			
			curinfo = con.cursor()
			curinfo.execute("SELECT name FROM services WHERE serviceID='"+str(serviceID)+"'")
			serviceinfo = curinfo.fetchall()
			
			
			print "++ item: "+str(itemID)
			print "service: "+str(serviceinfo[0][0])
			print "parameter: "+str(parameter)	
			
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

	
	
	
	
	

