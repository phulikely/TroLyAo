import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QFrame, QLabel, QWidget,
                             QPushButton, QApplication, QGridLayout)
from PyQt5.QtCore import QCoreApplication, QThread, QObject, pyqtSignal
import bot_tieng_viet


class Gui(QWidget):

    stop_signal = pyqtSignal()  # make a stop signal to communicate with the worker in another thread

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Background
        self.setWindowIcon(QtGui.QIcon("bot.ico"))
        self.setFixedSize(800, 600)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        font = QtGui.QFont()
        font.setFamily("Century")
        self.setFont(font)
        self.setStyleSheet("background-color: rgb(23,33,45)")

        # Buttons:
        self.btn_start = QPushButton('Start', self)
        self.btn_start.setGeometry(240, 240, 301, 81)
        #self.btn_start.resize(self.btn_start.sizeHint())
        self.btn_start.move(50, 250)
        self.btn_start.setStyleSheet("background-color: rgb(255,255,255)")
        self.btn_stop = QPushButton('Stop', self)
        self.btn_stop.setGeometry(240, 240, 301, 81)
        #self.btn_stop.resize(self.btn_stop.sizeHint())
        self.btn_stop.move(450, 250)
        self.btn_stop.setStyleSheet("background-color: rgb(255,255,255)")

        # Label
        info = '© 2021 VMO JSC. All rights reserved.'
        self.label_1 = QLabel(info, self)
        self.label_1.move(285, 550)
        self.label_1.setStyleSheet("solid black;")

        # GUI title, size, etc...
        #self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Bot')
        #self.layout = QGridLayout()
        # self.layout.addWidget(self.btn_start, 0, 0)
        # self.layout.addWidget(self.btn_stop, 0, 50)
        # self.setLayout(self.layout)



        # Thread:
        self.thread = QThread()
        self.worker = Worker()
        self.stop_signal.connect(self.worker.stop)  # connect stop signal to worker stop method
        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.thread.quit)  # connect the workers finished signal to stop thread
        self.worker.finished.connect(self.worker.deleteLater)  # connect the workers finished signal to clean up worker
        self.thread.finished.connect(self.thread.deleteLater)  # connect threads finished signal to clean up thread

        self.thread.started.connect(self.worker.do_work)
        self.thread.finished.connect(self.worker.stop)

        # Start Button action:
        self.btn_start.clicked.connect(self.thread.start)

        # Stop Button action:
        self.btn_stop.clicked.connect(self.stop_thread)

        self.show()

    # When stop_btn is clicked this runs. Terminates the worker and the thread.
    def stop_thread(self):
        self.stop_signal.emit()  # emit the finished signal on stop

class Worker(QObject):

    finished = pyqtSignal()  # give worker class a finished signal

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)

    def do_work(self):

        bot_tieng_viet.bot_vnese()

        self.finished.emit()  # emit the finished signal when the loop is done

    def stop(self):
        bot_tieng_viet.run = False  # set the run condition to false on stop
        QCoreApplication.quit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())