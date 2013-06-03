#!/usr/bin/python

import os
import wx
import MySQLdb as mdb
import sys


from functions import *
import modules
import passwords


con = mdb.connect('localhost', passwords.Mysql_user, passwords.Mysql_password, 'unify')
con.autocommit(True)
header(os)


CURRENTitem = 0

while True:
	answer = ask(con)
	header(os)
		
	if answer == 'q':
		#quit
		break
	
	elif answer == 'g':
		# show groups
		showItemsAsTree(con, 0, 0)
	
	elif answer == 'a':
		# add item
		addItem(con, modules, CURRENTitem)
		result = updateItems(mdb, con, modules)
		header(os, "item added, update affected: "+str(result)+" rows")
			
	elif answer == 's':
		# show all
		showItemsAsTree(con)
	
	elif answer == 'u':
		# parent
		result = getParent(con, CURRENTitem)

		if result == False:
			header(os, "no higher group exists")
		else:
			CURRENTitem = result
			showItem(con, modules, CURRENTitem)
	
	elif answer == 'c':
		# upate
		result = updateItems(mdb, con, modules)
		header(os, "updated: "+str(result)+" rows")	
					
	else:
		# itemID
		result = showItem(con, modules, answer)
		if result == False:
			header(os, "this item does not exist")
		else: 
			CURRENTitem = answer
con.close()
