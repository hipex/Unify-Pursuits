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
		break
	
	elif answer == 'g':
		showItemsAsTree(con, 0, 0)
	
	elif answer == 'a':
		additem(con, modules, CURRENTitem)
		header(os, "item added")
	
	
	elif answer == 's':
		showItemsAsTree(con)
	
	elif answer == 'u':
		result = getParent(con, CURRENTitem)

		if result == "Error":
			print "no higher group exists"
		else:
			CURRENTitem = result
			showItem(con, modules, CURRENTitem)
	
	else:
		cur = con.cursor()
		cur.execute("SELECT EXISTS(SELECT 1 FROM items WHERE itemID='"+str(answer)+"')")
		rows = cur.fetchall()
		
		if rows[0]:
			CURRENTitem = answer	
			showItem(con, modules, CURRENTitem)
		
con.close()
