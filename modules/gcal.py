import passwords

import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
	
# Contact to client
FLOW = OAuth2WebServerFlow(
	client_id=passwords.client_id,
	client_secret=passwords.client_secret,
	scope='https://www.googleapis.com/auth/calendar',
	user_agent='unify/1')

# create storage if offline
storage = Storage('calendar.dat')
credentials = storage.get()	
if credentials is None or credentials.invalid == True:
	credentials = run(FLOW, storage)

# authorize
http = httplib2.Http()
http = credentials.authorize(http)
service = build(serviceName='calendar', version='v3', http=http,
	   developerKey=passwords.developerKey)
			   
