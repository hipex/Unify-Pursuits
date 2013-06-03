import passwords

from evernote.api.client import EvernoteClient
import evernote.edam.notestore.ttypes as NoteStoreTypes

authToken=passwords.evernoteAuthToken
client = EvernoteClient(token=authToken, sandbox=True)
note_store = client.get_note_store()
