import evernoteInit
childServiceModule = 'evernote_note'

def showHeader(parameter):
	print "notebook: "+parameter

def getTitle(parameter):
	global evernoteInit
	
	curnotebook = evernoteInit.note_store.getNotebook(evernoteInit.authToken, parameter)
	
	
	return curnotebook.name
	

def getVirtualItems(parentParameter, parentItemID, parentServiceID, parentServiceTitle, childServiceID, childServiceModule):
	items = []
	
	notebookGUID = parentParameter
	
	filter = evernoteInit.NoteStoreTypes.NoteFilter()
	filter.notebookGuid = notebookGUID
	spec = evernoteInit.NoteStoreTypes.NotesMetadataResultSpec()
	notelist = evernoteInit.note_store.findNotesMetadata(evernoteInit.authToken,filter,0,10,spec)

	for note in notelist.notes:
		parameter = note.guid
		item = {"itemID":"virtual", "parentServiceID": parentServiceID, "parentID": parentItemID, "serviceID": childServiceID, "serviceModule": childServiceModule, "serviceTitle": "evernote note", "parameter":parameter}
		items.append(item)
	
	return items

def add(parentParameter):
	global evernoteInit
	# display calender list
	page_token = None
	count = 0
	notebooks = []
	
	
	notebook_list = evernoteInit.note_store.listNotebooks()
	
	for notebook in notebook_list:
		notebooks.append(notebook.guid)
		print str(count)+": "+notebook.name
		count = count+1
			
	notebookno = int(raw_input("choose notebook: "))
	notebookGUID = notebooks[notebookno]
	
	return [notebookGUID]
	
	
def remove(parameter):
	global evernoteInit
	
	evernoteInit.note_store.expungeNotebook(evernoteInit.authToken, parameter)
	return True


def update(mdb, parameter, itemID):
	global evernoteInit
	
	notebooklist = evernoteInit.note_store.listNotebooks(evernoteInit.authToken)
	
	for notebook in notebooklist:
		if notebook.guid == parameter:
			return 'none'
	
	# notebook non existing
	cur = mdb.con.cursor(mdb.cursors.DictCursor)
	cur.execute("DELETE FROM items WHERE itemID='"+str(itemID)+"'")

	return itemID
	
	
	
	
