__author__ = 'juhani.takkunen'
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import os
import logging
ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class Order:
    def __init__(self):
        self.product = None
        self.quantity = None
        self.userID = "Unknown"

    def send(self):
        return register_order(self)

def register_order(order):
    try:
        sheet = open_spreadsheet().sheet1
        report_line = [time.strftime("%H:%M"), time.strftime("%Y%m%d"), order.userID, order.product, order.quantity]
        sheet.append_row(report_line)
        return True
    except Exception:
        logging.exception("Unknown exception")
        return False

def open_spreadsheet():
    # This bit of code is copy-pasted from the Internet!
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(ROOT_DIRECTORY, 'kaljarobotti.json'), scope)
    gss_client = gspread.authorize(credentials)

    gc = gspread.authorize(credentials)
    sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1sTuTq5U_kp0zuS32VVKr8_N70lUChA3c2Jewm3HWcEo/edit?usp=sharing')
    return sht2
