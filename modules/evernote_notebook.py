import evernoteInit
from datetime import datetime

childServiceModule = 'evernote_note'

def showHeader(parameter):
	print "notebook: "+parameter

def getTitle(parameter):
	global evernoteInit
	
	curnotebook = evernoteInit.note_store.getNotebook(evernoteInit.authToken, parameter)
	
	
	return curnotebook.name
	

def getVirtualItems(parentParameter, parentItemID, parentServiceID, childServiceID, childServiceModule):
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

def getCalendarItems(notebookGUID):
 	# return only notes with reminder / todo date
	global evernoteInit
	global datetime
	
	items = []
	filter = evernoteInit.NoteStoreTypes.NoteFilter()
	filter.notebookGuid = notebookGUID
	spec = evernoteInit.NoteStoreTypes.NotesMetadataResultSpec()
	notelist = evernoteInit.note_store.findNotesMetadata(evernoteInit.authToken, filter,0,10,spec)
	for note in notelist.notes:
		noteinfo = evernoteInit.note_store.getNote(evernoteInit.authToken, note.guid, True, False, False, False)

		if noteinfo.attributes.reminderTime != None:
			noteTimestamp = noteinfo.attributes.reminderTime # given in miliseconds
			
			noteDatetime = datetime.fromtimestamp(noteTimestamp/1000).strftime('%Y-%m-%dT%H:%M:%S+01:00')
			
			item = {"start":noteDatetime, "end":noteDatetime, "summary":noteinfo.title}
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


def check(parameter):
	global evernoteInit
	
	notebooklist = evernoteInit.note_store.listNotebooks(evernoteInit.authToken)
	
	for notebook in notebooklist:
		if notebook.guid == parameter:
			return True
	
	return False
	
	
	
	
