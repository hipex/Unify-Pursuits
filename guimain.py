#!/usr/bin/python

import os
import wx
import MySQLdb as mdb

from StringIO import StringIO
from Tkinter import *
import tkSimpleDialog


from functions import *
import modules
import passwords

mdb.con = mdb.connect('localhost', passwords.Mysql_user, passwords.Mysql_password, 'unify')
mdb.con.autocommit(True)

old_stdout = sys.stdout

class gotoDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		Label(master, text="Value").pack()
		
		self.title("goto dialog")
		
		self.e = Entry(master)
		self.e.pack(padx=5)
		
		return self.e
		
	def apply(self):
		value = self.e.get()
		self.result = value

class addItemDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		Label(master, text="add item").pack()
		
		



class App:
	def __init__(self, master):
		global mdb
		global modules		

		self.CURRENTitem = [0, "none"]
		self.virtualitems = []
		
		self.master = master
		
		master.minsize(1000,450)
		master.title("Unify Pursuits")
		
		frame = Frame(master)
		frame.pack()
		
		# Initiate Menu
		menubar = Menu(root)
		
		MNnavigate = Menu(menubar, tearoff=0)
		MNnavigate.add_command(label="groups", command=self.showGroups)
		MNnavigate.add_command(label="all", command=self.showAll)
		MNnavigate.add_command(label="goto", command=self.showGoto)
		MNnavigate.add_command(label="up", command=self.goUp)
		MNnavigate.add_command(label="Quit", command=frame.quit)
		menubar.add_cascade(label="navigate", menu=MNnavigate)
		
		MNitems = Menu(menubar, tearoff=0)
		MNitems.add_command(label="add", command=self.addItem)
		MNitems.add_command(label="remove", command=self.removeItem)
		MNitems.add_command(label="update", command=self.updateItem)
		menubar.add_cascade(label="items", menu=MNitems)
		
		MNwidgets = Menu(menubar, tearoff=0)
		MNwidgets.add_command(label="add", command=self.addWidget)
		MNwidgets.add_command(label="remove", command=self.removeWidget)
		MNwidgets.add_command(label="update", command=self.updateWidget)
		menubar.add_cascade(label="widgets", menu=MNwidgets)
		
		root.config(menu=menubar)
		# Initiate Main
		
		
	
	def show(self):
		
		answer = showItem(mdb, modules, self.CURRENTitem, self.virtualitems)
		result=answer[0]	
		self.virtualitems = answer[1]
		
		if result == "error-item":
			header(os, "this item does not exist")
	
	## navigate functions
	def showGroups(self):
		# show groups
		showItemsAsTree(mdb, modules, 0, 0)
			
	def showAll(self):
		# show all
		showItemsAsTree(mdb, modules)
	
	
	def showGoto(self):
		dialog = gotoDialog(self.master, self.tkSimpleDialog.Dialog)
		
		answer = dialog.result
		
		# if answer starts with v:
		if str(answer)[0] == 'v':
			# requested virtual item
			
			# strip the v
			self.CURRENTitem[1] = int(answer[1:]) 
		elif answer == 'c':
			# show current
			pass	
			
		else:
			# requested database item
			self.CURRENTitem[0] = answer
			self.CURRENTitem[1] = "none"
		
		self.show()
		
	def goUp(self):
		# go to parent
	
		result = getParent(mdb, self.CURRENTitem)

		if result == "error-item":
			header(os, "no higher group exists")
		else:
			self.CURRENTitem = result
	
		self.show()
	
	## item functions
	
	def addItem(self):
		
		addItem(mdb, modules, self.CURRENTitem, self.virtualitems)
		result = updateItems(mdb, modules)
		header(os, "item added, update affected: "+str(result)+" rows")
		
	def removeItem(self):
		# remove item
		result = removeItem(mdb, modules, self.CURRENTitem)
		if result == True:
			header(os, "item removed")
		elif result == "error-user":
			header(os, "user canceled")
		elif result == "error-server":
			header(os, "error on server, try again")
		else:
			header(os, "something went wrong")	
	
	def updateItem(self):
		# update items
		result = updateItems(mdb, modules)
		header(os, "update: "+str(result)+" rows removed")	
	
	## widget functions
	def addWidget(self):
		# add widget
		result = addWidget(mdb, modules, self.CURRENTitem[0])
		
		if result == True:
			header(os, "Widget created and items added")
		elif result == "no-items":
			header(os, "Widget created, no compatible items available")
		else:
			header(os, "Something went wrong")
	
	def removeWidget(self):
		# remove widget
		result = removeWidget(mdb, modules, self.CURRENTitem[0])
		if result:
			header(os, "Widget removed")
		else:
			header(os, "No widget removed")
	
	def updateWidget(self):
		# update or alter widget
		result = alterWidget(mdb, modules, self.CURRENTitem[0])
		
		if result == True:
			header(os, "Done with widget")
		else:
			header(os, "Somthing went wrong")
	
	
	
root = Tk()
app = App(root)
app.tkSimpleDialog = tkSimpleDialog
root.mainloop()

mdb.con.close()
