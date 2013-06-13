import evernoteInit

def showHeader(parameter):
	global evernoteInit

	note = evernoteInit.note_store.getNote(evernoteInit.authToken, parameter, True, False, False, False)
	print "titel: "+note.title
	print note.content
	
def getTitle(parameter):
	global evernoteInit
	
	note = evernoteInit.note_store.getNote(evernoteInit.authToken, parameter, True, False, False, False)
	
	return note.title
	

	
def add(parentParameter):
	global service
	
	if parentParameter == False:
		# choose notebook manually
		pass
		
	else:
		evernoteNotebook = parentParameter
	
	parameter = raw_input("choose parameter: ")
	return [parameter]

def update(mdb, parameter, itemID):
	global evernoteInit
	
	try:
		evernoteInit.note_store.getNote(evernoteInit.authToken, parameter, False, False, False, False)
	except evernoteInit.errorTypes.EDAMNotFoundException:
		# note note found
		return itemID
	
	# note was found
	return 'none'
