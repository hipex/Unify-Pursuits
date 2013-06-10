import evernoteInit
childServiceModule = 'evernote_note'

def show(parameter):
	print "notebook: "+parameter

def getTitle(parameter):
	global evernoteInit
	
	curnotebook = evernoteInit.note_store.getNotebook(evernoteInit.authToken, parameter)
	
	
	return curnotebook.name
	


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

def update(mdb, parameter, parentID):
	global evernoteInit
	global childServiceModule
	
	notebookGUID = parameter
	
	online_items = []
	filter = evernoteInit.NoteStoreTypes.NoteFilter()
	filter.notebookGuid = notebookGUID
	spec = evernoteInit.NoteStoreTypes.NotesMetadataResultSpec()
	notelist = evernoteInit.note_store.findNotesMetadata(evernoteInit.authToken,filter,0,10,spec)

	for note in notelist.notes:
		online_items.append("'"+str(note.guid)+"'")	
	
	query = "DELETE FROM items \
	WHERE parentID='"+str(parentID)+"' \
	AND serviceID = (SELECT serviceID FROM services WHERE serviceModule='"+str(childServiceModule)+"')  \
	AND parameter NOT IN ("+','.join(online_items)+")"
	
	print query
	
	cur = mdb.con.cursor()
	cur.execute(query)
	
	return cur.rowcount
