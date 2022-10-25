# import.py
# Provides ability to import a member into the database. 
#
# Date of Last Change
# 10/17/2022 - P.Ireland - added comment headers
# 10/19/2022 - P.Ireland - fixed import for member data, will now import members from test_exported_contact_info.csv


from distutils.log import error
from tarfile import NUL
from typing import OrderedDict
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

#### Adding this to use in donation import
paymentsUrl = next(res for res in account.Resources if res.Name == 'Payments').Url 

#creating contact class with all fields accessed from export
class contact():
    def __init__(self, DisplayName, Id, Url, FirstName, LastName, Organization, Email, 
    ProfileLastUpdated, MembershipLevel ,Status, IsAccountAdministrator, TermsOfUseAccepted, Archived,
    Donor, Event_registrant, Member, Suspended_member, Event_announcements, Member_emails_and_newsletters,
    Email_delivery_disabled, Receiving_emails_disabled):
        self.DisplayName = DisplayName
        self.Id = Id 
        self.Url = Url
        self.FirstName = FirstName
        self.LastName = LastName
        self.Organization = Organization
        self.Email = Email
        self.ProfileLastUpdated = ProfileLastUpdated
        self.MembershipLevel = MembershipLevel
        self.Status = Status
        self.IsAccountAdministrator = IsAccountAdministrator
        self.TermsOfUseAccepted = TermsOfUseAccepted
        self.Archived = Archived
        self.Donor = Donor
        self.Event_registrant = Event_registrant
        self.Member = Member
        self.Suspended_member = Suspended_member
        self.Event_announcements = Event_announcements
        self.Member_emails_and_newsletters = Member_emails_and_newsletters
        self.Email_delivery_disabled = Email_delivery_disabled
        self.Receiving_emails_disabled = Receiving_emails_disabled

# Creating event clas with all fields accessed from export
class Event():
    def __init__(self,id,name,type,start_date,start_specified,
    end_date,end_specified,location,registration,registeration_types,
    access_level,tags):
        self.Id = id
        self.Name = name
        self.Type = type
        self.StartDate = start_date
        self.StartTimeSpecified = start_specified
        self.EndDate = end_date
        self.EndTimeSpecified = end_specified
        self.Location = location
        self.RegistrationEnabled = registration
        self.HasEnabledRegistrationTypes = registeration_types
        self.AccessLevel = access_level
        self.Tags = tags

# Creating donation clas with all fields accessed from export
class Donation():
    def __init__(self,Value,DonationDate,FirstName,LastName,PublicComment,Organization):
        self.Value = Value
        self.DonationDate = DonationDate
        self.FirstName = FirstName
        self.LastName = LastName
        self.PublicComment = PublicComment
        self.Organization = Organization
    def get_full_name(self):
        return self.FirstName + " " + self.LastName

# import all member data
def import_member_data():
    #csv file to read member data from to be imported
    with open('test_exported_contact_info.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        #creating a new contact/member with fields from csv file
        for row in reader:
            DisplayName = row['DisplayName'],
            Id = row['Id'],
            Url = row['Url'],
            FirstName = row['FirstName'],
            LastName = row['LastName'],
            Organization = row['Organization'],
            Email = row['Email'],
            ProfileLastUpdated = row['ProfileLastUpdated'],
            MembershipLevel = row['MembershipLevel'],
            Status = row['Status'],
            IsAccountAdministrator = row['IsAccountAdministrator'],
            TermsOfUseAccepted = row['TermsOfUseAccepted'],
            Archived = row['Archived'],
            Donor = row['Donor'],
            Event_registrant = row['Event registrant'],
            Member = row['Member'],
            Suspended_member = row['Suspended member'],
            Event_announcements = row['Event announcements'],
            Member_emails_and_newsletters = row['Member emails and newsletters'],
            Email_delivery_disabled = row['Email delivery disabled'],
            Receiving_emails_disabled = row['Receiving emails disabled'] 
            
            #creating the contact/member
            newContact = contact(DisplayName[0], Id[0], Url[0], FirstName[0], LastName[0], Organization[0], Email[0], 
                                ProfileLastUpdated[0], MembershipLevel[0], Status[0], IsAccountAdministrator[0], TermsOfUseAccepted[0], Archived[0],
                                Donor[0], Event_registrant[0], Member[0], Suspended_member[0], Event_announcements[0], Member_emails_and_newsletters[0],
                                Email_delivery_disabled[0], Receiving_emails_disabled[0])

            #try to import the member
            try:
                import_member(newContact)
            #catch and display any error (most common is email already in use error)    
            except Exception as error:    
                print(f"Error occured creating contact: {newContact.DisplayName}. Error: ", error)
            




# CREATE A CONTACT --- this method was taken from create&archive.py where it was tested and 
# successfully created a contact
def import_member(member:contact):
    #need to add all of the fields here, looking at SwaggerHub example may not can include all fields that were exported though
    
    #Membership level is a dictionary ex: {"Id": 1434812, "Url": "https://api.wildapricot.org/v2/accounts/422750/MembershipLevels/1434812", "Name": "40 and under"}
    #This is read in as a string when reading from the csv file, so we must take a slice of this string
    #to return the id number needed below
    member_level_id = member.MembershipLevel[7:14]

    
    data = {
        'Id' : member.Id,
        'FirstName': member.FirstName, 
        'LastName': member.LastName, 
        'Organization': member.Organization,
        'Email': member.Email,
        'MembershipLevel': {
            "Id" : member_level_id           
        },
        'MembershipEnabled': True,                  
        'Status' : member.Status
        # 'ProfileLastUpdated': member.ProfileLastUpdated, 
        # 'MembershipLevel': member.MembershipLevel, 
        # 'Status': member.Status, 
        # 'IsAccountAdministrator': member.IsAccountAdministrator,
        # 'TermsOfUseAccepted': member.TermsOfUseAccepted
        }

    return api.execute_request(contactsUrl, api_request_object=data, method='POST')




# Returns error: Method Not Allowed
# tried to use datetime object in place of string, but then get error datetime object not JSON serialiazable

#### The error is because we put Id in new created data
#### So basicly our querry is wrong
#### Also the start date needs to be before End Date that makes
#### another error here
def import_event(event:Event):
   #fieldnames = ['Id', 'Name', 'StartDate', 'EndDate', 'Location'] <-- from export.py
    data = {
        'Name': event.Name, 
        'EventType':event.Type,
        'StartDate':event.StartDate,
        'StartTimeSpecified':event.StartTimeSpecified,
        'EndDate':event.EndDate,
        'EndTimeSpecified':event.EndTimeSpecified,
        'Location':event.Location,
        'RegistrationEnabled':event.RegistrationEnabled,
        'Tags':event.Tags,
        "Details":{
            "AccessControl":{
                "AccessLevel":event.AccessLevel
            }
        }
    }
    return api.execute_request(eventsUrl, api_request_object=data, method='POST')

def import_event_data():
    with open('test_exported_event_info.csv',newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            Id = row['Id']
            Name = row['Name']
            Type = row['Type']
            StartDate = row['StartDate']
            StartTimeSpecified = row['StartTimeSpecified']
            EndDate = row['EndDate']
            EndTimeSpecified = row['EndTimeSpecified']
            Location = row['Location']
            RegistrationEnabled = row['RegistrationEnabled']
            HasEnabledRegistrationTypes = row['HasEnabledRegistrationTypes']
            AccessLevel = row['AccessLevel']
            Tags = row['Tags']

            newEvent = Event(Id,Name,Type,StartDate,
            StartTimeSpecified,EndDate,EndTimeSpecified,
            Location,RegistrationEnabled,HasEnabledRegistrationTypes,
            AccessLevel,Tags)

            try: 
                import_event(newEvent)
            except Exception as error:
                print(f"Error occured creating event: {newEvent.Name}. Error: ", error)


#Receive same Error 405: Method Not Allowed that receive with import_event()

#### We are totally wrong with the api querry 
#### Here we need to change our data 
#### ill let the old data stay so you can compare the changes
def import_invoice():
    # fieldnames = ['Id', 'Value', 'DocumentDate', 'Contact', 'CreatedDate', 'CreatedBy', 'IsPaid'] <-- from export.py
    '''data = {
        'Id': 999999,
        'Value': 5.0,
        'DocumentDate': '2022-09-30T03:06:36+00:00',
        'Contact': "{""Id"": 66020498, ""Url"": ""https://api.wildapricot.org/v2/accounts/422750/Contacts/66020498"", ""Name"": ""Honea, Seth""}",
        'CreatedDate': '2022-09-27T03:06:36',
        'CreatedBy' : "{""Id"": 66133802, ""Url"": ""https://api.wildapricot.org/v2/accounts/422750/Contacts/66133802""}",
        'IsPaid' : False

    }'''

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


#### 
#Receive same Error 405: Method Not Allowed that receive with import_event() and import_invoice()

#### Again same as above the querry call is wrong ill let 
#### the old one stay to cross-check what was missing
#### Also The Donation dosent support Post request
#### To add new donation
#### We need to create payment with type of Donation
#### That will create us new donation

def import_donation():
    # fieldnames = ['Value', 'DonationDate', 'FirstName', 'LastName', 'PublicComment', 'Organization']
    '''data = {
        'Value' : 25.00,
        'DonationDate' : '2022-09-30T03:06:36+00:00',
        'FirstName' : 'Payton',
        'LastName' : 'Ireland',
        'PublicComment' : '',
        'Organization' : ''
    }'''

    data = {
        "Value": 10.0,
        "DocumentDate": "2022-10-24",
        
        "Contact": {
            "Id": 66133802,
            "Url": "Nothing"
        },
        "Comment": "Checking Api Functionality",
        "PublicComment": "Checking API",
        # The reason paymentType is DonationPayment
        # This will make new Donation
        "PaymentType": "DonationPayment"
    }

    return api.execute_request(paymentsUrl, api_request_object=data, method='POST')

### it needs to be complete in future your export functions are missing some data like the member id which is needed to create the
### Donation Contact Field
def import_donation(donate:Donation):
    # fieldnames = ['Value', 'DonationDate', 'FirstName', 'LastName', 'PublicComment', 'Organization']
    print("-> Value " + donate.Value)
    print("-> DocumentDate " + donate.DonationDate)
    print("-> FirstName " + donate.FirstName)
    print("-> LastName " + donate.LastName)
    print("-> PublicComment " + donate.PublicComment)
    print("-> Organization " + donate.Organization)
    data = {
        "Value": donate.Value,
        "DocumentDate": donate.DonationDate,
        
        "Contact": {
            "Id": 66133802,
            "Url": "Not Provided",
            "Name": donate.get_full_name() 
        },
        "Comment": "Created From BackEnd",
        "PublicComment": donate.PublicComment,
        "PaymentType": "DonationPayment"
    }

    return api.execute_request(paymentsUrl, api_request_object=data, method='POST')

def import_donation_data():
    with open('test_exported_donation_info.csv',newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            Value = row['Value']
            DonationDate = row['DonationDate']
            FirstName = row['FirstName']
            LastName = row['LastName']
            PublicComment = row['PublicComment']
            Organization = row['Organization']

            newDonation = Donation(Value,DonationDate,FirstName,LastName,PublicComment,Organization)

            try: 
                import_donation(newDonation)
            except Exception as error:
                print(f"Error occured creating event: {newDonation.FirstName} {newDonation.LastName}. Error: ", error)


import_member_data()


