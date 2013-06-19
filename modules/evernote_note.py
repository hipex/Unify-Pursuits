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
	
def getCalendarItems(mdb, parameter):
 	# return only notes with reminder / todo date
	global evernoteInit
	global datetime
	
	noteinfo = evernoteInit.note_store.getNote(evernoteInit.authToken, parameter, True, False, False, False)
	if noteinfo.attributes.reminderTime != None:
		noteTimestamp = noteinfo.attributes.reminderTime # given in miliseconds
		
		noteDatetime = datetime.fromtimestamp(noteTimestamp/1000).strftime('%Y-%m-%dT%H:%M:%S+01:00')
		
		item = {"start":noteDatetime, "end":noteDatetime, "summary":noteinfo.title}

	return [item]

	
def add(parentParameter):
	global service
	
	if parentParameter == False:
		# choose notebook manually
		pass
		
	else:
		evernoteNotebook = parentParameter
	
	parameter = raw_input("choose parameter: ")
	return [parameter]

def check(parameter):
	global evernoteInit
	
	try:
		evernoteInit.note_store.getNote(evernoteInit.authToken, parameter, False, False, False, False)
	except (evernoteInit.errorTypes.EDAMNotFoundException, evernoteInit.errorTypes.EDAMUserException) as e:
		# note note found
		return True
	
	# note was found
	return False
