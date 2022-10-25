#__author__ = 'dsmirnov@wildapricot.com'

import API
import urllib.parse
import json


def get_10_active_members():
    params = {'$filter': 'member eq true',
              '$top': '10',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts


def print_contact_info(contact):
    print('Contact details for ' + contact.DisplayName + ', ' + contact.Email)
    print('Main info:')
    print('\tID:' + str(contact.Id))
    print('\tFirst name:' + contact.FirstName)
    print('\tLast name:' + contact.LastName)
    print('\tEmail:' + contact.Email)
    print('\tAll contact fields:')
    for field in contact.FieldValues:
        if field.Value is not None:
            print('\t\t' + field.FieldName + ':' + repr(field.Value))


def create_contact(email, name):
    data = {
        'Email': email,
        'FirstName': name}
    return api.execute_request(contactsUrl, api_request_object=data, method='POST')


def archive_contact(contact_id):
    data = {
        'Id': contact_id,
        'FieldValues': [
            {
                'FieldName': 'Archived',
                'Value': 'true'}]
    }
    return api.execute_request(contactsUrl + str(contact_id), api_request_object=data, method='PUT')

# How to obtain application credentials: https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication
# params in line below are API key and clinet secret
api = API.WaApiClient("gc7fl5u5rt", "t3haoauwug3tm91h4cu44m6odi6skr")
api.authenticate_with_contact_credentials("sch0010@uah.edu", "backend")
accounts = api.execute_request("/v2/accounts")
account = accounts[0]

#print(account.toString())
#print(account.PrimaryDomainName)
print(account.Id)
#for acc in account.Resources:
#    print(acc.Name)

contactsUrl = next(res for res in account.Resources if res.Name == 'Contacts').Url

memberGroupsUrl = next(res for res in account.Resources if res.Name == 'Member groups').Url

membershipLevelsUrl = next(res for res in account.Resources if res.Name == 'Membership levels').Url

contactFieldsUrl = next(res for res in account.Resources if res.Name == 'Contact fields').Url

#contactsUrl = next(res for res in account.Resources if res.Name == 'Contacts').Url
eventsUrl = next(res for res in account.Resources if res.Name == 'Events').Url
invoicesUrl = next(res for res in account.Resources if res.Name == 'Invoices').Url
donationsUrl = next(res for res in account.Resources if res.Name == 'Donations').Url   
paymentsUrl = next(res for res in account.Resources if res.Name == 'Payments').Url 
urlDict = {'Contacts' : contactsUrl,'Member Groups':memberGroupsUrl,'Membership levels':membershipLevelsUrl,'Contact fields':contactFieldsUrl}

# get top 10 active members and print their details
#contacts = get_10_active_members()
#for contact in contacts:
#    print_contact_info(contact)

# # create new contact
# new_copntact = create_contact('some_email1@invaliddomain.org', 'John Doe')
# print_contact_info(new_copntact)

# # finally archive it
# archived_contact = archive_contact(new_copntact.Id)
# print_contact_info(archived_contact)


 # GET EVENTS
def get_events():
    params = {'$filter': 'RegistrationEnabled eq true',
              '$async': 'false'}
    request_url = eventsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Events

 # GET EVENTS  --> not currently working
def get_upcoming_events():
    params = {'$filter': 'RegistrationEnabled eq true',
            '$filter': 'isUpcoming eq true',
              '$async': 'false'}
    request_url = eventsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Events   

def get_donations():
   params = {'EndDate': '2022-10-24'}
   request_url = donationsUrl + '?' + urllib.parse.urlencode(params)
   print(request_url)
   return api.execute_request(request_url)

#GET Attachments   //// not currently working 9/11/22
'''def get_attachments():
   params = {'size': 'attachment eq true',
               'atBase64': 'false'}
   request_url = attachmentsUrl + '?' + urllib.parse.urlencode(params)
   print(request_url)
   return api.execute_request(request_url).Attachments'''

#data = get_donations()
#print(type(data))
#for i in data:
#    print(i.toString())

# Error was for new id and date time 
# def import_event():
#    #fieldnames = ['Id', 'Name', 'StartDate', 'EndDate', 'Location'] <-- from export.py
#    data = {
#        'Name': "Test Event Improt", 
#        'StartDate': '2022-12-10T00:00:00+01:00',
#        'EndDate': '2022-12-20T00:00:00+01:00', 
#        'Location': 'Huntsville-Test',
#        "RegistrationEnabled": 'true',
#
#    }
#    return api.execute_request(eventsUrl, api_request_object=data, method='POST')

#import_event()

# error was for new id & OrderDetails & IsPaid
#Receive same Error 405: Method Not Allowed that receive with import_event()
def import_invoice():
    # fieldnames = ['Id', 'Value', 'DocumentDate', 'Contact', 'CreatedDate', 'CreatedBy', 'IsPaid'] <-- from export.py
    data = {
        'Value': 5.0,
        'DocumentDate': '2022-09-30T03:06:36+00:00',
        'Contact': {'Id': 66133802},
        'CreatedDate': '2022-09-27T03:06:36',
        'CreatedBy' : {'Id': 66226364},
        'DocumentNumber': 1000,
        'OrderType':'Undefined',
        'OrderDetails':[{
            'Value':5.0,
            'OrderDetailType':'Unspecified',
            'Notes':'Import From Api',
            'Taxes':{
                'Amount':0,
                'CalculatedTax1': 0,
                'CalculatedTax2': 0,
                'NetAmount': 0,
                'RoundedAmount': 0,
                'Tax1': {
                'Name': 'string',
                'PublicId': 'string',
                'Rate': 0
                },
                'Tax2': {
                'Name': 'string',
                'PublicId': 'string',
                'Rate': 0
                }
            }}],
        'IsPaid' : False,
        'Memo':'ok',
        'PublicMemo':'Nook'

    }

    return api.execute_request(invoicesUrl, api_request_object=data, method='POST')

# api call is totally wrong
def import_donation():
    # fieldnames = ['Value', 'DonationDate', 'FirstName', 'LastName', 'PublicComment', 'Organization']
    data = {
        "Value": 10.0,
        "DocumentDate": "2022-10-24",
        
        "Contact": {
            "Id": 66133802,
            "Url": "Nothing"
        },
        "Comment": "Checking Api Functionality",
        "PublicComment": "Checking API",
        "PaymentType": "DonationPayment"
    }

    return api.execute_request(paymentsUrl, api_request_object=data, method='POST')

import_donation()