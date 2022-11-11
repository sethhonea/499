# import_events.py
# Provides ability to import invoices into the database.

# Created by: Backend Team (Payton Ireland, Seth Honea, Juliet Awoyale)

# Date of Last Change
# 11/01/2022 - P.Ireland Created file and added functions to import invoices - not currently functional. 

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
invoicesUrl = next(res for res in account.Resources if res.Name == 'Invoices').Url


# invoice class to create an invoice with appropriate fields
class invoice():
    def __init__(self,Id,Value,DocumentDate,Contact,CreatedDate,CreatedBy,IsPaid,OrderType,Memo,PublicMemo):
        self.Id = Id
        self.Value = Value
        self.DocumentDate = DocumentDate
        self.Contact = Contact
        self.CreatedDate = CreatedDate
        self.CreatedBy = CreatedBy
        self.IsPaid = IsPaid
        self.OrderType = OrderType
        self.Memo = Memo
        self.PublicMemo = PublicMemo
    
#IMPORT INVOICES - reads in invoices from test_invoices.csv and creates an invoice from each row to be imported
def import_invoice_data():
    with open('test_invoices.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        #creating a new invoice with fields from a row in the csv file
        for row in reader:
            Id = row['Id']
            Value = row['Value']
            DocumentDate = row['DocumentDate']
            Contact = row['Contact']
            CreatedDate = row['CreatedDate']
            CreatedBy = row['CreatedBy']
            IsPaid = row['IsPaid']
            OrderType = row['OrderType']
            Memo = row['Memo']
            PublicMemo = row['PublicMemo']
            
            #cretae an invoice with fields read in from csv
            new_invoice = invoice(Id, Value, DocumentDate, Contact, CreatedDate, CreatedBy,
            IsPaid, OrderType, Memo, PublicMemo)
            
            #import the new_invoice created above
            import_invoice(new_invoice)


#Receive -->  API.ApiException: b'{"code":"Validation","message":"All invoice items must have description","details":[{"Key":".","Value":"","Restriction":"All invoice items must have description"}]}'
#IMPORT INVOICE - takes in a single invoice and imports it into the database
def import_invoice(invoice:invoice):
    #only need the Id of contact 
    contact_id = invoice.Contact[7:15]
    #only need the Id of the contact that created the invoice
    created_by_id = invoice.CreatedBy[7:15]

    data = {
        #'Id': ,              cannot supply an ID
        'Value': invoice.Value,
        'DocumentDate': invoice.DocumentDate,
        'Contact': {
            'Id' : contact_id
        },
        'CreatedBy' : {
            'Id' : created_by_id
        },
        'Memo' : invoice.Memo,
        'PublicMemo' : invoice.PublicMemo,
        'OrderDetails' : [{
            'Value' : invoice.Value,
            'OrderDetailType': 'Testing Import' 
        }]

    }

    return api.execute_request(invoicesUrl, api_request_object=data, method='POST')


#call to import invoices
import_invoice_data()



