#!/usr/bin/python

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import text
import time


def main():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client-secret.json', scope)
    client = gspread.authorize(creds)
    responses = client.open('Family History Help (Responses)')
    rows = responses.sheet1.get_all_records()
    
    not_helped = [row for row in rows if not row["Who's helping them"]]
    help(not_helped)

    not_verified = [row for row in rows if row["Who's helping them"] and not row['Followed up']]
    verify(not_verified)


def help(not_helped):
    with open('committee.txt') as file:
        committee = file.read().splitlines()
	message = ("Hey, {{name}}! There are {number} people that have filled "
			   "requested help with family history that haven't been helped "
               "yet. If you could help one of them that'd be great. "
			   "Remember to put your name in the \"Who's helping them\" "
               "column for whomever you're going to help. Thanks!"
              ).format(number=len(not_helped))
    for person in committee:
        name = person.split(' ')[0]
        personalized = message.format(name=name)
        text.send_to_name(person, personalized)
        # android app can't handle multiple notifications that arrive at almost the same time
        # TODO: fix android app
        time.sleep(1)


def verify(not_verified):
    # TODO
    pass


if __name__ == '__main__':
    main()

