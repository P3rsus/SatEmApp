from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
from data_analysis import DataAnalysis
import pyqtgraph.examples

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.data = DataAnalysis("/Users/pedrofonseca/Documents/CANSAT PROJECT/Cansat App Project/CansatData.txt", 10)
        self.data.clean()
        d = list(zip(*self.data.val_read()))

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        print(list(d[0]), list(d[5]))
        self.x = list(map(float, d[0]))
        self.y = list(map(float, d[5]))

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(0, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        
        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

        self.data.update(clean=True)
        d = list(zip(*self.data.val_read()))

        self.x = list(map(float, d[0]))
        self.y = list(map(float, d[5]))

        self.data_line.setData(self.x, self.y)  # Update the data.


"""app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())"""
pyqtgraph.examples.run()