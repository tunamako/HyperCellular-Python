from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pcviewmodel import PoincareViewModel
from controller import CellularController

import sys

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.model = PoincareViewModel()
		self.controller = CellularController(self)


		self.hbox = QHBoxLayout()
		self.hbox.addWidget(self.controller)
		self.hbox.addWidget(self.model)	
		self.hbox.setContentsMargins(0, 0, 0, 0)
		self.hbox.setStretch(0, 1)
		self.hbox.setStretch(1, 3)

		widget = QWidget()
		widget.setLayout(self.hbox)

		self.setCentralWidget(widget)
		self.setWindowTitle('QT Testing')
		self.setBaseSize(500, 500)    
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())
