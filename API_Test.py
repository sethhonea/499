#__author__ = 'dsmirnov@wildapricot.com'

from tarfile import NUL
from typing import OrderedDict
import API
import urllib.parse
import json
import csv


class contact():
    def __init__(self, id, firstName, lastName, email):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

# GET 10 ACTIVE MEMBERS
def get_10_active_members():
    params = {'$filter': 'archived eq false',
              '$top': '10',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts

def get_archived_members():
    params = {'$filter': 'archived eq true ',
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

 # GET 1 Event
def get_events():
    params = {'$filter': 'RegistrationEnabled eq true',
              '$top': '1',
              '$async': 'false'}
    request_url = eventsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Events      

# GET Invoices
def get_invoices():
    params = {'$unpaidOnly': 'true',
              '$top': '1'}
    request_url = invoicesUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url)

# GET Donations
def get_donations():
    params = {'$top': '1'}
    request_url = donationsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url)


# GET Attachments   //// not currently working 9/11/22
#def get_attachments():
#    params = {'size': 'attachment eq true',
#                'atBase64': 'false'}
#    request_url = attachmentsUrl + '?' + urllib.parse.urlencode(params)
#    print(request_url)
#    return api.execute_request(request_url).Attachments

# PRINT DONATION INFO
def print_donation_info(payment):
    print('Donation Value: ' + str(payment.Value))
    print('Donation Date: ' + str(payment.DonationDate))
    print('Donation made by: ' + str(payment.FirstName) + ' ' + str(payment.LastName))
    if(payment.PublicComment == ""):
        payment.PublicComment = "NA"
    print('Donation Comments: ' + str(payment.PublicComment))
    if(payment.Organization == ""):
        payment.Organization = "NA"
    print('Donation Organization: ' + str(payment.Organization))

# PRINT INVOICE INFO
def print_invoice_info(invoice):
    print('Invoice ID: ' + str(invoice.Id))
    print('Invoice Value: ' + str(invoice.Value))
    print('Invoice Document Date: ' + str(invoice.DocumentDate))
    print('Invoice Contact: ' + str(invoice.Contact))
    print('Invoice Created Date: ' + str(invoice.CreatedDate))
    print('Invoice Created By: ' + str(invoice.CreatedBy))
    print('Invoice Paid: ' + str(invoice.IsPaid))
    

# PRINT EVENT INFO
def print_event_info(event):
    print('Event ID: ' + str(event.Id))
    print('Event Name: ' + str(event.Name))
    print('Event Start Date: ' + str(event.StartDate))
    print('Event End Date: ' + str(event.EndDate))
    print('Event Location: ' + str(event.Location))
    

# PRINT CONTACT INFO
def print_contact_info(contact):
    print('')
    print('\t\t******** Contact details for ' + contact.DisplayName + '***********')
    print('Main info: \t (values we can specifically grab from a contact)')
    print('\tID: ' + str(contact.Id))
    print('\tURL: ' + str(contact.Url))
    print('\tFirst name: ' + contact.FirstName)
    print('\tLast name: ' + contact.LastName)
    if(contact.Organization == ""):
        contact.Organization = "NA"
    print('\tOrganization: ' + contact.Organization)
    print('\tEmail: ' + contact.Email)
    print('\tDisplayName ' + contact.DisplayName)
    print('\tProfile Last Updated: ' + contact.ProfileLastUpdated)
    print('\tMembership Level: ' + str(contact.MembershipLevel))
    print('\tMembership Enabled: ' + str(contact.MembershipEnabled))
    print('\tStatus: ' + contact.Status)
    print('\tIs Account Administrator: ' + str(contact.IsAccountAdministrator))
    print('\tTerms of Use Accepted: ' + str(contact.TermsOfUseAccepted))
    ## for some reason we have to pop these get the values
    ## may need to do further research on this for report
    #print('\tField Values: ')
    #print('\t\tArchived: ' + str(contact.FieldValues.pop(0)))
    #print('\t\tDonor: ' + str(contact.FieldValues.pop(0)))
    #print('\t\tEvent Registrant: ' + str(contact.FieldValues.pop(0)))
    #print('\t\tMember ' + str(contact.FieldValues.pop(0)))
    #print('\t\tSuspended Member ' + str(contact.FieldValues.pop(0)))
    #print('\t\tEvent Announcements ' + str(contact.FieldValues.pop(0)))
    #print('\t\tMember emails and newsletters ' + str(contact.FieldValues.pop(0)))
    #print('\t\tEmail delivery disabled ' + str(contact.FieldValues.pop(0)))
    #print('\t\tReceiving emails disabled ' + str(contact.FieldValues.pop(0)))
    
    print('--------------------------------------')
    print('\tAll contact fields where value is NOT "none":')
    counter =1
    for field in contact.FieldValues:
        if field.Value is not None:
            print('\t\t' + str(counter) + ' ' + field.FieldName + ': ' + repr(field.Value))
        counter+=1
            
    print('--------------------------------------')
    print('\tAll contact fields where value IS "none":')
    for field in contact.FieldValues:
        if field.Value is None:
            print('\t\t' + field.FieldName + ': ' + repr(field.Value))

    print(' ** End of Print Contact Info **')
    print('-----------------------------------------------------------------------------------------------')
# end "print_contact_info()"

# SET Contact Field Values
c_field_values = []
def set_contact_field_values(contact):
    for field in contact.FieldValues:
        #if field.Value is None or not None:
        c_field_values.append(str(contact.FieldValues.pop(0)))

# GET Contact Field Values            
def get_contact_field_values():
    counter = 1
    for field in c_field_values:
        print(str(counter) + ' '+ field)
        counter+=1
    
    return c_field_values

# EXPORT CONTACT INFO
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


# IMPORT A CONTACT
def import_contact(contact):    
    data = {
        'Email': contact.email,
        'FirstName': contact.firstName,
        'LastName' : contact.lastName,
        'ID' : contact.id,
        
        }
    return api.execute_request(contactsUrl, api_request_object=data, method='POST')


# IMPORT ALL CONTACT DATA    
def import_data():
    with open('test_exported_contact_info.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            id = row['ID']
            firstName = row['First Name']
            lastName = row['Last Name']
            email = row['Email']
            newContact = contact(id, firstName, lastName, email)
            print(newContact.id, newContact.firstName, newContact.lastName, newContact.email)
            try:
                import_contact(newContact)
                print(f"Imported contact with email {newContact.email} to database.")
            except:
                print(f"Contact with email {newContact.email} already exists.")

def print_archive_member(member):                
    print('\tID: ' + str(member.Id))
    print('\tURL: ' + str(member.Url))
    print('\tFirst name: ' + member.FirstName)
    print('\tLast name: ' + member.LastName)
    print('\tArchived: ' + str(member.FieldValues.pop(0).Value))

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

## GET TOP 10 ACTIVE MEMBERS and print their details ## (works)
#contacts = get_10_active_members()
#for contact in contacts:
#    print_contact_info(contact)

## GET 1 ACTIVE MEMBER (made for testing) ## (works)
#contacts = get_1_active_member()
#for contact in contacts:
#    print_contact_info(contact)
#    set_contact_field_values(contact)

## GET EXTRA CONTACT FIELD VALUES ## (works?)
#get_contact_field_values()

## GET ATTACHMENTS (not working) ## (doesnt work)
#attachments = get_attachments()
#for attachment in attachments:
#    print_contact_info(contact)

## EXPORT CONTACT INFO ## (works)
#contacts = get_10_active_members()
#export_contact_info(contacts)

## CREATE NEW CONTACT ##
#new_contact = create_contact('some_email1@invaliddomain.org', 'John Doe')

#adds test contact from above to db
#Note: if run code multiple times, will throw error because email already in use
# will take care of this in future
#add_new_contact = add_contact(new_contact.Id)
#print("New contact added: Info below")


## Next: pull info from exported_contact_info.csv and import it into database
# import_data()

## FINALLY ARCHIVE IT ##
# archived_contact = archive_contact(new_copntact.Id)
# print_contact_info(archived_contact)

## GET AND PRINT EVENTS ## (works)
events = get_events()
for event in events:
    print('** BEGIN EVENT INFO **')
    print_event_info(event)
    print('** END EVENT INFO **')

## GET AND PRINT INVOICES ## (works)
invoices = get_invoices()
for invoice in invoices:
    print('** BEGIN INVOICE INFO **')
    print_invoice_info(invoice)
    print('** END INVOICE INFO **')

## GET AND PRINT DONATIONS ## (works)
donations = get_donations()
for donation in donations:
    print('** BEGIN DONATION INFO **')
    print_donation_info(donation)
    print('** END DONATION INFO **')

## GET AND PRINT ARCHIVED MEMBERS 
archived_members = get_archived_members()
for member in archived_members:
    print('** BEGIN ARCHIVED MEMBER INFO**')   
    print_archive_member(member)
    print('** END ARCHIVED MEMBER INFO **')
