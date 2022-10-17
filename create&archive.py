# Create and Arichve
# Not currently being used as part of project.
# Provides capability to create new member and archive a member. 
# Date of Last Change
# 10/17/2022 - P.Ireland - added comment headers

from tarfile import NUL
from typing import OrderedDict
import API
import urllib.parse
import json
import csv

from export import print_contact_info

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


class contact():
    def __init__(self, id, firstName, lastName, email):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

# CREATE A CONTACT
def create_contact(email, name):
    data = {
        'Email': email,
        'FirstName': name}
    return api.execute_request(contactsUrl, api_request_object=data, method='POST')


# ADD A CONTACT
def add_contact(contact_id):
    data = {
        'Id': contact_id,
        'FieldValues': [
            {
                'FieldName': 'Member',
                'Value': 'true'}]
    }
    return api.execute_request(contactsUrl + str(contact_id), api_request_object=data, method='PUT')

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




## CREATE NEW CONTACT ## (works)
new_contact = create_contact('some_email1_JaneDoe@invaliddomain.org', 'Jane Doe')

#adds test contact from above to db
#Note: if run code multiple times, will throw error because email already in use
# will take care of this in future
add_new_contact = add_contact(new_contact.Id)
print("New contact added: Info below")


## FINALLY ARCHIVE IT ##
#archived_contact = archive_contact(new_copntact.Id)
#print_contact_info(archived_contact)