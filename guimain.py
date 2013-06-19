#!/usr/bin/python

import os
import wx
import MySQLdb as mdb
import sys
from StringIO import StringIO

from functions import *
import modules
import passwords

mdb.con = mdb.connect('localhost', passwords.Mysql_user, passwords.Mysql_password, 'unify')
mdb.con.autocommit(True)

old_stdout = sys.stdout


CURRENTitem = [0, "none"]
virtualitems = []

class gotoDialog(wx.Dialog):
 	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size=(350,300))
		
		hbox = wx.BoxSizer(wx.VERTICAL)
		self.boxGo = wx.TextCtrl(self, -1)
		btnGo = wx.Button(self, -1, 'go')
		hbox.Add(self.boxGo)
		hbox.Add(btnGo)
		
		self.SetSizer(hbox)
		
		btnGo.Bind(wx.EVT_BUTTON, self.OnClose)
		
	def OnClose(self, e):
		self.Destroy()


class Unify(wx.Frame):
	
	def __init__(self, *args, **kwargs):
		super(Unify, self).__init__(*args, **kwargs)
		
		self.InitUI()
	
	def InitUI(self):
		menubar= wx.MenuBar()
		
		mainMenu = wx.Menu()
		
		mainGoto = mainMenu.Append(wx.ID_ANY, 'Goto..', 'Goto an item page')
		mainUp = mainMenu.Append(wx.ID_ANY, 'Go up', 'Move an item up')
		mainReload = mainMenu.Append(wx.ID_ANY, 'Reload', 'reload current page')
		mainQuit = mainMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
		
		self.Bind(wx.EVT_MENU, self.goto, mainGoto)
		self.Bind(wx.EVT_MENU, self.goUp, mainUp)
		self.Bind(wx.EVT_MENU, self.doReload, mainReload)
		self.Bind(wx.EVT_MENU, self.doQuit, mainQuit)
				
		menubar.Append(mainMenu, '&Navigation')
		
		itemMenu = wx.Menu()
		itemAdd = itemMenu.Append(wx.ID_ANY, 'add', 'add an item')
		itemRemove = itemMenu.Append(wx.ID_ANY, 'remove', 'remove an item')
		itemCheck = itemMenu.Append(wx.ID_ANY, 'check', 'check items for existence')
		
		self.Bind(wx.EVT_MENU, self.itemAdd, itemAdd)
		self.Bind(wx.EVT_MENU, self.itemRemove, itemRemove)
		self.Bind(wx.EVT_MENU, self.itemCheck, itemCheck)
		
		menubar.Append(itemMenu, '&item')
		
		self.SetMenuBar(menubar)
		
		self.textplace = wx.TextCtrl(self, style= wx.TE_MULTILINE )
		
		self.SetSize((300,200))
		self.SetTitle('Unify Pursuits')
		self.Show(True)
	
	def goto(self, e):
		global virtualitems
		global CURRENTitem
		global mdb
		global modules
		
		dia = gotoDialog(self, -1, 'buttons')
 		res = dia.ShowModal()
		answer = dia.boxGo.GetValue()

		dia.Destroy() 
		outputty = StringIO()
		sys.stdout = outputty
		
		# if answer starts with v:
		if str(answer)[0] == 'v':
			# requested virtual item
			
			# strip the v
			CURRENTitem[1] = int(answer[1:]) 	
			
		else:
			# requested database item
			CURRENTitem[0] = answer
			CURRENTitem[1] = "none"
		
		answer = showItem(mdb, modules, CURRENTitem, virtualitems)

		result=answer[0]
		
		virtualitems = answer[1]

		
		if result == "error-item":
			header(os, "this item does not exist")
		
		result_string = outputty.getvalue()
		self.textplace.Clear()
		self.textplace.ChangeValue(result_string)
		
				
	def goUp(self, e):
		global virtualitems
		global CURRENTitem
		global mdb
		global modules
		
		
		outputty = StringIO()
		sys.stdout = outputty
		
		result = getParent(mdb, CURRENTitem)

		if result == "error-item":
			header(os, "no higher group exists")
		else:
			CURRENTitem = result
		
		answer = showItem(mdb, modules, CURRENTitem, virtualitems)

		result=answer[0]
		
		virtualitems = answer[1]

		
		if result == "error-item":
			header(os, "this item does not exist")
		
		result_string = outputty.getvalue()
		self.textplace.Clear()
		self.textplace.ChangeValue(result_string)
				
		
	def doReload(self, e):
		global virtualitems
		global CURRENTitem
		global mdb
		global modules
		
		outputty = StringIO()
		sys.stdout = outputty
		
		answer = showItem(mdb, modules, CURRENTitem, virtualitems)

		result=answer[0]
		
		virtualitems = answer[1]

		
		if result == "error-item":
			header(os, "this item does not exist")
		
		result_string = outputty.getvalue()
		self.textplace.Clear()
		self.textplace.ChangeValue(result_string)
		
	def itemAdd(self, e):
		global virtualitems
		global CURRENTitem
		global mdb
		global modules
		
		outputty = StringIO()
		sys.stdout = outputty
		
		addItem(mdb, modules, CURRENTitem, virtualitems)
		result = updateItems(mdb, modules)
		header(os, "item added, update affected: "+str(result)+" rows")
		
		result_string = outputty.getvalue()
		self.textplace.Clear()
		self.textplace.ChangeValue(result_string)
		
		
	def itemRemove(self, e):
		global virtualitems
		global CURRENTitem
		global mdb
		global modules
		
		outputty = StringIO()
		sys.stdout = outputty
		
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
		
		result_string = outputty.getvalue()
		self.textplace.Clear()
		self.textplace.ChangeValue(result_string)
		
		
	def itemCheck(self, e):
		global virtualitems
		global CURRENTitem
		global mdb
		global modules
		
		outputty = StringIO()
		sys.stdout = outputty
		
		result = updateItems(mdb, modules)
		header(os, "update: "+str(result)+" rows removed")	
		
		result_string = outputty.getvalue()
		self.textplace.Clear()
		self.textplace.ChangeValue(result_string)
	
	
	def doQuit(self, e):
		self.Close
	

if __name__=='__main__':
	app = wx.App()
	Unify(None)
	app.MainLoop()



header(os)


# integrate below into gui menu
"""
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

"""

mdb.con.close()
