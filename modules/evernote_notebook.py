import evernoteInit


def show(parameter):
	print "notebook: "+parameter
	
	
def add():
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

def update(con, parameter, parentID):
	global evernoteInit
	
	notebookGUID = parameter
	
	online_items = []
	filter = evernoteInit.NoteStoreTypes.NoteFilter()
	filter.notebookGuid = notebookGUID
	spec = evernoteInit.NoteStoreTypes.NotesMetadataResultSpec()
	notelist = evernoteInit.note_store.findNotesMetadata(evernoteInit.authToken,filter,0,10,spec)

	for note in notelist.notes:
		online_items.append(note.guid)	
	
	cur = con.cursor()
	cur.execute("SELECT parameter FROM items WHERE parentID='"+str(parentID)+"'")
	offline_items = cur.fetchall()
	offline_items = [val for subl in offline_items for val in subl]
		
	inserts = [x for x in online_items if x not in offline_items]
	deletes = [x for x in offline_items if x not in online_items]
	
	return ["evernote_note", inserts, deletes]
