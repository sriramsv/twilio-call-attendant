from __future__ import print_function
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

class ContactRegistry:
    def __init__(self):
        self.contactMap = {}
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('people', 'v1', credentials=creds)
        self.contactMap = self.fetch_contacts(service,"")

    def get_contacts(self):
        return self.contactMap

    def fetch_contacts(self, service, pageToken=""):
        contactMap = {}
        while True:
            results = service.people().connections().list(
                resourceName='people/me',
                pageSize=20,
                pageToken=pageToken,
                personFields='names,phoneNumbers').execute()
            connections = results.get('connections', [])
            for person in connections:
                if "names" in person and "phoneNumbers" in person:
                    name = person["names"][0]["displayName"]
                    phone = person["phoneNumbers"][0]["value"]
                    contactMap[name]=phone

            pageToken = results.get('nextPageToken',"")
            if pageToken == "":
                break
        return contactMap



if __name__ == '__main__':
    c = ContactRegistry()
    print(c.get_contacts())