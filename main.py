#!/usr/bin/python

import os
import wx
import MySQLdb as mdb
import sys


from functions import *
import modules
import passwords


mdb.con = mdb.connect('localhost', passwords.Mysql_user, passwords.Mysql_password, 'unify')
mdb.con.autocommit(True)


header(os)


CURRENTitem = [0, "none"]
virtualitems = []

while True:
	
	answer = ask(mdb)
	
	header(os)
	
	
	
	## navigate commands
	if answer == 'q':
		# quit
		break
	
	
			
	elif answer == 'g':
		# show groups
		showItemsAsTree(mdb, modules, 0, 0)
			
	elif answer == 's':
		# show all
		showItemsAsTree(mdb, modules)
	
	
	
	## item commands
	elif answer == 'ia':
		# add item
		
		addItem(mdb, modules, CURRENTitem, virtualitems)
		result = updateItems(mdb, modules)
		header(os, "item added, update affected: "+str(result)+" rows")
		
	elif answer == 'ir':
		# remove item
		result = removeItem(mdb, modules, CURRENTitem)
		if result == True:
			header(os, "item removed")
		elif result == "error-user":
			header(os, "user canceled")
		elif result == "error-server":
			header(os, "error on server, try again")
		else:
			header(os, "something went wrong")	
	
	elif answer == 'iu':
		# update items
		result = updateItems(mdb, modules)
		header(os, "update: "+str(result)+" rows removed")	
	
	
	
	## widget commands
	elif answer == 'wa':
		# add widget
		result = addWidget(mdb, modules, CURRENTitem[0])
		
		if result == True:
			header(os, "Widget created and items added")
		elif result == "no-items":
			header(os, "Widget created, no compatible items available")
		else:
			header(os, "Something went wrong")
	
	elif answer == 'wr':
		# remove widget
		result = removeWidget(mdb, modules, CURRENTitem[0])
		if result:
			header(os, "Widget removed")
		else:
			header(os, "No widget removed")
	
	elif answer == 'wu':
		# update or alter widget
		result = alterWidget(mdb, modules, CURRENTitem[0])
		
		if result == True:
			header(os, "Done with widget")
		else:
			header(os, "Somthing went wrong")
			
	else:
		# all commands that show itemID, up or virtual id
		
		if answer == 'u':
			# go to parent
	
			result = getParent(mdb, CURRENTitem)

			if result == "error-item":
				header(os, "no higher group exists")
			else:
				CURRENTitem = result
				
				
		# if answer starts with v:
		elif str(answer)[0] == 'v':
			# requested virtual item
			
			# strip the v
			CURRENTitem[1] = int(answer[1:]) 
		elif answer == 'c':
			# show current
			pass	
			
		else:
			# requested database item
			CURRENTitem[0] = answer
			CURRENTitem[1] = "none"
		
		answer = showItem(mdb, modules, CURRENTitem, virtualitems)

		result=answer[0]
		
		virtualitems = answer[1]

		
		if result == "error-item":
			header(os, "this item does not exist")
# end while

mdb.con.close()
