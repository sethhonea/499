#__author__ = 'dsmirnov@wildapricot.com'

from tarfile import NUL
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

# GET 1 Active Member 
def get_1_active_member():
    params = {'$filter': 'member eq true',
              '$top': '1',
              '$async': 'false',
              'showSectionDividers': 'true'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts

# GET Custom Fields 
def get_custom_fields():
    params = {'showSectionDividers': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts

# GET Attachments   //// not currently working 9/11/22
#def get_attachments():
#    params = {'size': 'attachment eq true',
#                'atBase64': 'false'}
#    request_url = attachmentsUrl + '?' + urllib.parse.urlencode(params)
#    print(request_url)
#    return api.execute_request(request_url).Attachments

# PRINT CONTACT INFO
def print_contact_info(contact):
    print('Contact details for.... ' + contact.DisplayName)
    print('Main info: (values we can specifically grab from a contact)')
    print('\tID: ' + str(contact.Id))
    print('\tFirst name: ' + contact.FirstName)
    print('\tLast name: ' + contact.LastName)
    print('\tEmail: ' + contact.Email)
    print('\tMembership Enabled: ' + str(contact.MembershipEnabled))
    print('\tStatus: ' + contact.Status)
    print('\tTerms of Use Accepted: ' + str(contact.TermsOfUseAccepted))
    if(contact.Organization == ""):
        contact.Organization = "NA"
    print('\tOrganization: ' + contact.Organization)
    print('\tProfile Last Updated: ' + contact.ProfileLastUpdated)
    print('\tIs Account Administrator: ' + str(contact.IsAccountAdministrator))
    
    print('--------------------------------------')
    print('\tAll contact fields where value is NOT "none":')
    for field in contact.FieldValues:
        if field.Value is not None:
            print('\t\t' + field.FieldName + ': ' + repr(field.Value))
     
    print('--------------------------------------')
    print('\tAll contact fields where value IS "none":')
    for field in contact.FieldValues:
        if field.Value is None:
            print('\t\t' + field.FieldName + ': ' + repr(field.Value))

    print(' ** End of Print Contact Info **')
# end print_contact_info()

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
#attachmentsUrl = next(res for res in account.Resources if res.Name == 'Attachments').Url

## get top 10 active members and print their details
contacts = get_10_active_members()
for contact in contacts:
    print_contact_info(contact)

## get top 1 active member and print their details (made for testing)
#contacts = get_1_active_member()
#for contact in contacts:
#    print_contact_info(contact)

#contacts_custom = get_custom_fields()

## trying to get attachments
#attachments = get_attachments()
#for attachment in attachments:
#    print_contact_info(contact)

## EXPORT contact info of members
#contacts = get_10_active_members()
#export_contact_info(contacts)

## create new contact
# new_copntact = create_contact('some_email1@invaliddomain.org', 'John Doe')
# print_contact_info(new_copntact)

## finally archive it
# archived_contact = archive_contact(new_copntact.Id)
# print_contact_info(archived_contact)
