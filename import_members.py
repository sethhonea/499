# Provies the ability to import members into the databae. Multiple
# members may not have the same email address - this causes 
# members already in the database to not be uploaded. Any member
# that is not imported will display an error message in the terminal
# stating the member was not imported. 

# Created by: Backend Team (Payton Ireland, Seth Honea, Juliet Awoyale)

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



# import all member data
def import_member_data():
    #csv file to read member data from to be imported
    with open('test_exported_members.csv', newline='') as csvfile:
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
    member_archived = member.Archived
    member_enabled = True
    if member_archived:
        member_enabled = False
    

    data = {
        #'Id' : member.Id,
        'FirstName': member.FirstName, 
        'LastName': member.LastName, 
        'Organization': member.Organization,
        'Email': member.Email,
        'MembershipLevel': {
            "Id" : member_level_id           
        },
        'MembershipEnabled': member_enabled,                  
        'Status' : member.Status
        # 'ProfileLastUpdated': member.ProfileLastUpdated, 
        # 'MembershipLevel': member.MembershipLevel, 
        # 'Status': member.Status, 
        # 'IsAccountAdministrator': member.IsAccountAdministrator,
        # 'TermsOfUseAccepted': member.TermsOfUseAccepted
        }

    return api.execute_request(contactsUrl, api_request_object=data, method='POST')



import_member_data()