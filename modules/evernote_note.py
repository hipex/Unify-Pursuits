import evernoteInit

def show(parameter):
	global evernoteInit

	note = evernoteInit.note_store.getNote(evernoteInit.authToken, parameter, True, False, False, False)
	print "titel: "+note.title
	print note.content
	
	
def add():
	global service
	
	parameter = raw_input("choose parameter: ")
	return [parameter]

def update(con, parameter, parentID):
	return False
