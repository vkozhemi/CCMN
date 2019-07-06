from collections import defaultdict

import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
import operator
import logging


cmxURL = "https://cisco-cmx.unit.ua"
cmxUsername = "RO"
cmxPassword = "just4reading"

class Presence():
    def __init__(self):
        urllib3.disable_warnings()
        self.URL = "https://cisco-presence.unit.ua"
        self.username = "RO"
        self.password = "Passw0rd"

        self.startDate = "2019-04-12"  # YYYY-MM-DD
        self.endDate = "2019-04-13"  # YYYY-MM-DD
        self.key_dict = "repeatvisitors_average"  # connected visitor passerby  (from dict[])
        self.date = "today"  # today yesterday lastweek lastmonth  or nothing
        self.siteid = self.getSiteId()

        self.dict = {

            # PROXIMITY
            # ----------------------------------Graphic----------------------------------------
            # Passerby
            "passerby": "/api/presence/v1/passerby/",
            # Visitors
            "visitor": "/api/presence/v1/visitor/",
            # Connected
            "connected": "/api/presence/v1/connected/",
            # ----------------------------------Average----------------------------------------
            # Average -> Passerby

            # ----------------------------------Distribution-----------------------------------
            # Passerby Distribution
            "passerby_dist": "/api/presence/v1/passerby/",
            # Visitors Distribution
            "visitor_dist": "/api/presence/v1/visitor/",
            # Connected Distribution
            "connected_dist": "/api/presence/v1/connected/",

            # DWELL TIME
            # ----------------------------------Graphic----------------------------------------
            "dwell": "/api/presence/v1/dwell/",
            # ----------------------------------Average----------------------------------------
            "dwell_dailyaverage": "/api/presence/v1/dwell/dailyaverage/",
            # ----------------------------------Distribution-----------------------------------
            "dwell_dist": "/api/presence/v1/dwell/count/",

            ## REPEAT VISITORS                    241
            # ----------------------------------Graphic----------------------------------------
            # Repeat Visitors
            "repeatvisitors": "/api/presence/v1/repeatvisitors/",
            # ----------------------------------Average----------------------------------------
            # Repeat Visitors Average
            "repeatvisitors_average": "/api/presence/v1/repeatvisitors/average/",
            # ----------------------------------Distribution-----------------------------------
            # Repeat Visitors Distribution O
            "repeatvisitors_dist": "/api/presence/v1/repeatvisitors/count/",
        }
        self.LOG_FILENAME = 'logging_example'
        logging.basicConfig(filename=self.LOG_FILENAME, level=logging.ERROR, filemode="w")

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
            logging.error("An error happened in class Presence(): doRequest()")
        return js

    def getSiteId(self):
        siteid = []
        try:
            URI = "/api/config/v1/sites"
            res = self.doRequest(URI)
            siteid = res[0]['aesUId']
        except Exception:
            self.error()
            logging.error("An error happened in class Presence(): getSiteId()")
        return (siteid)


    def total_visitors(self):
        unique_visitors = self.proximity("visitor_dist")
        total_visitors = unique_visitors
        total_connected = self.proximity("connected_dist")
        percentage_of_connected_visitors = round(total_connected / total_visitors * 100)
        return [unique_visitors, total_visitors, total_connected, percentage_of_connected_visitors]


    def average_dwell_time(self):
        visitors = self.dwell_time("dwell_dist")
        return list(visitors.values())


    def peak_hour(self):
        visitors = self.proximity("visitor")
        if self.date == "today" or self.date == "yesterday":
            inverse = [(value, key) for key, value in visitors.items()]
            peakhour = max(inverse)[1]
            visitors_on = max(inverse)[0]
            return [peakhour, visitors_on]
        else:
            inverse = [(value, key) for key, value in visitors.items()]
            peakday = max(inverse)[1]
            visitors_on = max(inverse)[0]
            return [peakday, visitors_on]


    def conversion_rate(self):
        passerby = self.proximity("passerby_dist")
        visitors = self.proximity("visitor_dist")
        res = round(visitors / (visitors + passerby) * 100)
        return [res, visitors, passerby]

    def leaders(self, xs, top=10):
        counts = defaultdict(int)
        for x in xs:
            counts[x] += 1
        return sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]

    def top_device_maker(self):
        try:
            URI = '/api/location/v2/clients/'
            request = requests.get(
                url=(cmxURL + URI),
                auth=HTTPBasicAuth(cmxUsername, cmxPassword),
                verify=False)
            js = json.loads(request.text)
            res = []
            for item in js:
                mac = item['manufacturer']
                res.append(mac)
        except Exception:
            self.error()
            res = []
            logging.error("An error happened in class Presence(): top_device_maker()")
        return self.leaders(res)

    # =========================================== INSIGHTS =================================================================

    def insights_today(self):
        URI = '/api/presence/v1/passerby/count/today?siteId=' + str(self.siteid)
        pas = self.doRequest(URI)
        URI = '/api/presence/v1/visitor/count/today?siteId=' + str(self.siteid)
        vis = self.doRequest(URI)
        URI = '/api/presence/v1/connected/count/today?siteId=' + str(self.siteid)
        con = self.doRequest(URI)
        URI = '/api/presence/v1/visitor/hourly/today?siteId=' + str(self.siteid)
        res = self.doRequest(URI)
        inverse = [(value, key) for key, value in res.items()]
        peakhour = max(inverse)[1]
        visitors_on = max(inverse)[0]
        return [pas, vis, con, peakhour, visitors_on]

    def insights_yesterday(self):
        URI = '/api/presence/v1/passerby/count/yesterday?siteId=' + str(self.siteid)
        pas = self.doRequest(URI)
        URI = '/api/presence/v1/visitor/count/yesterday?siteId=' + str(self.siteid)
        vis = self.doRequest(URI)
        URI = '/api/presence/v1/connected/count/yesterday?siteId=' + str(self.siteid)
        con = self.doRequest(URI)
        URI = '/api/presence/v1/visitor/hourly/yesterday?siteId=' + str(self.siteid)
        res = self.doRequest(URI)
        inverse = [(value, key) for key, value in res.items()]
        peakhour = max(inverse)[1]
        visitors_on = max(inverse)[0]
        return [pas, vis, con, peakhour, visitors_on]

    def insights_tomorrow(self):
        URI = '/api/presence/v1/passerby/daily/lastmonth?siteId=' + str(self.siteid)
        pas = self.doRequest(URI)
        URI = '/api/presence/v1/visitor/daily/lastmonth?siteId=' + str(self.siteid)
        vis = self.doRequest(URI)
        URI = '/api/presence/v1/connected/daily/lastmonth?siteId=' + str(self.siteid)
        con = self.doRequest(URI)
        pas = list(pas.values())
        pas = round((pas[23] + pas[16] + pas[9] + pas[2]) / 4)
        vis = list(vis.values())
        vis = round((vis[23] + vis[16] + vis[9] + vis[2]) / 4)
        con = list(con.values())
        con = round((con[23] + con[16] + con[9] + con[2]) / 4)
        insights_yesterday_peak_hour = self.insights_yesterday()
        insights_yesterday_visitors = self.insights_yesterday()
        visitors_on = round(
            (insights_yesterday_peak_hour[4] / insights_yesterday_visitors[1]) * vis)
        peakhour = insights_yesterday_peak_hour[3]
        return [pas, vis, con, peakhour, visitors_on]

    # ==================================================================================================================

    def proximity(self, key_dict):
        try:
            if "dist" in key_dict:
                if self.date != "":
                    date = "count/" + self.date
                elif key_dict == "passerby_dist" or key_dict == "connected_dist" and self.date == "":
                    date = "total"
                elif key_dict == "visitor_dist" and self.date == "":
                    date = "count/"
            else:
                if self.date == "today" or self.date == "yesterday":
                    date = "hourly/" + self.date
                elif self.date == "lastweek" or self.date == "lastmonth":
                    date = "daily/" + self.date
                else:
                    date = "daily/"
            URI = self.dict[key_dict] + date + "?siteId=" + str(self.siteid) + "&startDate=" + self.startDate + "&endDate=" + self.endDate
            res = self.doRequest(URI)
        except Exception:
            self.error()
            res = ""
            logging.error("An error happened in class Presence(): proximity()")
        return res

    def dwell_time(self, key_dict):
        try:
            date = self.date
            if "dist" in key_dict:
                date = self.date
            elif "dailyaverage" in key_dict:
                if self.date == "today" or self.date == "yesterday":
                    key_dict = "passerby"
                    res = self.proximity(key_dict)
                    return (res)
            else:
                if self.date == "today" or self.date == "yesterday":
                    date = "hourly/" + self.date
                elif self.date == "lastweek" or "lastmonth":
                    date = "daily/" + self.date
                else:
                    date = "daily"
            URI = self.dict[key_dict] + date + "?siteId=" + str(self.siteid) + "&startDate=" + self.startDate + "&endDate=" + self.endDate
            res = self.doRequest(URI)
        except Exception:
            self.error()
            res = ""
            logging.error("An error happened in class Presence(): dwell_time()")
        return res


    def repeat_visitors(self, key_dict):
        global date
        try:
            if "dist" in key_dict:
                date = self.date
            elif "average" in key_dict:
                if self.date == "today" or self.date == "yesterday":
                    key_dict = "passerby"
                    res = self.proximity(key_dict)
                    return (res)
            else:
                if self.date == "today" or self.date == "yesterday":
                    date = "hourly/" + self.date
                else:
                    date = "daily" #+ self.date
            URI = self.dict[key_dict] + date + "?siteId=" + str(self.siteid) + "&startDate=" + self.startDate + "&endDate=" + self.endDate
            res = self.doRequest(URI)
        except Exception:
            self.error()
            res = ""
            logging.error("An error happened in class Presence(): repeat_visitors()")
        return res
