# Export.py
# Provides ability to export active member data, archived member data, 
# event data, invoice data, and donation data as separate csv files. 

# Created by: Backend Team (Payton Ireland, Seth Honea, Juliet Awoyale)

# Date of Last Change
# 10/17/2022 - P.Ireland - added comment headers
# 11/01/2022 - P.Ireland - cleaned code by removing extraneous comments

from tarfile import NUL
import API
import urllib.parse
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

#DEFINING ALL FUNCTIONS TO RETRIEVE DATA FROM DATABASE
# ----------------------------------------------------------------------------------------------        

# GET ACTIVE MEMBERS - retrieves all active members
def get_active_members():
    params = {'$filter': 'archived eq false',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts

# GET ARCHIVED MEMBERS - retrieves all archived members
def get_archived_members():
    params = {'$filter': 'archived eq true ',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts    

 # GET EVENTS - retrieves all events with registration enabled
def get_events():
    params = {'$filter': 'RegistrationEnabled eq true',
              '$async': 'false'}
    request_url = eventsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Events      
      

# GET INVOICES - retrieves last 100 invoices
def get_invoices():
    params = {'$unpaidOnly': 'true',
              '$top': '100'}
    request_url = invoicesUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url)

# GET DONATIONS - retrieves last 100 donations
def get_donations():
    params = {'$top': '100'}
    request_url = donationsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url)


# DEFINING ALL PRINT TO TERMINAL FUNCTIONS BELOW
#---------------------------------------------------------------------------------------------------

# PRINT DONATION INFO
def print_donation_info(payment):
    print('Donation Value: ' + str(payment.Value))
    print('Donation Date: ' + str(payment.DonationDate))
    print('Donation Made By: ' + str(payment.FirstName) + ' ' + str(payment.LastName))
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
    print('Invoice Updated Date: ' + str(invoice.UpdatedDate))
    print('Invoice Updated By: ' + str(invoice.UpdatedBy))
    print('Document Number: ' + str(invoice.DocumentNumber))
    print('Invoice Is Paid: ' + str(invoice.IsPaid))
    print('Invoice Order Type: ' + str(invoice.OrderType))
    print('Invoice Memo: ' + str(invoice.Memo))
    print('Invoice Public Memo: ' + str(invoice.PublicMemo))

    

# PRINT EVENT INFO
def print_event_info(event):
    print('Event ID: ' + str(event.Id))
    print('Event Name: ' + str(event.Name))
    print('Event Type: ' + str(event.EventType))
    print('Event Start Date: ' + str(event.StartDate))
    print('Event Start Time Specified: ' + str(event.StartTimeSpecified))
    print('Event End Date: ' + str(event.EndDate))
    print('Event End Time Specified: ' + str(event.EndTimeSpecified))
    print('Event Location: ' + str(event.Location))
    print('Event Registration Enabled: ' + str(event.RegistrationEnabled))
    print('Event Has Enabled Registration Types: ' + str(event.HasEnabledRegistrationTypes))
    print('Event Access Level: ' + str(event.AccessLevel))
    print('Event Tags: ' + str(event.Tags))


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
        #Field Values must be popped
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

# EXPORT CONTACT INFO -- used for both archived and active members to export their information to csv
# because they have the exact same fields. 
def export_contact_info(contacts, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['DisplayName', 'Id', 'Url', 'FirstName', 'LastName', 'Organization',
        'Email', 'ProfileLastUpdated', 'MembershipLevel', 'Status', 'IsAccountAdministrator',
        'TermsOfUseAccepted', 'Archived', 'Donor', 'Event registrant', 'Member', 'Suspended member',
        'Event announcements', 'Member emails and newsletters', 'Email delivery disabled', 
        'Receiving emails disabled']

        #open the provided csv file, writing each contact in contacts provided to a row
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
                })
            except: 
                print("Unable to export information for ", contact.DisplayName)


# EXPORT EVENT INFO - write each event in events to csv file as a row
def export_event_info(events):
    with open('exported_event_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['Id', 
                    'Name', 
                    'Type',
                    'StartDate', 
                    'StartTimeSpecified',
                    'EndDate', 
                    'EndTimeSpecified',
                    'Location',
                    'RegistrationEnabled',
                    'HasEnabledRegistrationTypes',
                    'AccessLevel',
                    'Tags'
                    ]
        thewriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
        thewriter.writeheader()
        for event in events:
            ## *****************************
            # will need to update if clause to account for all uploaded document names
            if event.Name == "DDD Draft Document Upload Test":
                export_document_event(event)
                continue
            thewriter.writerow({
                'Id': event.Id, 
                'Name': event.Name, 
                'Type': event.EventType,
                'StartDate': event.StartDate,
                'StartTimeSpecified': event.StartTimeSpecified, 
                'EndDate': event.EndDate,
                'EndTimeSpecified': event.EndTimeSpecified, 
                'Location': event.Location,
                'RegistrationEnabled': event.RegistrationEnabled,
                'HasEnabledRegistrationTypes': event.HasEnabledRegistrationTypes,
                'AccessLevel': event.AccessLevel,
                'Tags': event.Tags
            })


# EXPORT INVOICE INFO - write each invoice in invoices to csv file as a row
def export_invoice_info(invoices):
    with open('exported_invoice_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['Id', 
                    'Value', 
                    'DocumentDate', 
                    'Contact', 
                    'CreatedDate', 
                    'CreatedBy', 
                    'IsPaid',
                    'OrderType',
                    'Memo',
                    'PublicMemo']
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
                'IsPaid': invoice.IsPaid,
                'OrderType': invoice.OrderType,
                'Memo': invoice.Memo,
                'PublicMemo': invoice.PublicMemo
            })


# EXPORT DONATION INFO - write each donation in donations to csv file as a row
def export_donation_info(donations):
    with open('exported_donation_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['Value', 
                    'DonationDate', 
                    'FirstName', 
                    'LastName',
                    'PublicComment', 
                    'Organization']
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



# EXPORT EVENT INFO - write each event in events to csv file as a row
def export_document_event(doc_event):
    filename = doc_event.Name + '.txt'
    
    with open(filename, 'w') as file:
        text = doc_event.Tags
        for string in text:
            file.write(string)
        
    


# CALLING FUNCTIONS TO RETRIEVE DATA, PRINT DATA, AND/OR EXPORT DATA
#---------------------------------------------------------------------------------------------------------



# EXPORT ACTIVE MEMBERS 
members = get_active_members()
export_contact_info(members, 'exported_members.csv')

# EXPORT ARCHIVED MEMBER INFO - uses same export function as regular members
archived_members = get_archived_members()
export_contact_info(archived_members, 'exported_archived_members.csv')


## EXPORT EVENTS
events = get_events()
export_event_info(events)


# EXPORT DONATIONS
donations = get_donations()
export_donation_info(donations)


# EXPORT INVOICES
invoices = get_invoices()
export_invoice_info(invoices)




