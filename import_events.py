import csv
import API

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


#creating event class with all fields accessed from export
class event():
    def __init__(self, Id, Name,Type,StartDate,StartTimeSpecified,EndDate,EndTimeSpecified,Location,RegistrationEnabled,HasEnabledRegistrationTypes,AccessLevel,Tags):
        self.Id = Id
        self.Name = Name
        self.Type = Type
        self.StartDate = StartDate
        self.StartTimeSpec = StartTimeSpecified
        self.EndDate = EndDate
        self.EndTimeSpec = EndTimeSpecified
        self.Location = Location
        self.RegEnabled = RegistrationEnabled
        self.HasEnabled = HasEnabledRegistrationTypes
        self.AccessLevel = AccessLevel
        self.Tags = Tags


def import_event_data():
    with open('test_exported_events.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

#Id,Name,Type,StartDate,StartTimeSpecified,EndDate,EndTimeSpecified,Location,RegistrationEnabled,HasEnabledRegistrationTypes,AccessLevel,Tags
        #creating a new contact/member with fields from csv file
        for row in reader:
            Id = row['Id'],
            Name = row['Name'],
            Type = row['Type'],
            StartDate = row['StartDate'],
            StartTimeSpec = row['StartTimeSpecified'],
            EndDate = row['EndDate'],
            EndTimeSpec = row['EndTimeSpecified'],
            Location = row['Location'],
            RegEnabled = row['RegistrationEnabled'],
            HasEnabled = row['HasEnabledRegistrationTypes']
            AccessLevel = row['AccessLevel']
            Tags = row['Tags']

            new_event = event(Id[0], Name[0], Type[0], StartDate[0], StartTimeSpec[0], EndDate[0], EndTimeSpec[0], Location[0],
            RegEnabled[0], HasEnabled, AccessLevel, Tags[0])
            
            import_event(new_event)


def import_event(event:event):
    data = {
        #'Id' : event.Id,
        'Name' : event.Name,
        'EventType' : event.Type,
        'StartDate' : event.StartDate,
        'StartTimeSpecified' : event.StartTimeSpec,
        'EndDate': event.EndDate,
        'EndTimeSpecified' : event.EndTimeSpec,
        'Location' : event.Location,
        'RegistrationEnabled' : event.RegEnabled,
        'Tags' : event.Tags
        }

    return api.execute_request(eventsUrl, api_request_object=data, method='POST')



import_event_data()