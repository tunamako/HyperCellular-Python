from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from poincareview import PoincareView

import sys

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.hbox = QHBoxLayout()
		#self.hbox.addWidget() 						#lefthand side, ui elements
		self.hbox.addWidget(PoincareView())	
		self.hbox.setContentsMargins(0, 0, 0, 0)
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