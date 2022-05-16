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
from PyQt5.QtWidgets import QAction

#QT gui imports
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QTransform
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QColor
from sklearn.datasets import load_files



class Window(QMainWindow):

    """
    Variables to keep in mind:
    originalFilePath: has the path to the original img
    originalImagePixmap: the original image
    imagePixmap: the current image
    """

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
        loadfile = QAction("Load img", self)
        tools.addAction(loadfile)
        loadfile.triggered.connect(self.getImage)
        resetImg = QAction("Reset img", self)
        tools.addAction(resetImg)
        resetImg.triggered.connect(self.resetImage)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("No image Loaded")
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

    def _setStatus(self, newText):
        status = QStatusBar()
        status.showMessage(newText)
        self.setStatusBar(status)

    def _displayImage(self):
        self.pictureLabel.setPixmap(self.imagePixmap)
        self.pictureLabel.adjustSize()
        self.pictureLabel.setAlignment(Qt.AlignCenter)



# ======================================================================= Sidebar Stuff ===================================

    def _createSidebarLayout(self):
        """
        Creates the sidebar that has the image editing options
        """
        sidebar = QVBoxLayout()
        sidebar.addWidget(self.createRotateClockwiseButton())
        sidebar.addWidget(self.createRotateCounterClockwiseButton())
        sidebar.addWidget(self.createBlackNWhiteButton())
        sidebar.addWidget(self.createGrayScaleButton())
        sidebar.addWidget(self.createResetImageButton())
        return sidebar

    def createRotateClockwiseButton(self):
        rotateButton = QPushButton("Rotate 90 Clockwise")
        rotateButton.clicked.connect(self.rotateImageClockwise)
        return rotateButton

    def createRotateCounterClockwiseButton(self):
        rotateButton = QPushButton("Rotate 90 Counter-Clockwise")
        rotateButton.clicked.connect(self.rotateImageCounterClockwise)
        return rotateButton

    def createBlackNWhiteButton(self):
        filterButton = QPushButton("Make Black and White")
        filterButton.clicked.connect(self.transformBlackNWhite)
        return filterButton

    def createGrayScaleButton(self):
        filterButton = QPushButton("Make Grayscale")
        filterButton.clicked.connect(self.transformGrayScale)
        return filterButton

    def createResetImageButton(self):
        resetButton = QPushButton("Reset the Image")
        resetButton.clicked.connect(self.resetImage)
        return resetButton
    
    def resetImage(self):
        self.imagePixmap = self.originalImagePixmap
        self.pictureLabel.setPixmap(self.imagePixmap)
        self.pictureLabel.adjustSize()
        self._setStatus("Reset the image")

    def rotateImageClockwise(self):
        if self.originalImagePixmap:
            rotateTransform = QTransform()
            rotateTransform.rotate(90)
            self.imagePixmap = self.imagePixmap.transformed(rotateTransform)
            self.pictureLabel.setPixmap(self.imagePixmap)
            self.pictureLabel.adjustSize()
        self._setStatus("Rotated the image 90 degrees Clockwise")

    def rotateImageCounterClockwise(self):
        if self.originalImagePixmap:
            rotateTransform = QTransform()
            rotateTransform.rotate(-90)
            self.imagePixmap = self.imagePixmap.transformed(rotateTransform)
            self.pictureLabel.setPixmap(self.imagePixmap)
            self.pictureLabel.adjustSize()
        self._setStatus("Rotated the image 90 degrees Counter-Clockwise")

    def transformBlackNWhite(self):
        targetImage = self.imagePixmap.toImage()
        # print(targetImage)
        imgWidth = targetImage.width()
        imgHeight = targetImage.height()
        # print(imgHeight)
        # print(imgWidth)
        for x in range(0,imgWidth):
            for y in range(0,imgHeight):
                targetPixel = targetImage.pixelColor(x,y).getRgb()
                #print(targetPixel.getRgb())
                pixel_red = targetPixel[0]
                pixel_blue = targetPixel[1]
                pixel_green = targetPixel[2]
                pixel_avg = (pixel_red + pixel_blue + pixel_green) / 3
                new_color = QColor(0,0,0)
                if pixel_avg > 127:
                    new_color = QColor(255,255,255)
                targetImage.setPixelColor(x,y,new_color)
        
        targetPixmap = QPixmap(targetImage)
        # targetPixel = targetPixmap.fromImage(targetImage)
        self.imagePixmap = targetPixmap
        self.pictureLabel.setPixmap(self.imagePixmap)
        self.pictureLabel.adjustSize()
        self._setStatus("Turned the image Black and White")

    def transformGrayScale(self):
        targetImage = self.imagePixmap.toImage()
        # print(targetImage)
        imgWidth = targetImage.width()
        imgHeight = targetImage.height()
        # print(imgHeight)
        # print(imgWidth)

        for x in range(0,imgWidth):
            for y in range(0,imgHeight):
                targetPixel = targetImage.pixelColor(x,y).getRgb()
                #print(targetPixel.getRgb())
                pixel_red = targetPixel[0]
                pixel_blue = targetPixel[1]
                pixel_green = targetPixel[2]
                pixel_avg = int((pixel_red + pixel_blue + pixel_green) / 3)
                new_color = QColor(pixel_avg,pixel_avg,pixel_avg)
                targetImage.setPixelColor(x,y,new_color)
        
        targetPixmap = QPixmap(targetImage)
        # targetPixel = targetPixmap.fromImage(targetImage)
        self.imagePixmap = targetPixmap
        self.pictureLabel.setPixmap(self.imagePixmap)
        self.pictureLabel.adjustSize()
        self._setStatus("Turned the image into grayscale")

# ======================================================================= PictureBar Stuff ===================================
    def _createPictureBarLayout(self):
        """
        Creates the sidebar that views the image, also has upload and save buttons
        """
        pictureBar = QVBoxLayout()
        # scrollArea = QScrollArea()
        
        self.pictureLabel = QLabel("No Image Loaded /n Click the 'Choose an Image' button to select an Image")
        # adds scroll since images might be too big
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.pictureLabel)
        scrollArea.setAlignment(Qt.AlignCenter)
        uploadButton = QPushButton("Choose an Image")
        uploadButton.clicked.connect(self.getImage)
        pictureBar.addWidget(scrollArea)
        pictureBar.addWidget(uploadButton)
        pictureBar.addWidget(QPushButton("save image button"))
    
        
        return pictureBar

    def getImage(self):
        # opens in current directory
        # returns a tuple
        file_name = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)" )
        # incase you cancel
        if file_name:
            #self.pictureLabel.setText(file_name[0])
            self.originalFilePath = file_name[0]
            self.imagePixmap = QPixmap(file_name[0])
            self.originalImagePixmap = self.imagePixmap
            #self.pictureLabel.setPixmap(self.ImagePixmap.scaled(1000,800,  Qt.KeepAspectRatio))
            self.pictureLabel.setPixmap(self.imagePixmap)
            self.pictureLabel.adjustSize()
            self.pictureLabel.setAlignment(Qt.AlignCenter)
            # self.pictureLabel.setScaledContents(True)
            self._setStatus("Loaded the image")






if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

