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
	
	#for note in evernoteInit.note_store:
	#	if note.guid == parameter:
	return 'none'
	
	# note not found in online list
	return itemID
