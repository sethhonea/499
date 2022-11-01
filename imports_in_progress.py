import API
import csv

# How to obtain application credentials: https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication
# params in line below are API key and clinet secret
api = API.WaApiClient("gc7fl5u5rt", "t3haoauwug3tm91h4cu44m6odi6skr")
api.authenticate_with_contact_credentials("sch0010@uah.edu", "backend")
accounts = api.execute_request("/v2/accounts")
account = accounts[0]

print(account.PrimaryDomainName)

## URLS to retrieve data
contactsUrl = next(res for res in account.Resources if res.Name == 'Contacts').Url
eventsUrl = next(res for res in account.Resources if res.Name == 'Events').Url
invoicesUrl = next(res for res in account.Resources if res.Name == 'Invoices').Url
donationsUrl = next(res for res in account.Resources if res.Name == 'Donations').Url


#Receive same Error 405: Method Not Allowed that receive with import_event()
def import_invoice():
    # fieldnames = ['Id', 'Value', 'DocumentDate', 'Contact', 'CreatedDate', 'CreatedBy', 'IsPaid'] <-- from export.py
    data = {
        'Id': 999999,
        'Value': 5.0,
        'DocumentDate': '2022-09-30T03:06:36+00:00',
        'Contact': "{""Id"": 66020498, ""Url"": ""https://api.wildapricot.org/v2/accounts/422750/Contacts/66020498"", ""Name"": ""Honea, Seth""}",
        'CreatedDate': '2022-09-27T03:06:36',
        'CreatedBy' : "{""Id"": 66133802, ""Url"": ""https://api.wildapricot.org/v2/accounts/422750/Contacts/66133802""}",
        'IsPaid' : False

    }

    return api.execute_request(invoicesUrl, api_request_object=data, method='POST')



#Receive same Error 405: Method Not Allowed that receive with import_event() and import_invoice()
def import_donation():
    # fieldnames = ['Value', 'DonationDate', 'FirstName', 'LastName', 'PublicComment', 'Organization']
    data = {
        'Value' : 25.00,
        'DonationDate' : '2022-09-30T03:06:36+00:00',
        'FirstName' : 'Payton',
        'LastName' : 'Ireland',
        'PublicComment' : '',
        'Organization' : ''
    }

    return api.execute_request(donationsUrl, api_request_object=data, method='POST')