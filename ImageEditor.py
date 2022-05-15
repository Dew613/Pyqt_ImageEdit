"""
Dewan Sunnah


Resources used:
https://www.pythonguis.com/tutorials/pyqt-layouts/
    - referenced for combining QV and QH layouts

https://doc.qt.io/qtforpython/PySide6/QtWidgets/QFileDialog.html?highlight=qfiledialog
    - referenced for opening files
    - referenced for specifying file type

https://doc.qt.io/qtforpython/PySide6/QtGui/QPixmap.html?highlight=qpixmap#more
    - referenced for displaying an image in PyQt
    - docs said that Qpixmap is "designed and optimized" for displaying images so I used it over QImage
"""
   
import sys

# QT widgets import
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt

#QT gui imports
from PyQt5.QtGui import QPixmap


class Window(QMainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("PyQt Image Editor")
        self.setMinimumSize(750,500)
        #self.setCentralWidget(QLabel("I'm in the center, you all adore me"))
        self._presetLayout()
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction("&Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction("Exit", self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm a status bar!")
        self.setStatusBar(status)
# ============================================================================ Layout Settings ====================================================================

    def _presetLayout(self):
        windowLayout = QHBoxLayout()
        sidebar = self._createSidebarLayout()
        pictureBar = self._createPictureBarLayout()
        windowLayout.addLayout(sidebar)
        windowLayout.addLayout(pictureBar)
        widget = QWidget()
        widget.setLayout(windowLayout)
        self.setCentralWidget(widget)


    def _createSidebarLayout(self):
        """
        Creates the sidebar that has the image editing options
        """
        sidebar = QVBoxLayout()
        sidebar.addWidget(QPushButton("Button 1"))
        sidebar.addWidget(QPushButton("Button 2"))
        sidebar.addWidget(QPushButton("Button 3"))
        sidebar.addWidget(QPushButton("Button 4"))
        return sidebar

    def _createPictureBarLayout(self):
        """
        Creates the sidebar that views the image, also has upload and save buttons
        """
        pictureBar = QVBoxLayout()
        # scrollArea = QScrollArea()
        
        self.pictureLabel = QLabel("ImageLabel")
        # adds scroll since images might be too big
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.pictureLabel)
        uploadButton = QPushButton("Choose an Image")
        uploadButton.clicked.connect(self.getImage)
        pictureBar.addWidget(scrollArea)
        pictureBar.addWidget(uploadButton)
        pictureBar.addWidget(QPushButton("save image button"))
    
        
        return pictureBar

    def getImage(self):
        # opens in current directory
        # returns a tuple
        file_name = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg)" )
        # incase you cancel
        if file_name:
            #self.pictureLabel.setText(file_name[0])
            self.ImagePixmap = QPixmap(file_name[0])
            #self.pictureLabel.setPixmap(self.ImagePixmap.scaled(1000,800,  Qt.KeepAspectRatio))
            self.pictureLabel.setPixmap(self.ImagePixmap)
            self.pictureLabel.adjustSize()
            # self.pictureLabel.setScaledContents(True)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

