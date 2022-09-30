
from tarfile import NUL
from typing import OrderedDict
import API
import urllib.parse
import json
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


class contact():
    def __init__(self, id, firstName, lastName, email):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email