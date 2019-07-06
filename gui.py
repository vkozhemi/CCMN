from tkinter import *
from tkinter import ttk
import numpy as np
from self import self

import presence
import map
import my_calendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import threading
import logging
import time
import tkinter as tk
from tkinter import *

class Gui:
    self.LOG_FILENAME = 'logging_example'
    logging.basicConfig(filename=self.LOG_FILENAME, level=logging.ERROR, filemode="w")

    try:

        def __init__(self, master):
            self.message = StringVar()
            self.list1 = {}
            self.pres = presence.Presence()
            self.map = map.Map()
            self.root = master
            self.root.configure(background='white')

            self.nbMain = ttk.Notebook(self.root)
            self.nbMain.grid(row=4, column=0, columnspan=5, sticky='NESW')
            self.presFrame = Frame(self.nbMain)
            self.mapFrame = Frame(self.nbMain)

            self.nbMain.add(self.presFrame, text='Presence')
            self.nbMain.add(self.mapFrame, text='Map')
            # ----------------------------------------------------------Presence----------------------------------------------------
            self.listbox = Listbox(self.presFrame, font=('AppleGothic', 14, 'bold'), bd=0, fg='#ffffff', width=24, height=5)
            self.listbox2 = Listbox(self.presFrame, font=('AppleGothic', 14, 'bold'), bd=0, fg='#ffffff', width=24, height=5)
            self.colors = ['#FFA31A', '#B90F56', '#7C2CA8', '#5FCFF8', '#40CC9B']
            self.changeColors = ['#FFA311', '#B90F51', '#7C2CA1', '#5FCFF1', '#40CC91']
            self.listBoxColors = ['#FF931A', '#a90F56', '#6C2C98', '#5FbFf8', '#40bC9B']

            self.colors2 = ['#990F57', '#5C2CA9', '#4FBFE8']
            self.changeColors2 = ['#990F52', '#5C2CA2', '#4FBFE1']
            self.listBoxColors2 = ['#890F57', '#4C2C99', '#2FAFD8']

            self.dates = {'Today': 'today', 'Yesterday': 'yesterday', 'This week': 'lastweek',
                          'This month': 'lastmonth', 'Custom': 'nothing'}
            self.calendarStart = my_calendar.Calendar(master=self.presFrame, firstweekday=my_calendar.calendar.MONDAY)
            self.calendarEnd = my_calendar.Calendar(master=self.presFrame, firstweekday=my_calendar.calendar.MONDAY)
            self.calendarButton = Button(self.presFrame, text='OK', command=self.setDate)

            self.labels = []
            self.labelNames = ['Total visitors ', 'Average Dwell Time ', 'Peak Hour ', 'Conversion Rate ',
                               'Top Device Maker']
            self.labelListNames = [
                ['Unique visitors ', 'Total visitors ', 'Total connected ', '% of connected visitors '],
                ['5-30 mins ', '30-60 mins ', '1-5 hours ', '5-8 hours ', '8+ hours '],
                ['Visitor count in peak hour '],
                ['Conversion Rate ', 'Total Visitors ', 'Total Passersby '],
                ['Top1', 'Top2', 'Top3', 'Top4', 'Top5']
            ]
            self.labelListVals = [[1, 1, 1, 1], [1, 1, 1, 1, 1], [1], [1, 1, 1], [1, 1, 1, 1, 1]]

            for i in range(5):
                self.labels.append(
                    Label(master=self.presFrame, text=self.labelNames[i], font=('AppleGothic', 24, 'bold'), bd=0, bg=self.colors[i], fg='#ffffff',
                          width=15, height=1))
                self.labels[i].bind('<Button-1>', self.listBoxFunc)

            self.comboExample = ttk.Combobox(self.presFrame, width=24, state='readonly',
                                             values=['Today', 'Yesterday', 'This week', 'This month', 'Custom'])
            self.comboExample.current(0)
            print(self.comboExample.current(), self.comboExample.get())
            self.comboExample.bind('<<ComboboxSelected>>', self.callbackFunc)

            self.fig = Figure(figsize=(14.4, 5), dpi=100, facecolor='white')
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.presFrame)

            self.comboExample.grid(row=0, column=2, columnspan=1)
            for labl in self.labels:
                labl.grid(row=1, column=self.labels.index(labl))

            self.figs = []
            self.canvs = []
            self.gs = []
            self.toolBarFrames = []
            self.toolBars = []
            self.graphFrames = []
            self.graphicNames = ['Proximity', 'Dwell Time', 'Repeat Visitors']
            self.subplots = [[], [], []]

            self.nbPres = ttk.Notebook(self.presFrame)
            self.nbPres.grid(row=5, column=0, columnspan=5, sticky='NESW')

            # # ======================================== INSIGHTS ============================================================

            self.labelNames_insights = ['Yesterday', 'Today', 'Tomorrow']
            self.labelListNames_insights = [
                ['passerby ', 'visitors ', 'connected ', 'peak hour ', 'peak visitors '],
                ['passerby ', 'visitors ', 'connected ', 'peak hour ', 'peak visitors '],
                ['passerby ', 'visitors ', 'connected ', 'peak hour ', 'peak visitors ']
            ]

            self.labelListVals_insights = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
            self.labels_insights = []

            self.pirateList = []

            for i in range(3):
                self.labels_insights.append(
                    Label(master=self.presFrame, text=self.labelNames_insights[i], font=('AppleGothic', 24, 'bold'), bd=0,
                          bg=self.colors2[i], fg='#ffffff',
                          width=15, height=1))
                self.labels_insights[i].bind('<Button-1>', self.listBoxFunc2)

            for lab in self.labels_insights:
                lab.grid(row=3, column=self.labels_insights.index(lab) + 1)


            self.graphics()
            self.labelUpdate()
            # self.notification()
            # ==============================================================================================================

    # ----------------------------------------------------------Map---------------------------------------------------------

            # ============================================= NOTIFICATON ====================================================
            self.thread_notification = threading.Thread(target=self.map.proc_notification, name="proc_notification")
            self.thread_notification.start()
            self.thread_notification2 = threading.Thread(target=self.notification, name="notification")
            self.thread_notification2.start()
            self.thread_notification4 = threading.Thread(target=self.updateFloorThread, name="updateFloorThread")
            self.thread_notification4.start()
            # ==============================================================================================================


            self.img_tk = self.map.get_image_floor('1_Floor')
            self.canvas = Canvas(self.mapFrame, width=self.map.width, height=self.map.height, bg='pink')
            self.canvas.grid(row=0, column=1, rowspan=3)
            self.canvas.create_image(0, 0, image=self.img_tk, anchor=NW)

            self.floorLabels = []
            self.floorLabelNames = ['1_Floor', '2_Floor', '3_Floor']
            for i in range(3):
                self.floorLabels.append(Label(master=self.mapFrame, text=self.floorLabelNames[i],
                    font=('AppleGothic', 24, 'bold'), bd=0, bg=self.colors[i], fg='#ffffff', width=15, height=1))
                self.floorLabels[i].bind('<Button-1>', self.changeFloor)
                self.floorLabels[i].grid(row=i, column=0)

            self.getMacLogin()
            self.pirate = self.canvas.create_oval(0, 0, 0, 0, width=2, fill='green')

            self.infoFrame = Frame(self.mapFrame)
            self.infoFrame.grid(row=1, column=2, rowspan=3, columnspan=2)

            self.labelListInfoKeysNames = ['userName', 'mac_addres', 'Floor', 'manufacturer', 'statistics']
            self.labelListInfoKeys = []
            for i in range(len(self.labelListInfoKeysNames)):
                self.labelListInfoKeys.append(Label(master=self.infoFrame, text=self.labelListInfoKeysNames[i],
                    font=('AppleGothic', 20, 'bold'), bd=0, fg=self.colors[3], width=25, height=1))
                self.labelListInfoKeys[i].grid(row=i*2, column=0)

            self.labelListInfoValsNames = [' ', ' ', ' ', ' ', ' ']
            self.labelListInfoVals = []
            for i in range(len(self.labelListInfoValsNames)):
                self.labelListInfoVals.append(Label(master=self.infoFrame, text=self.labelListInfoValsNames[i],
                                                    font=('AppleGothic', 15, 'bold'), bd=0, width=25, height=1))
                self.labelListInfoVals[i].grid(row=i*2 + 1, column=0)


            self.labelNotific = Label(self.mapFrame, text="NOTIFICATION:", bg=self.colors[3], font=('AppleGothic', 20, 'bold'),
                          fg='#ffffff', width=17, height=1)
            self.labelNotific.grid(row=4, column=0)

        #===========================================================================================================================================
        def printf(self):
            self.list1 = self.map.search_username(self.message.get())
            self.showInfo()


        def getMacLogin(self):
            message_entry = Entry(self.mapFrame, textvariable=self.message, width=20, font='Arial 14')
            # message_entry.place(relx=.9, rely=.0, anchor="ne")
            message_button = Button(self.mapFrame, text="Search", command=self.printf)
            # message_button.place(relx=.9, rely=.0, anchor="nw")
            message_entry.grid(row=0, column=2)
            message_button.grid(row=0, column=3)


        def showInfo(self):

            if self.list1:
                list2 = list(self.list1.values())
                self.map.floor = self.map.find_floor(self.message.get())[:1] + "_Floor"
                
                # print(list2)
                self.labelListInfoValsNames[0] = list2[0]
                self.labelListInfoValsNames[1] = list2[1]
                self.labelListInfoValsNames[2] = self.map.floor[:1]
                self.labelListInfoValsNames[3] = list2[5]
                self.labelListInfoValsNames[4] = list2[6]['lastLocatedTime'][:10] + " " + list2[6]['lastLocatedTime'][11:19]


                if not list2[4]:
                    return

                self.canvas.delete(self.pirate)
                self.pirateList = [round(list2[4]['x']) * 0.563, round(list2[4]['y']) * 0.582, (round(list2[4]['x']) + 14) * 0.563, (round(list2[4]['y']) + 14) * 0.582]
                self.pirate = self.canvas.create_oval(self.pirateList, width=2, fill='green')
            else:
                self.labelListInfoValsNames = ['Not found','','','','']
            for i in range(len(self.labelListInfoVals)):
                self.labelListInfoVals[i].configure(text=self.labelListInfoValsNames[i])

        def notification(self):
            while self.map.threadLoop:
                time.sleep(1)
                label2 = Label(self.mapFrame, text=self.map.mac_or_login, font=('AppleGothic', 20, 'bold'), fg=self.colors[1])
                self.mac_or_login = "                                                                              "
                # label2.place(x=210, y=650, anchor="nw")
                label2.grid(row=4, column=1)

        def setDate(self):
            if self.calendarStart.date > self.calendarEnd.date:
                self.pres.startDate = self.calendarEnd.date.strftime('%Y-%m-%d')
                self.pres.endDate = self.calendarStart.date.strftime('%Y-%m-%d')
            else:
                self.pres.startDate = self.calendarStart.date.strftime('%Y-%m-%d')
                self.pres.endDate = self.calendarEnd.date.strftime('%Y-%m-%d')
            self.labelUpdate()

        def callbackFunc(self, event):
            if event.widget.get() == 'Custom':
                self.pres.date = ''
                self.calendarStart.grid(row=0, column=1, columnspan=1)
                self.calendarEnd.grid(row=0, column=3, columnspan=1)
                self.calendarButton.grid(row=0, column=4)
            else:
                self.pres.date = self.dates[event.widget.get()]
                self.calendarStart.grid_remove()
                self.calendarEnd.grid_remove()
                self.calendarButton.grid_remove()
                self.labelUpdate()
            # print(event.widget.get())

        def updateFloorThread(self):
            while self.map.threadLoop:
                self.updateFloor()
                time.sleep(10)

        def updateFloor(self):
            # self.img_tk = self.map.get_image_floor(self.map.floor)
            # self.canvas.create_image(0, 0, image=self.img_tk, anchor=NW)

            list_all = self.map.show_all_user_floor(self.map.floor[:1])
            # print('----------------\n', list_all, '\n--------------------')
            self.img_tk = self.map.get_image_floor(self.map.floor)
            self.canvas.create_image(0, 0, image=self.img_tk, anchor=NW)
            for item in list_all:
                # print(item)
                list2 = list(item.values())
                self.canvas.create_oval(round(list2[4]['x']) * 0.563, round(list2[4]['y']) * 0.582,
                                        (round(list2[4]['x']) + 14) * 0.563,
                                        (round(list2[4]['y']) + 14) * 0.582, width=2, fill='purple')
            if self.pirateList:
                self.canvas.create_oval(self.pirateList, width=2, fill='green')

        def changeFloor(self, event):
            self.map.floor = event.widget['text']
            self.updateFloor()

        def listBoxFunc(self, event):
            self.listbox.delete(0, self.listbox.size())
            self.listbox.grid_forget()
            for i in range(5):
                if event.widget['bg'] == self.colors[i]:
                    event.widget['bg'] = self.changeColors[i]
                    self.listbox['bg'] = self.listBoxColors[i]
                    for item in self.labelListVals[i]:
                        self.listbox.insert(END, item)
                    self.listbox.grid(row=2, column=i)
                    return 1
            for i in range(5):
                if event.widget['bg'] == self.changeColors[i]:
                    event.widget['bg'] = self.colors[i]


        def listBoxFunc2(self, event):
            self.listbox2.delete(0, self.listbox2.size())
            self.listbox2.grid_forget()
            for i in range(3):
                if event.widget['bg'] == self.colors2[i]:
                    event.widget['bg'] = self.changeColors2[i]
                    self.listbox2['bg'] = self.listBoxColors2[i]
                    for item in self.labelListVals_insights[i]:
                        self.listbox2.insert(END, item)
                    self.listbox2.grid(row=4, column=i+1)
                    return 1
            for i in range(3):
                if event.widget['bg'] == self.changeColors2[i]:
                    event.widget['bg'] = self.colors2[i]


        def labelUpdate(self):

            totalVis = self.pres.total_visitors()
            for i in range(len(self.labelListNames[0])):
                self.labelListVals[0][i] = self.labelListNames[0][i] + str(totalVis[i])
            self.labels[0].configure(text=self.labelNames[0] + str(totalVis[1]))

            dwellTime = self.pres.average_dwell_time()
            for i in range(len(self.labelListNames[1])):
                self.labelListVals[1][i] = self.labelListNames[1][i] + str(dwellTime[i])

            peakHour = self.pres.peak_hour()
            self.labelListVals[2][0] = self.labelListNames[2][0] + str(peakHour[1])
            self.labels[2].configure(text=self.labelNames[2] + str(peakHour[0]))

            convRate = self.pres.conversion_rate()
            for i in range(len(self.labelListNames[3])):
                self.labelListVals[3][i] = self.labelListNames[3][i] + str(convRate[i])
            self.labels[3].configure(text=self.labelNames[3] + str(convRate[0]) + '%')

            topDev = self.pres.top_device_maker()
            for i in range(len(self.labelListNames[4])):
                self.labelListVals[4][i] = str(topDev[i][0]) + str(topDev[i][1])
            self.labels[4].configure(text=str(topDev[0][0]) + str(topDev[1][1]))

# ======================================== INSIGHTS ====================================================================
#             print("\n=================== YESTERDAY ===============")
            insights_yesterday = self.pres.insights_yesterday()
            for i in range(len(self.labelListNames_insights[0])):
                self.labelListVals_insights[0][i] = self.labelListNames_insights[1][i] + str(insights_yesterday[i])
            self.labels_insights[0].configure(text=self.labelNames_insights[0])
            # print("passerby, visitors, connected, peak_hour, peak visitors", insights_yesterday)

            # print("\n=================== TODAY ===================")
            insights_today = self.pres.insights_today()
            for i in range(len(self.labelListNames_insights[1])):
                self.labelListVals_insights[1][i] = self.labelListNames_insights[1][i] + str(insights_today[i])
            self.labels_insights[1].configure(text=self.labelNames_insights[1])
            # print("passerby, visitors, connected, peak_hour, peak visitors", insights_today)

            # print("\n=================== TOMORROW (FORECAST) =====")
            insights_tomorrow = self.pres.insights_tomorrow()
            for i in range(len(self.labelListNames_insights[2])):
                self.labelListVals_insights[2][i] = self.labelListNames_insights[2][i] + str(insights_tomorrow[i])
            self.labels_insights[2].configure(text=self.labelNames_insights[2])
            # print("passerby, visitors, connected, peak_hour, peak visitors", insights_tomorrow)
# ======================================================================================================================
            for plt in self.subplots:
                for subplot in plt:
                    subplot.cla()

            self.proximityGraph()
            self.dwellTimeGraph()
            self.repeatVisitorsGraph()

            for i in range(3):
                self.canvs[i].draw()


        def graphics(self):
            for i in range(3):
                self.graphFrames.append(Frame(self.nbPres))
                self.nbPres.add(self.graphFrames[i], text=self.graphicNames[i])
                self.figs.append(Figure(figsize=(12.2, 5), dpi=100, facecolor='white'))
                self.canvs.append(FigureCanvasTkAgg(self.figs[i], master=self.graphFrames[i]))
                self.gs.append(self.figs[i].add_gridspec(2, 3, height_ratios=[4, 1], wspace=0.1, hspace=0.1, left=0.05))

                self.subplots[i].append(self.figs[i].add_subplot(self.gs[i][0, :-1]))
                self.subplots[i].append(self.figs[i].add_subplot(self.gs[i][1, :-1]))
                self.subplots[i].append(self.figs[i].add_subplot(self.gs[i][:, 2]))

                self.toolBarFrames.append(Frame(master=self.graphFrames[i]))
                self.toolBars.append(NavigationToolbar2Tk(self.canvs[i], self.toolBarFrames[i]))

                self.canvs[i].get_tk_widget().grid(row=0, column=0, columnspan=5, rowspan=1)
                self.toolBarFrames[i].grid(row=1, column=0, columnspan=5)

        def proximityGraph(self):

            data_names = ['passerby', 'visitor', 'connected']
            passerby = self.pres.proximity('passerby')
            visitor = self.pres.proximity('visitor')
            connected = self.pres.proximity('connected')
            dist = [self.pres.proximity('passerby_dist'), self.pres.proximity('visitor_dist'),
                    self.pres.proximity('connected_dist')]

            # ---------------------------------------------------- СТОЛБИКИ ----------------------------------------------
            self.subplots[0][0].yaxis.grid(True, zorder=1)
            self.subplots[0][0].bar([x for x in range(len(list(passerby.values())))], list(passerby.values()), width=0.2,
                      color=self.colors[2], alpha=0.7, label='passerby', zorder=2)
            self.subplots[0][0].bar([x + 0.3 for x in range(len(list(visitor.values())))], list(visitor.values()), width=0.2,
                      color=self.colors[0], alpha=0.7, label='visitor', zorder=2)
            self.subplots[0][0].bar([x + 0.6 for x in range(len(list(connected.values())))], list(connected.values()), width=0.2,
                      color=self.colors[1], alpha=0.7, label='connected', zorder=2)

            self.subplots[0][0].set_xticks([x for x in range(len(passerby))], data_names)
            self.subplots[0][0].legend(loc='upper right')
            # ---------------------------------------------------- --------- ----------------------------------------------
            # ------------------------------------------------------ ЛИНИИ ------------------------------------------------
            self.subplots[0][1].plot([x for x in range(len(list(passerby.values())))], list(passerby.values()),
                       marker='o', color=self.colors[1])
            # ---------------------------------------------------- --------- ----------------------------------------------
            # ---------------------------------------------------- ДИАГРАММЫ ----------------------------------------------
            self.subplots[0][2].pie(dist, autopct='%.1f', radius=1.1, explode=[0.15] + [0 for _ in range(len(data_names) - 1)],
                      colors=self.colors)
            # ---------------------------------------------------- --------- ----------------------------------------------

        def dwellTimeGraph(self):
            data_names = ['5-30 mins', '30-60 mins', '1-5 hours', '5-8 hours', '8+ hours']
            dwell = self.pres.dwell_time('dwell')
            dwellTime = []
            for item in dwell:
                for k in dwell[str(item)]:
                    dwellTime.append([dwell[str(item)][key] for item in dwell for key in dwell[str(item)] if key == k])
            hours = np.arange(len(dwellTime[0]))
            dwellDist = list(self.pres.dwell_time('dwell_dist').values())

            # ----------------------------------------------- ЛИНИИ С ЗАПОЛНЕНИЕМ -----------------------------------------
            self.subplots[1][0].stackplot(hours, dwellTime[0], dwellTime[1], dwellTime[2], dwellTime[3], dwellTime[4],
                                colors=self.colors, labels=data_names)
            self.subplots[1][0].legend(loc='upper left')
            self.subplots[1][0].set_xlim(left=hours[0], right=hours[-1])
            self.fig.tight_layout()
            # ----------------------------------------------- ------------------- -----------------------------------------
            # ------------------------------------------------------ ЛИНИИ ------------------------------------------------
            self.subplots[1][1].plot(hours, dwellTime[0], marker='o', color=self.colors[1])
            # ---------------------------------------------------- --------- ----------------------------------------------
            # ---------------------------------------------------- ДИАГРАММЫ ----------------------------------------------
            self.subplots[1][2].pie(dwellDist, autopct='%.1f', radius=1.1, explode=[0.15] + [0 for _ in range(len(data_names) - 1)],
                       colors=self.colors)
            # ---------------------------------------------------- --------- ----------------------------------------------

        def repeatVisitorsGraph(self):
            data_names = ['daily', 'weekly', 'occasional', 'first time', 'yesterday']
            repeat = self.pres.repeat_visitors('repeatvisitors')
            # print(repeat)
            repeatVisitors = []
            for item in repeat:
                for k in repeat[str(item)]:
                    repeatVisitors.append([repeat[str(item)][key] for item in repeat for key in repeat[str(item)] if key == k])
            hours = np.arange(len(repeatVisitors[0]))
            repeatDist = list(self.pres.repeat_visitors('repeatvisitors_dist').values())

            # ------------------------------------------------------ ЛИНИИ  -----------------------------------------------
            for i in range(5):
                self.subplots[2][0].plot(hours, repeatVisitors[i], marker='o', color=self.colors[i], label=data_names[i])
            self.subplots[2][0].legend(loc='upper right')
            self.fig.tight_layout()
            # ----------------------------------------------- ------------------- -----------------------------------------
            # ------------------------------------------------------ ЛИНИИ ------------------------------------------------
            self.subplots[2][1].plot(hours, repeatVisitors[0], marker='o', color=self.colors[1])
            # ---------------------------------------------------- --------- ----------------------------------------------
            # ---------------------------------------------------- ДИАГРАММЫ ----------------------------------------------
            self.subplots[2][2].pie(repeatDist, autopct='%.1f', radius=1.1, explode=[0.15] + [0 for _ in range(len(data_names) - 1)],
                         colors=self.colors)
            # ---------------------------------------------------- --------- ----------------------------------------------

    except Exception:
        logging.error("Happened something serious in class Gui():")


def on_closing():
    print("DESTROY")
    app.map.threadLoop = False
    app.thread_notification.join(1)
    app.thread_notification2.join(1)
    app.thread_notification4.join(1)
    app.root.destroy()


root = Tk()
root.title('Can catch me now ?')
# root.geometry('1000x1000+900+900')


app = Gui(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
