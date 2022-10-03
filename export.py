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

#DEFINING ALL FUNCTIONS TO RETRIEVE DATA FROM DATABASE
# ----------------------------------------------------------------------------------------------        

# GET ACTIVE MEMBERS
def get_active_members():
    params = {'$filter': 'archived eq false',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts

# GET ARCHIVED MEMBERS
def get_archived_members():
    params = {'$filter': 'archived eq true ',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts    

 # GET EVENTS
def get_events():
    params = {'$filter': 'RegistrationEnabled eq true',
              '$async': 'false'}
    request_url = eventsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Events      

 # GET EVENTS  --> not currently working
# def get_archived_events():
#     params = {'$filter': 'RegistrationEnabled eq true',
#             '$filter': 'archived eq true',
#               '$async': 'false'}
#     request_url = eventsUrl + '?' + urllib.parse.urlencode(params)
#     print(request_url)
#     return api.execute_request(request_url).Events        

# GET INVOICES
def get_invoices():
    params = {'$unpaidOnly': 'true',
              '$top': '100'}
    request_url = invoicesUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url)

# GET DONATIONS --- IN OTHER FUNCTIONS WE HAVE BEEN ABLE TO REMOVE THE 'TOP' PARAM TO RETRIEVE ALL, 
#                   HOW WILL THAT WORK HERE?
def get_donations():
    params = {'$top': '100'}
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


# DEFINING ALL PRINT TO TERMINAL FUNCTIONS BELOW
#---------------------------------------------------------------------------------------------------

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
    print('Event type:' + str(event.EventType))
    

# PRINT CONTACT INFO
def print_contact_info(contact):
    try:
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
        print('\tField Values: ')
        print('\t\tArchived: ' + str(contact.FieldValues.pop(0).Value))
        print('\t\tDonor: ' + str(contact.FieldValues.pop(0).Value))
        print('\t\tEvent Registrant: ' + str(contact.FieldValues.pop(0).Value))
        print('\t\tMember ' + str(contact.FieldValues.pop(0).Value))
        print('\t\tSuspended Member ' + str(contact.FieldValues.pop(0).Value))
        print('\t\tEvent Announcements ' + str(contact.FieldValues.pop(0).Value))
        print('\t\tMember emails and newsletters ' + str(contact.FieldValues.pop(0).Value))
        print('\t\tEmail delivery disabled ' + str(contact.FieldValues.pop(0).Value))
        print('\t\tReceiving emails disabled ' + str(contact.FieldValues.pop(0).Value))
        
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
    except:
        print("An error occured printing fields for ", contact.DisplayName)


def print_archive_member(member):                
    print('\tID: ' + str(member.Id))
    print('\tURL: ' + str(member.Url))
    print('\tFirst name: ' + member.FirstName)
    print('\tLast name: ' + member.LastName)
    print('\tArchived: ' + str(member.FieldValues.pop(0).Value))

#-------------------------------------------------------------------------------------------------------------------------

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

#DEFINING ALL EXPORT FUNCTIONS BELOW
#----------------------------------------------------------------------------------------------------

# EXPORT CONTACT INFO
def export_contact_info(contacts, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['DisplayName', 'Id', 'Url', 'FirstName', 'LastName', 'Organization',
        'Email', 'ProfileLastUpdated', 'MembershipLevel', 'Status', 'IsAccountAdministrator',
        'TermsOfUseAccepted', 'Archived', 'Donor', 'Event registrant', 'Member', 'Suspended member',
        'Event announcements', 'Member emails and newsletters', 'Email delivery disabled', 
        'Receiving emails disabled', 
        # # from all contact fields where value is NOT none
        # 'Balance', 'Total donated', 'Profile last updated',
        # 'Profile last updated by', 'Creation date', 'Last login date', 'Administrator role',
        # 'Notes', 'Renew now', '(Office Use)', 'e-Mail', 'Cell Phone', 'Member since', 'Renewal due',
        # 'Membership level ID', 'Access to profile by others', 'Level last changed', 
        # 'Membership status', 'Membership enabled', 'Privacy Policy Consent', 'Code of Conduct Consent',
        # 'Addess in Paris / ile de France', 'City', 'Postal code in FRANCE', '2nd email address',
        # 'Hometown', 'Age Range', 'Approximate length of stay in Paris', 'Percentage of time will you physically be in Paris',
        # 'Areas in which I am willing to volunteer with AWG.', 'Working in France?', 'Group participation',
        # 'Preferred time for activities/meetings', "I'm interested in:",
        # #from all contact fields where value IS none
        # 'Registered for specific event', 'Member role', 'Renewal date last changed', 'Bundle ID',
        # 'Country', 'Citizenship', 'Dual Citizenship, if applicable', 'Birth Month', 'Arrival Date In Paris',
        # 'How did you hear about AWG?', 'Are you fluent in French ?', 'AWG Bag received', 'Friends & Neighbors Group'
        ]
        thewriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
        thewriter.writeheader()
        for contact in contacts:
            try:
                thewriter.writerow({
                    'DisplayName': contact.DisplayName , 
                    'Id': contact.Id, 
                    'Url': contact.Url, 
                    'FirstName': contact.FirstName, 
                    'LastName': contact.LastName, 
                    'Organization': contact.Organization,
                    'Email': contact.Email,
                    'ProfileLastUpdated': contact.ProfileLastUpdated, 
                    'MembershipLevel': contact.MembershipLevel, 
                    'Status': contact.Status, 
                    'IsAccountAdministrator': contact.IsAccountAdministrator,
                    'TermsOfUseAccepted': contact.TermsOfUseAccepted, 
                    'Archived': str(contact.FieldValues.pop(0).Value), 
                    'Donor': str(contact.FieldValues.pop(0).Value), 
                    'Event registrant': str(contact.FieldValues.pop(0).Value), 
                    'Member': str(contact.FieldValues.pop(0).Value), 
                    'Suspended member': str(contact.FieldValues.pop(0).Value),
                    'Event announcements': str(contact.FieldValues.pop(0).Value), 
                    'Member emails and newsletters': str(contact.FieldValues.pop(0).Value), 
                    'Email delivery disabled': str(contact.FieldValues.pop(0).Value), 
                    'Receiving emails disabled': str(contact.FieldValues.pop(0).Value),
                    ## figure out how to add the values for rows where value IS none and value is NOT none
                })
            except: 
                print("Unable to export information for ", contact.DisplayName)

def export_event_info(events):
    with open('exported_event_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['Id', 'Name', 'StartDate', 'EndDate', 'Location']
        thewriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
        thewriter.writeheader()
        for event in events:
            thewriter.writerow({
                'Id': event.Id, 
                'Name': event.Name, 
                'StartDate': event.StartDate, 
                'EndDate': event.EndDate, 
                'Location': event.Location
            })

def export_invoice_info(invoices):
    with open('exported_invoice_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['Id', 'Value', 'DocumentDate', 'Contact', 
        'CreatedDate', 'CreatedBy', 'IsPaid']
        thewriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
        thewriter.writeheader()
        for invoice in invoices:
            thewriter.writerow({
                'Id': invoice.Id, 
                'Value': invoice.Value, 
                'DocumentDate': invoice.DocumentDate, 
                'Contact': invoice.Contact, 
                'CreatedDate': invoice.CreatedDate, 
                'CreatedBy': invoice.CreatedBy, 
                'IsPaid': invoice.IsPaid
            })

def export_donation_info(donations):
    with open('exported_donation_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['Value', 'DonationDate', 'FirstName', 'LastName',
        'PublicComment', 'Organization']
        thewriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
        thewriter.writeheader()
        for donation in donations:
            thewriter.writerow({
                'Value': donation.Value, 
                'DonationDate': donation.DonationDate, 
                'FirstName': donation.FirstName, 
                'LastName': donation.LastName,
                'PublicComment': donation.PublicComment, 
                'Organization': donation.Organization
            })

# CALLING FUNCTIONS TO RETRIEVE DATA, PRINT DATA, AND/OR EXPORT DATA
#---------------------------------------------------------------------------------------------------------

## GET ALL ACTIVE MEMBERS & PRINT THEIR DETAILS ## (works)
#contacts = get_active_members()
#print("***BEGIN CONTACT PRINT***")
#for contact in contacts:
#    print_contact_info(contact)
#print("***END CONTACT PRINT***")



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

# EXPORT CONTACT INFO ## (works)
members = get_active_members()
export_contact_info(members, 'exported_members.csv')

# EXPORT ARCHIVED MEMBER INFO - uses same export function as regular members
archived_members = get_archived_members()
export_contact_info(archived_members, 'exported_archived_members.csv')


## GET AND PRINT EVENTS ## (works)
events = get_events()
export_event_info(events)

# for event in events:
#     print('** BEGIN EVENT INFO **')
#     print_event_info(event)
#     print('** END EVENT INFO **')

# ## GET AND PRINT DONATIONS ## (works)
donations = get_donations()
export_donation_info(donations)
# for donation in donations:
#     print('** BEGIN DONATION INFO **')
#     print_donation_info(donation)
#     print('** END DONATION INFO **')

# ## GET AND PRINT INVOICES ## (works)
invoices = get_invoices()
export_invoice_info(invoices)
#for invoice in invoices:
#    print('** BEGIN INVOICE INFO **')
#    print_invoice_info(invoice) 
#    print('** END INVOICE INFO **')



# ## GET AND PRINT ARCHIVED MEMBERS 
#archived_members = get_archived_members()
# for member in archived_members:
#     print('** BEGIN ARCHIVED MEMBER INFO**')   
#     print_archive_member(member)
#     print('** END ARCHIVED MEMBER INFO **')
