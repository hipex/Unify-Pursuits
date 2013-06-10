# show header
def header(os, message=False):
	os.system('clear')
	print "commands: q=quit, s=show all g=show groups, u=parent, ia=item add, ir, item remove, iu=item update, wa=widget add, wr=widget remove, wu=widget update/alter"
	
	if message != False:
		print message
# end header

# choose itemID or command
def ask(mdb, virtualitems):
	
	# get input
	answer = raw_input("choose itemID or command: ")
	
	# fetch items with input id
	cur = mdb.con.cursor()
	cur.execute("SELECT EXISTS(SELECT 1 FROM items WHERE itemID='"+str(answer)+"')")
	rows = cur.fetchone()
	
	commands = ['q', 's', 'g', 'u', 'ia', 'ir', 'iu', 'wa', 'wr', 'wu']
	
	# check if correct command
	if answer in commands or answer in virtualitems:
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
def getParent(mdb, itemID):

	cur = mdb.con.cursor()
	cur.execute("SELECT parentID FROM items WHERE itemID='"+str(itemID)+"'")
	rows = cur.fetchall()

	if len(rows) > 0:
		parentID = rows[0][0]
		return parentID
	else: 
		return "error-item"
	
# end getParent()





