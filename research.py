import API
import urllib.parse

#
api = API.WaApiClient("gc7fl5u5rt", "t3haoauwug3tm91h4cu44m6odi6skr")
# enter Research admin credentials below
api.authenticate_with_contact_credentials("sch0010@uah.edu", "backend")
accounts = api.execute_request("/v2/accounts")
account = accounts[0]


## other URLS
contactsUrl = next(res for res in account.Resources if res.Name == 'Contacts').Url
eventsUrl = next(res for res in account.Resources if res.Name == 'Events').Url
invoicesUrl = next(res for res in account.Resources if res.Name == 'Invoices').Url
donationsUrl = next(res for res in account.Resources if res.Name == 'Donations').Url  

#possibly URL for Attachments??
attachmentsUrl = next(res for res in account.Resources if res.Name == 'Attachments').Url


def import_research():
    #some unique id
    attachment_id = 1234
    #not entirely sure where you'll put the actual file to upload??
    #maybe take another look at swaggerhub API stuff
    data = {
        'Id': attachment_id,
        #Fill out right size of fields below
        'Name' : 'InsertAttachementName',
        'Size': 'InsertAttachmentSize??', #might could leave off?
        'CreatedDate': 'InsertDate' 
    }
    return api.execute_request(attachmentsUrl + str(attachment_id), api_request_object=data, method='PUT')   

import_research()