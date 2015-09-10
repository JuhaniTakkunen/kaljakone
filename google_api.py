__author__ = 'juhani.takkunen'
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import time

class Order:
    def __init__(self):
        self.product = None
        self.quantity = None
        self.userID = "Junnu"

    def send(self):
        return register_order(self)

def register_order(Order):
    try:
        sheet = open_spreadsheet().sheet1
        # report line data
        report_line = [time.strftime("%H:%M"),time.strftime("%Y%m%d"),Order.userID, Order.product, Order.quantity]
        #status = register_gui.add_row(Order)
        sheet.append_row(report_line)
        #status.all_ok()
        return True
    except Exception as error:
        print(error)
        raise
        # return False

def open_spreadsheet():
    #status = register_gui.connect_to_google(Order)
    json_key = json.load(open('kaljarobotti.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'utf-8'), scope)
    gc = gspread.authorize(credentials)
    #status.all_ok()

    #status = register_gui.open_spreadsheet(Order)
    # You can open a spreadsheet by its title as it appears in Google Docs
    # Or, if you feel really lazy to extract that key, paste the entire url
    sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1sTuTq5U_kp0zuS32VVKr8_N70lUChA3c2Jewm3HWcEo/edit?usp=sharing')
    #status.all_ok()
    return sht2

