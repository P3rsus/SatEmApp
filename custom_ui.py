""" Script handles custom Widgets """
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from custom_ui import *
from data_analysis import DataAnalysis

class ScrollableLabelInput(QWidget):
    def __init__(self, items, parent=None):
        QWidget.__init__(self, parent=parent)
        listBox = QVBoxLayout(self)
        self.setLayout(listBox)

        scroll = QScrollArea(self)
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollLayout.setAlignment(Qt.AlignTop)
        scrollContent.setLayout(scrollLayout)
        for item in items:
            scrollLayout.addWidget(item)
        scroll.setWidget(scrollContent)

class LabelInput(QWidget):
    """ Label with Input """

    def __init__(self, text, after_input_text="", digits=False, float=False, parent=None):
        QWidget.__init__(self, parent=parent)
        self.digits = digits

        lay = QHBoxLayout(self)

        lay.addWidget(QLabel(text))

        if self.digits:
            if float:
                self.textBox = QDoubleSpinBox()
                self.textBox.setDecimals(3)
            else:
                self.textBox = QSpinBox()
            self.textBox.setRange(0,9999)
        else:
            self.textBox = QLineEdit()
        lay.addWidget(self.textBox)

        if after_input_text != "":
            lay.addWidget(QLabel(after_input_text))
    
    def read(self):
        if self.digits:
            return self.textBox.value()
        else:
            return self.textBox.text()
    
    def write(self, t):
        if self.digits:
            self.textBox.setValue(t)
        else:
            self.textBox.setText(t)

class ScrollLabel(QScrollArea):
    """ Text Label with scroll capacity """

    # contructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def set_text(self, text):
        """ Setting text to the label"""

        self.label.setText(text)

class Button(QPushButton):
    """ Button Widget """

    def __init__(self, f, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.clicked.connect(f)

class FileDialog(QFileDialog):
    """ File Dialog - to choose files """

    def __init__(self, dtype, *args, **kwargs):
        QFileDialog.__init__(self, *args, **kwargs)
        self.setFileMode(QFileDialog.ExistingFile)
        self.setNameFilter(dtype)
        self.setViewMode(QFileDialog.Detail)

class Graphing(pg.PlotWidget):
    """ Graphing Widget """

    def __init__(self, *args, **kwargs):
        pg.PlotWidget.__init__(self, *args, **kwargs)
        self.setBackground('w')
        pen = pg.mkPen(color=(0, 0, 0))
        self.data_line = self.plot([], [], pen=pen)
    
    def set_title(self, s):
        self.setTitle(s, color="b", size="30pt")

    def update_plot_data(self, x, y):
        """ Update de Graph data """
        self.data_line.setData(x, y)