# show header
def header(os, message=False):
	os.system('clear')
	print "commands: q=quit, s=show all, g=show groups, c=reload current, u=parent, ia=item add, ir=item remove, iu=item update, wa=widget add, wr=widget remove, wu=widget update/alter"
	
	if message != False:
		print message
# end header

# choose itemID or command
def ask(mdb):
	
	# get input
	answer = raw_input("choose itemID or command: ")
	
	# fetch items with input id
	cur = mdb.con.cursor()
	cur.execute("SELECT EXISTS(SELECT 1 FROM items WHERE itemID='"+str(answer)+"')")
	rows = cur.fetchone()
	
	commands = ['q', 'c', 's', 'g', 'u', 'ia', 'ir', 'iu', 'wa', 'wr', 'wu']
	
	# check if correct command
	if answer in commands:
		return answer
	
	elif str(answer)[0]=='v':
		return answer
	
	elif rows[0] == 1:
		# item exists
		return int(answer)
	
	else:
		# no command, no item. Print error
		print "wrong answer, choose itemID or command"
		return ask(mdb)

# end ask()

# Get a parents item from the database
def getParent(mdb, CURRENTitem):
	if CURRENTitem[1] != "none":
		# currently in virtual, parent already stored in CURRENTitem
		CURRENTitem[1] = "none"
		
	else:
		itemID = CURRENTitem[0]
	
		# get parentID and check if the row exists
		cur = mdb.con.cursor()
		cur.execute("SELECT itemID FROM items WHERE itemID=(SELECT parentID FROM items WHERE itemID='"+str(itemID)+"')")
		rows = cur.fetchone()

		if not rows or len(rows) == 0:
			return "error-item"
		else:
			CURRENTitem[0] = rows[0]
	
	return CURRENTitem
	
# end getParent()





