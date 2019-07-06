import json
import io
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from tkinter import *
from PIL import ImageTk, Image
import time
import logging

var = "48:2c:a0:e3:0b:8c"
var = "f0:18:98:43:5e:81"
var = "msakovyc"
var = "vkozhemi"
floor = "3rd"

class Map():
    def __init__(self):
        urllib3.disable_warnings()
        self.threadLoop = True
        self.URL = "https://cisco-cmx.unit.ua"
        self.username = "RO"
        self.password = "just4reading"

        self.width = 1000
        self.height = 500

        self.mac_or_login = ""

        self.var = "48:2c:a0:e3:0b:8c"
        self.var = "f0:18:98:43:5e:81"
        self.var = "msakovyc"
        self.var = "vkozhemi"
        self.floor = "1_Floor"

        # MAP pic
        self.dict_map = {
            "1_Floor": "/api/config/v1/maps/image/System%20Campus/UNIT.Factory/1st_Floor",
            "2_Floor": "/api/config/v1/maps/image/System%20Campus/UNIT.Factory/2nd_Floor",
            "3_Floor": "/api/config/v1/maps/image/System%20Campus/UNIT.Factory/3rd_Floor",
        }

        self.LOG_FILENAME = 'logging_example'
        logging.basicConfig(filename=self.LOG_FILENAME, level=logging.ERROR, filemode="w")

        self.all_info = self.doRequest('/api/location/v2/clients/')

    def error(self):
        print("ERROR: Server not responding")

    def doRequest(self, URI):
        try:
            request = requests.get(
                url=(self.URL + URI),
                auth=HTTPBasicAuth(self.username, self.password),
                verify=False)
            js = json.loads(request.text)
        except Exception:
            self.error()
            js = []
            logging.error("An error happened in class Map(): doRequest()")
        return js

    def search_username(self, user):
        try:
            js = self.doRequest('/api/location/v2/clients/')
            tmp = ""
            user_data = []
            for x in js:
                if user == (x['userName']) or user == (x['macAddress']):
                    tmp = 1
                    user_data = {
                        'userName': (x['userName']),
                        'mac_addres': (x['macAddress']),
                        'ipAddress': (x['ipAddress']),
                        'mapInfo': (x['mapInfo']),
                        'mapCoordinate': (x['mapCoordinate']),
                        'manufacturer': (x['manufacturer']),
                        'statistics': (x['statistics']),
                    }
            if not tmp:
                # print("user not found")
                user_data = ""
        except Exception:
                self.error()
                user_data = ""
                logging.error("An error happened in class Map(): search_username()")
        return user_data

    def show_all_user_floor(self, floor):
        try:
            floor = "System Campus>UNIT.Factory>" + floor# + "_Floor"
            js = self.doRequest('/api/location/v2/clients/')
            tmp = ""
            user_data = []

            for x in js:
                if floor in x['mapInfo']['mapHierarchyString']:
                    tmp = 1
                    user = {
                        'userName': (x['userName']),
                        'mac_addres': (x['macAddress']),
                        'ipAddress': (x['ipAddress']),
                        'mapInfo': (x['mapInfo']),
                        'mapCoordinate': (x['mapCoordinate']),
                        'manufacturer': (x['manufacturer']),
                        'statistics': (x['statistics']),
                    }
                    user_data.append(user)
            if not tmp:
                print("not found")
                user_data = ""
        except Exception:
            self.error()
            user_data = ""
            logging.error("An error happened in class Map(): show_all_user_floor()")
        return user_data

    def get_image_floor(self, key_dict):
        try:
            image = self.v1(key_dict)
            img = Image.open(io.BytesIO(image))
            self.width = img.width
            self.height = img.height

            factor = 0.5
            if key_dict == "2_Floor":
                factor *= 0.796

            self.width = int(self.width * factor)
            self.height = int(self.height * factor)
            img = img.resize((self.width, self.height), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)
        except Exception:
            self.error()
            logging.error("An error happened in class Map(): get_image_floor()")
        return img_tk

    def v1(self, key_dict):
        try:
            URI = self.dict_map[key_dict]
            request = requests.get(
                url=(self.URL + URI),
                auth=HTTPBasicAuth(self.username, self.password),
                verify=False)
            request = request.content
        except Exception:
            self.error()
            request = ""
            logging.error("An error happened in class Map(): v1()")
        return request

    # ============================================= NOTIFICATON ========================================================
    def mapCoordinates(self, dict):
        dict = str(dict)
        dict = dict[20:40]
        return dict
    #
    #
    # def find_floor2(self, dict):
    #     try:
    #         js = dict
    #         tmp = ""
    #         user_data = []
    #         for x in js:
    #             if dict == (x['userName']) or dict == (x['macAddress']):
    #                 tmp = 1
    #                 user_data = {
    #                     (x['mapInfo']['mapHierarchyString'])
    #                 }
    #                 user_data = str(user_data)
    #                 user_data = user_data[29:32]
    #         if not tmp:
    #             print("user not found")
    #             user_data = ""
    #     except Exception:
    #         self.error()
    #         user_data = ""
    #         logging.error("An error happened in class Map(): find_floor()")
    #     return user_data

    def find_floor(self, user):
        try:
            js = self.doRequest('/api/location/v2/clients/')
            tmp = ""
            user_data = []
            for x in js:
                if user == (x['userName']) or user == (x['macAddress']):
                    tmp = 1
                    user_data = {
                        (x['mapInfo']['mapHierarchyString'])
                    }
                    user_data = str(user_data)
                    user_data = user_data[29:32]
            if not tmp:
                print("user not found")
                user_data = ""
        except Exception:
            self.error()
            user_data = ""
            logging.error("An error happened in class Map(): find_floor()")
        return user_data

    def diff(self, first, second):
        second = set(second)
        return [item for item in first if item not in second]

    def macs(self):
        try:
            js = self.doRequest('/api/location/v2/clients/')
            all_macs = []
            for x in js:
                tmp = x['macAddress']
                all_macs.append(tmp)
        except Exception:
            self.error()
            all_macs = ""
            logging.error("An error happened in class Map(): macs()")
        return (all_macs)

    def proc_notification(self):
        try:
            js1 = self.macs()
            while self.threadLoop:
                time.sleep(4)                                                                             # delay 4 sec
                js2 = self.macs()
                if js1 != js2:
                    notification = self.diff(js2, js1)
                    if notification:
                        for x in notification:
                            login = self.search_username(x)
                            floor = self.find_floor(x)
                            if login != "":
                                if not login['userName']:
                                    self.mac_or_login = "Hi, "+x+" now is on the "+floor+" floor"
                                    print(self.mac_or_login)                                                     # mac
                                else:
                                    floor = self.find_floor(login['userName'])
                                    self.mac_or_login = "Hi, "+login['userName']+" now is on the "+floor+" floor"
                                    print(self.mac_or_login)                                                    # login
                            # else:
                            #     self.mac_or_login = "Hi, "+x+" now is on the "+floor+"floor"
                            #     print(self.mac_or_login)                                                      # mac
                else:
                    self.mac_or_login = "                                                                              "
                js1 = js2
        except Exception:
            self.error()
            self.mac_or_login = ""                                                                              # empty
            logging.error("An error happened in class Map(): proc_notification()")
    # ==================================================================================================================

# def main():
#     map = Map()
#     print("\nHELLO\n")
#
#     root = Tk()
#     print("all = ", map.all_info)
#     print("search_userName(userName) = ", map.search_username('vkozhemi'))  # mac or userName
#     print("show_all_user_floor(floor) = ", map.show_all_user_floor('2nd'))
#     # print("notifications = ", map.notifications())
#
#     fr = Frame(root, width=14.4, height=10)
#     fr.grid()
#
#     img_tk = map.get_image_floor('1_Floor')
#
#     # canvas = Canvas(fr, width=14.4, height=10)
#     # canvas.create_image(0, 0, image=img_tk, anchor=NW)
#     # canvas.grid(row=0, column=0)
#
#     panel = Label(fr, image=img_tk)
#     panel.grid()
#     root.mainloop()
