__author__ = 'juhani.takkunen'
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import time

class Order:
    def __init__(self):
        self.product = None
        self.quantity = None
        self.userID = "Junnu"  # TODO: get this from fingerprint sensor

    def send(self):
        return register_order(self)

def register_order(order):
    try:
        sheet = open_spreadsheet().sheet1
        report_line = [time.strftime("%H:%M"),time.strftime("%Y%m%d"),order.userID, order.product, order.quantity]
        sheet.append_row(report_line)
        return True
    except Exception as error:
        print(error)
        return False

def open_spreadsheet():
    # This bit of code is copy-pasted from the Internet!
    json_key = json.load(open('kaljarobotti.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'utf-8'), scope)
    gc = gspread.authorize(credentials)
    sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1sTuTq5U_kp0zuS32VVKr8_N70lUChA3c2Jewm3HWcEo/edit?usp=sharing')
    return sht2

