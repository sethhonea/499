import API

# How to obtain application credentials: https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication
# params in line below are API key and clinet secret
api = API.WaApiClient("gc7fl5u5rt", "t3haoauwug3tm91h4cu44m6odi6skr")
api.authenticate_with_contact_credentials("sch0010@uah.edu", "backend")
accounts = api.execute_request("/v2/accounts")
account = accounts[0]

print(account.PrimaryDomainName)

## URLS to retrieve data

## URLS to retrieve data
eventsUrl = next(res for res in account.Resources if res.Name == 'Events').Url


#IMPORT SINGLE Document
def import_document():

    #replace text file with any text file wanting to upload
    with open("Test_Document_To_Upload.txt", 'r') as file:
        text = file.readlines()
    
    #reaplce Name with document name, and dates as needed. 
    data = {
        #'Id' : event.Id,   cannot provide an Id
        'Name' : 'DDD Draft Document Upload Test',
        'StartDate' : '2022-11-07',
        'StartTimeSpecified' : False,
        'EndDate': '2022-11-08',
        'EndTimeSpecified' : False,
        'Location' : 'Test Upload',
        'RegistrationEnabled' : True,
        'Tags' : text
        }

    return api.execute_request(eventsUrl, api_request_object=data, method='POST')



#calling function to import the document
import_document()