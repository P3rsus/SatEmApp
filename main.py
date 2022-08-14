# pylint: disable=E1101
""" Main Script for the SatEmApp """
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from custom_ui import *
from data_analysis import DataAnalysis
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from scipy import stats
import math
import os
from multiprocessing import Process
import subprocess
import pickle


# Global Variables
FILE_PATH = None
DATA = None
LIVE = False
UPDATE_SPEED = 1000

class MainScreen(QMainWindow):
    """ Class that handles behavior of the Main Screen """

    def __init__(self, parent=None):
        super(MainScreen, self).__init__(parent)

        # Screen Setup Settings
        self.setWindowTitle("SatEmApp")
        self.setGeometry(100, 100, 600, 400)

        # Variables
        self.file_path = FILE_PATH = None
        self.prev_path = self.file_path
        self.data_prefs = None
        self.graph_screen = GraphScreen()

        # UI Components
        self.ui_components()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.scroll_label)
        layout.addWidget(self.select_data_button)
        layout.addWidget(self.show_graphs_button)
        layout.addWidget(self.broadcast_data_button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Timer Setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.loop)

        # Show
        self.show()

        # Timer (aka Loop) Start
        self.timer.start(UPDATE_SPEED)

    def loop(self):
        """ Function that takes care of repetitive actions """
        if self.file_path:
            global DATA
            if self.prev_path != self.file_path:
                DATA = DataAnalysis(self.file_path)
                DATA.clean()
                if not self.data_prefs:
                    self.data_prefs = DataPrefs()
                self.data_prefs.ready = False
            elif LIVE:
                DATA.update(clean=True)
            if self.data_prefs:
                if not self.data_prefs.ready:
                    self.data_prefs.show()
            self.prev_path = self.file_path
            self.scroll_label.set_text("\n".join(DATA.line_read(100)))
            with open("temp.txt", "wb") as t:
                pickle.dump(DATA, t)
        # self.timer.stop()

    def ui_components(self):
        """ Function that loads the ui components"""
        # creating scroll label
        self.scroll_label = ScrollLabel(self)

        # Select Data Button Object
        self.select_data_button = Button(
            self.open_file_dialog, "Select Data", self)
        
        # Show Graphs Button Object
        self.show_graphs_button = Button(
            self.show_graphs, "Show Graphs", self)
        
        self.broadcast_data_button = Button(
            self.broadcast_data, "Broadcast Data", self)

    def connect_screens(self):
        """ Allows to pass variables to other screen classes"""
        return self.file_path

    def open_file_dialog(self):
        """ Button Click Function - File Dialog """
        file_select = FileDialog("Text Document (*.txt *.csv *.asc)")
        if file_select.exec_():
            global FILE_PATH
            FILE_PATH = self.file_path = str(file_select.selectedFiles()[0])
    
    def show_graphs(self):
        if DATA:
            self.graph_screen.show()
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage("No data was found!")
    
    def broadcast_data(self):
        if DATA:
            subprocess.Popen("sh run_website.sh", shell=True)
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage("No data was found!")



class GraphScreen():
    """ Class that handles behavior of the Graphs Screen """

    def __init__(self, parent=None):
        style.use("seaborn")
    
    def calcVelocityAcceleration(self, time, altitude):
        t = []
        v = []
        for i in range(len(time)-3):
            inttempo = time[i+3] - time[i]
            desl = altitude[i+3] - altitude[i]
            vel = desl/inttempo
            tim = time[i+3]
            t.append(tim)
            v.append(vel)
        return t, v
    
    def acceleration(self, time, vel):
        t = []
        a = []
        for i in range(len(time)-3):
            inttempo = time[i+3] - time[i]
            varia = vel[i+3] - vel[i]
            ace = varia/inttempo
            tim = time[i+3]
            t.append(tim)
            a.append(ace)
        return t, a
        
    
    def show(self):

        sep = DATA.val_read()
        time = list(map(lambda x: x/1000, list(map(float, sep[0]))))
        mpu_temp = list(map(float, sep[1]))
        accel = list(map(float, sep[2]))
        airQuality = list(map(lambda x: 100-x/1023*100, map(float, sep[3])))
        press = list(map(float, sep[4]))
        temp = list(map(float, sep[5]))
        alt = list(map(float, sep[6]))
        co = list(map(float, sep[7]))
        humidity = list(map(float, sep[8]))
        uv = list(map(float, sep[9]))
        latitude = list(map(float, sep[10]))
        longitude = list(map(float, sep[11]))

        tVel, velocity = self.calcVelocityAcceleration(time, alt)
        tAcc, aceleration = self.acceleration(tVel, velocity)

        print(np.mean(airQuality[-10:]))
        print(latitude[-1], longitude[-1])

        a = plt.figure("Satemlat (Tempo/Velocidade)")
        tempoVelGraph = a.add_subplot(111)
        b = plt.figure("Satemlat (Altitude/Pressão)")
        altPresGraph = b.add_subplot(111)
        c = plt.figure("Satemlat (Altitude/Temperatura)")
        altTempGraph = c.add_subplot(111)
        d = plt.figure("Satemlat (Tempo/Temperatura)")
        tempoOxiGraph = d.add_subplot(111)
        e = plt.figure("Satemlat (Tempo/Humidity)")
        tempoUvGraph = e.add_subplot(111)
        f = plt.figure("Satemlat (Tempo/Altitude)")
        tempoAltGraph = f.add_subplot(111)
        g = plt.figure("Satemlat (Tempo/CO2)")
        tempAltGraph = g.add_subplot(111)

        tVEL = velocity
        tTEMPO = tVel
        tempoVelGraph.plot(tTEMPO, tVEL)
        tempoVelGraph.set_title("Velocity/Time")
        tempoVelGraph.set_xlabel("Time (s)")
        tempoVelGraph.set_ylabel("Velocity ± 0.01 (m/s)")

        tPRS = time
        tALT = list(map(lambda x: x/22, airQuality))
        #tPRS, tALT = remOutliers(prs, alt, 0.5)
        altPresGraph.plot(tPRS, tALT)
        #altPresGraph.invert_xaxis()
        altPresGraph.set_title("Air Quality Index/Time")
        altPresGraph.set_ylabel("Air Quality Index")
        altPresGraph.set_xlabel("Time (s)")

        tTEMP = temp
        tALT = alt
        #tTEMP, tALT = remOutliers(tmp, alt, 0.5)
        altTempGraph.scatter(tALT, tTEMP, s=8)
        altTempGraph.set_title("Altitude/Temperature")
        #altTempGraph.invert_xaxis()
        altTempGraph.set_ylabel("Temperature ± 0.01 (ºC)")
        altTempGraph.set_xlabel("Altitude ± 0.01 (m)")

        tTEMP = temp
        tTEMPO = time
        #tTEMP, tALT = remOutliers(tmp, alt, 0.5)
        tempAltGraph.plot(tTEMPO, tTEMP)
        tempAltGraph.set_title("Temperature/Time")
        #altTempGraph.invert_xaxis()
        tempAltGraph.set_ylabel("Temperature ± 0.01 (ºC)")
        tempAltGraph.set_xlabel("Time (s)")

        tTEMPO = time
        tHUMIDITY = humidity
        #tTEMPO, tOXIGENIO = remOutliers(tempo, concOxigenio, 1)
        tempoOxiGraph.plot(tTEMPO, tHUMIDITY)
        tempoOxiGraph.set_title("Humidity/Time")
        tempoOxiGraph.set_xlabel("Time (s)")
        tempoOxiGraph.set_ylabel("Humidity ± 0.01 (%)")

        tTEMPO = time
        tALTITUDE = alt
        #tTEMPO, tALTITUDE = remOutliers(tempo, alt, 0.5)
        tempoAltGraph.plot(tTEMPO, tALTITUDE)
        tempoAltGraph.set_title("Altitude/Time")
        tempoAltGraph.set_xlabel("Time (s)")
        tempoAltGraph.set_ylabel("Altitude ± 0.01 (m)")


        tTEMPO = time
        tCO = co
        #tTEMPO, tUV = remOutliers(tempo, uvIntensidade, 0.5)
        tempoUvGraph.plot(tTEMPO, tCO)
        tempoUvGraph.set_title("CO2/Time")
        tempoUvGraph.set_xlabel("Time (s)")
        tempoUvGraph.set_ylabel("CO2 ± 1 (ppm)")

        plt.show()

    def loop(self):
        """ Function that takes care of repetitive actions """
        if DATA:
            sep = DATA.val_read()
            time = list(map(float, sep[0]))
            uv = list(map(float, sep[2]))
            o = list(map(float, sep[3]))
            t = list(map(float, sep[5]))
            p = list(map(float, sep[6]))
            a = list(map(float, sep[7]))
            self.ap.update_plot_data(a, p)
            self.at.update_plot_data(a, t)
            self.to.update_plot_data(time, o)
            self.ti.update_plot_data(time, uv)
            self.ta.update_plot_data(time, a)


        # self.timer.stop()

    def ui_components(self):
        """ Function that loads the ui components"""
        self.ap = Graphing()
        self.ap.set_title("Altitude/Pressão")
        self.at = Graphing()
        self.at.set_title("Altitude/Temperatura")
        self.to = Graphing()
        self.to.set_title("Tempo/Oxigénio")
        self.ti = Graphing()
        self.ti.set_title("Tempo/Intensidade UV")
        self.ta = Graphing()
        self.ta.set_title("Tempo/Altitude")


class DataPrefs(QMainWindow):

    def __init__(self, parent=None):
        super(DataPrefs, self).__init__(parent)

        # Screen Setup Settings
        self.setWindowTitle("Data Preferences")
        self.setGeometry(100, 100, 600, 400)

        # Variables
        self.file_path = FILE_PATH
        self.ready = False

        # Saving & Loading
        self.settings = QSettings("Pedro Fonseca", "DataPreferences")

        # UI Components
        self.ui_components()

        # Layout
        self.main_layout = QVBoxLayout()

        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.amount_variables)
        self.top_layout.addWidget(self.set)
        self.top_layout.addWidget(self.detect)
        self.top_widget = QWidget()
        self.top_widget.setLayout(self.top_layout)
        self.main_layout.addWidget(self.top_widget)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.naming_variables)

        self.right_side = QVBoxLayout()
        self.right_side.addWidget(self.live_check)
        self.right_side.addWidget(self.upd_spd)
        self.right_side.addWidget(self.preview_button)
        self.right_side.addWidget(self.preference_name)

        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.addWidget(self.load_button)
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.okay_button)
        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(self.buttons_layout)
        self.right_side.addWidget(self.buttons_widget)
        self.right_side_widget = QWidget()
        self.right_side_widget.setLayout(self.right_side)
        self.bottom_layout.addWidget(self.right_side_widget)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_layout)

        self.main_layout.addWidget(self.bottom_widget)

        self.layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def ui_components(self):
        """ Function that loads the ui components"""
        global DATA

        ## Label Amount Variables
        self.amount_variables = LabelInput("Amount Variables", digits=True)
        self.amount_variables.textBox.setMinimum(1)
        self.amount_variables.write(DATA.amount_variables)

        ## Auto Detect Button
        self.detect = Button(self.auto_detect, "Auto Detect", self)

        ## Set Button
        self.set = Button(self.update, "Set", self)

        ## Scrollable LabelInputs
        self.l = [LabelInput(f"Variable{str(i+1)}") for i in range(DATA.amount_variables)]
        [x.write(DATA.naming[ind]) for (ind, x) in enumerate(self.l)]
        self.naming_variables = ScrollableLabelInput(self.l)

        ## Okay Button
        self.okay_button = Button(self.okay, "Okay", self)
        self.okay_button.setDefault(True)
        self.okay_button.setFocus()

        ## Live Check
        self.live_check = QCheckBox("Live Data")
        self.live_check.stateChanged.connect(self.checkbox_live)

        ## Update speed
        self.upd_spd = LabelInput("Update every", "seconds", digits=True, float=True)
        self.upd_spd.textBox.setMinimum(0)
        self.upd_spd.write(UPDATE_SPEED/1000)
        self.upd_spd.textBox.setEnabled(LIVE)

        ## Preference Name
        self.preference_name = LabelInput("Preference Name: ")
        self.preference_name.write("Default")

        ## Save Button
        self.save_button = Button(self.save, "Save Preferences", self)

        ## Load Previous Button
        self.load_button = Button(self.load, "Load Previous", self)

        ## Preview Button
        self.preview_button = Button(self.preview, "Preview", self)

        ## Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(f"{str(DATA.amount_variables)} variables - {DATA.cleaned_lines}/{DATA.lines} lines ({round(DATA.cleaned_lines/DATA.lines*100, 1)}%)")
    
    def preview(self):
        self.amount_variables.write(DATA.amount_variables)
        self.update()
        self.table = DataPrefsPreview(DATA.val_read(), DATA.naming)
        self.table.show()

    def checkbox_live(self, state):
        global LIVE
        if (QtCore.Qt.Checked == state):
            LIVE = True
        else:
            LIVE = False
        self.upd_spd.textBox.setEnabled(LIVE)

    def save(self):
        self.settings.setValue("amount_variables", self.amount_variables.read())
        l = [x.read() for x in self.l]
        self.settings.setValue("variable_names", l)
        self.settings.setValue("live_data", LIVE)
        self.settings.setValue("update_speed", self.upd_spd.read())
        self.settings.setValue("preference_name", self.preference_name.read())
    
    def load(self):
        self.amount_variables.write(self.settings.value("amount_variables"))
        self.update()
        [x.write(self.settings.value("variable_names")[ind]) for (ind, x) in enumerate(self.l)]
        self.bottom_layout.removeWidget(self.naming_variables)
        self.naming_variables = ScrollableLabelInput(self.l)
        self.bottom_layout.insertWidget(0, self.naming_variables)
        global LIVE
        LIVE = self.settings.value("live_data")
        self.live_check.setChecked(True)
        self.upd_spd.write(self.settings.value("update_speed"))
        self.preference_name.write(self.settings.value("preference_name"))


    def auto_detect(self):
        global DATA
        self.amount_variables.write(DATA.detect_amount_variables())
        self.update()
    
    def okay(self):
        DATA.naming = [x.read() for x in self.l]
        UPDATE_SPEED = self.upd_spd.read() * 1000
        self.ready = True
        self.close()
    
    def update(self):
        ## Updates Status Bar & Data Handling
        global DATA
        DATA.naming = [x.read() for x in self.l]
        DATA.change_amount_variables(int(self.amount_variables.read()))
        DATA.update(clean=True)
        self.statusBar.showMessage(f"{str(DATA.amount_variables)} variables - {DATA.cleaned_lines}/{DATA.lines} lines ({round(DATA.cleaned_lines/DATA.lines*100, 1)}%)")

        ## Updates Naming Variable Amount
        self.bottom_layout.removeWidget(self.naming_variables)
        self.l = [LabelInput(f"Variable{str(i+1)}") for i in range(DATA.amount_variables)]
        [x.write(DATA.naming[ind]) for (ind, x) in enumerate(self.l)]
        self.naming_variables = ScrollableLabelInput(self.l)
        self.bottom_layout.insertWidget(0, self.naming_variables)


class DataPrefsPreview(QMainWindow):
    def __init__(self, data, naming=None, parent=None, *args):
        super(DataPrefsPreview, self).__init__(parent)

        self.data = data
        self.naming = naming

        self.setWindowTitle("Data Preferences - Preview")
        self.setGeometry(100, 100, 600, 400)

        self.ui_components()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.show()

    def ui_components(self):
        self.table = QTableWidget(len(self.data[0]), len(self.data))
        if not self.naming:
            self.naming = ["" for _ in range(len(self.data))]
        for n, vals_col in enumerate(self.data):
            for m, item in enumerate(vals_col):
                newitem = QTableWidgetItem(item)
                self.table.setItem(m, n, newitem)
        self.table.setHorizontalHeaderLabels([x if x!="" else f"Unnamed{str(ind+1)}" for (ind, x) in enumerate(self.naming)])
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

if __name__ == "__main__":
    #Create temp data
    t = open("temp.txt","w+")
    t.close()

    # Initialize PyQt5
    app = QApplication(sys.argv)

    # Initialize
    main_screen = MainScreen()

    # Run Event Loop
    app.exec_()

    #Delete temp data
    os.remove("temp.txt")


