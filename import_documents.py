# This script provides the ability to import documents into the database. 
# For this example, the a Database Design Document (DDD) Draft was 
# uploaded (DDD_Draft_Upload.txt). Any plain text document could be substituted
# by changing the filename along with the event name which is being used as the
# document title. These documents are uploaded as an event with the text 
# located in the Tags portion of the event. This is due to the limited
# capabilities of WildApricot. 

# Created by: Backend Team (Payton Ireland, Seth Honea, Juliet Awoyale)

import API

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

## URLS to retrieve data
eventsUrl = next(res for res in account.Resources if res.Name == 'Events').Url


#IMPORT SINGLE Document
def import_document(filename, name_event):

    #************************************
    # CHANGE DETAILS BELOW: file name with extension of document wanting to upload
    #************************************
    with open(filename, 'r') as file:
        text = file.readlines()
    #************************************
    # CHANGE DETAILS BELOW: Name (may change start/end date if needed)
    # The Name for the document provided below will be needed in export_documents.py
    #************************************
    data = {
        'Name' : name_event,
        'StartDate' : '2022-12-10',
        'StartTimeSpecified' : False,
        'EndDate': '2022-12-10',
        'EndTimeSpecified' : False,
        'Location' : 'Upload',
        'RegistrationEnabled' : True,
        'Tags' : text
        }

    return api.execute_request(eventsUrl, api_request_object=data, method='POST')



#calling function to import the document into the database
import_document("DDD_Draft_Upload.txt", "DDD Draft")
