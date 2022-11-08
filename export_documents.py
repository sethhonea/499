
from tarfile import NUL
import API
import urllib.parse
import csv




# How to obtain application credentials: https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication
# params in line below are API key and clinet secret
api = API.WaApiClient("gc7fl5u5rt", "t3haoauwug3tm91h4cu44m6odi6skr")

#************************************
# CHANGE CREDENTIALS BELOW username, password
#************************************
api.authenticate_with_contact_credentials("sch0010@uah.edu", "backend")
accounts = api.execute_request("/v2/accounts")
account = accounts[0]

print(account.PrimaryDomainName)

## URLS to retrieve data
eventsUrl = next(res for res in account.Resources if res.Name == 'Events').Url
   

 # GET EVENTS - retrieves all events with registration enabled
def get_events():
    params = {'$filter': 'RegistrationEnabled eq true',
              '$async': 'false'}
    request_url = eventsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Events      
      


#DEFINING ALL EXPORT FUNCTIONS BELOW
#----------------------------------------------------------------------------------------------------

# EXPORT EVENT INFO - write each event in events to csv file as a row
def export_documents(events):
    with open('exported_event_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['Id', 
                    'Name', 
                    'Type',
                    'StartDate', 
                    'StartTimeSpecified',
                    'EndDate', 
                    'EndTimeSpecified',
                    'Location',
                    'RegistrationEnabled',
                    'HasEnabledRegistrationTypes',
                    'AccessLevel',
                    'Tags'
                    ]
        thewriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
        thewriter.writeheader()
        for event in events:
            ## *****************************
            # UPDATE below with your doucment title/name used in import_documents.py -- MUST MATCH EXACTLY
            ## *****************************
            if event.Name == "DDD Draft Document Upload Test":
                export_document_event(event)
                continue
            


# EXPORT DOCUMENT EVENT
def export_document_event(doc_event):
    #use provided document name as the filename
    filename = doc_event.Name + '.txt'
    
    #open the file and write all of the document located in Tags field
    with open(filename, 'w') as file:
        text = doc_event.Tags
        #Tags is list of strings, so have to write for each string in the text list
        for string in text:
            file.write(string)
        
    

## EXPORT EVENTS THAT ARE DOCUMENTS
events = get_events()
export_documents(events)
