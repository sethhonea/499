#__author__ = 'dsmirnov@wildapricot.com'

import API
import urllib.parse
import json
import csv

# GET 10 ACTIVE MEMBERS
def get_10_active_members():
    params = {'$filter': 'member eq true',
              '$top': '10',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts

#GET 1 Active Member 
def get_1_active_member():
    params = {'$filter': 'member eq true',
              '$top': '1',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts

#PRINT CONTACT INFO
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


#EXPORT CONTACT INFO
def export_contact_info(contacts):
   
    with open('exported_contact_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['ID', 'First Name', 'Last Name', 'Email']
        thewriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
        thewriter.writeheader()
        for contact in contacts:
            thewriter.writerow({'ID':contact.Id, 'First Name':contact.FirstName, 
            'Last Name':contact.LastName, 'Email':contact.Email})


# CREATE A CONTACT
def create_contact(email, name):
    data = {
        'Email': email,
        'FirstName': name}
    return api.execute_request(contactsUrl, api_request_object=data, method='POST')

# ARCHIVE A CONTACT
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

print(account.PrimaryDomainName)

contactsUrl = next(res for res in account.Resources if res.Name == 'Contacts').Url

# get top 10 active members and print their details
#contacts = get_10_active_members()
#for contact in contacts:
#    print_contact_info(contact)

## export contact info of members
contacts = get_10_active_members()
export_contact_info(contacts)

# # create new contact
# new_copntact = create_contact('some_email1@invaliddomain.org', 'John Doe')
# print_contact_info(new_copntact)

# # finally archive it
# archived_contact = archive_contact(new_copntact.Id)
# print_contact_info(archived_contact)
