import sys

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import qGray
from PyQt5.QtWidgets import QAbstractItemDelegate
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QStyleOptionViewItem
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class ImageModel(QAbstractTableModel):
    def __init__(self, *args):
        self.modelImage = QImage()

        super().__init__(*args)

    def setImage(self, image):
        self.beginResetModel()
        self.modelImage = image
        self.endResetModel()

    def rowCount(self, parent=None, *args, **kwargs):
        return self.modelImage.height()

    def columnCount(self, parent=None, *args, **kwargs):
        return self.modelImage.width()

    def data(self, index, role=None):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()
        return qGray(self.modelImage.pixel(index.column(), index.row()))

    def headerData(self, section, orientation, role=None):
        if role == Qt.SizeHintRole:
            return QSize(1, 1)
        return QVariant


class PixelDelegate(QAbstractItemDelegate):
    def __init__(self, parent: QModelIndex = None):
        self.pixelSize = 12
        super().__init__(parent)

    def paint(self, painter: QPainter, option, index: QModelIndex):
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        size = min(option.rect.width(), option.rect.height())
        brightness = index.model().data(index, Qt.DisplayRole)
        radius = (size / 2.0) - (brightness / 255.0 * size / 2.0)
        if radius == 0.0:
            return

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)

        if option.state & QStyle.State_Selected:
            painter.setBrush(option.palette.highlightedText())
        else:
            painter.setBrush(option.palette.text())

        painter.drawEllipse(QRectF(option.rect.x() + option.rect.width() / 2 - radius,
                                   option.rect.y() + option.rect.height() / 2 - radius,
                                   2 * radius, 2 * radius))

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        return QSize(self.pixelSize, self.pixelSize)

    def setPixelSize(self, size):
        self.pixelSize = size


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentPath = QDir.currentPath()
        self.model = ImageModel(self)

        centralWidget = QWidget()

        self.view = QTableView()
        self.view.setShowGrid(False)
        self.view.horizontalHeader().hide()
        self.view.verticalHeader().hide()
        self.view.horizontalHeader().setMinimumSectionSize(1)
        self.view.verticalHeader().setMinimumSectionSize(1)
        self.view.setModel(self.model)

        delegate = PixelDelegate(self)
        self.view.setItemDelegate(delegate)

        pixelSizeLabel = QLabel("Pixel size:")
        pixelSizeSpinBox = QSpinBox()
        pixelSizeSpinBox.setMinimum(4)
        pixelSizeSpinBox.setMaximum(32)
        pixelSizeSpinBox.setValue(12)

        fileMenu = QMenu("&File", self)
        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcuts(QKeySequence.Open)

        self.printAction = fileMenu.addAction('&Print...')
        self.printAction.setEnabled(False)
        self.printAction.setShortcuts(QKeySequence.Print)

        quitAction = fileMenu.addAction('E&xit')
        quitAction.setShortcuts(QKeySequence.Quit)

        helpMenu = QMenu('&Help', self)
        aboutAction = helpMenu.addAction('&About')

        self.menuBar().setNativeMenuBar(False)
        self.menuBar().addMenu(fileMenu)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(helpMenu)

        openAction.triggered.connect(self.chooseImage)
        self.printAction.triggered.connect(self.printImage)
        quitAction.triggered.connect(QCoreApplication.quit)
        aboutAction.triggered.connect(self.showAboutBox)
        pixelSizeSpinBox.valueChanged.connect(delegate.setPixelSize)
        pixelSizeSpinBox.valueChanged.connect(self.updateView)

        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(pixelSizeLabel)
        controlsLayout.addWidget(pixelSizeSpinBox)
        controlsLayout.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.view)
        mainLayout.addLayout(controlsLayout)
        centralWidget.setLayout(mainLayout)

        self.setCentralWidget(centralWidget)

        self.setWindowTitle('Pixalator')
        self.resize(640, 480)

    def openImage(self, fileName):
        image = QImage()

        if image.load(fileName):
            self.model.setImage(image)
            if not fileName.startswith(':/'):
                self.currentPath = fileName
                self.setWindowTitle('%s - Pixelator' % fileName)

        self.updateView()

    def chooseImage(self):
        fileName, _ = QFileDialog(self).getOpenFileName(self, 'Choose an image', self.currentPath, '*')
        print(fileName)
        if fileName:
            self.openImage(fileName)

    def printImage(self):
        pass

    def showAboutBox(self):
        QMessageBox().about(self, 'About the Pixelator example',
                            'This example demonstrates how a standard view and a custom\n'
                            'delegate can be used to produce a specialized representation\n'
                            'of data in a simple custom model.')

    def updateView(self):
        self.view.resizeColumnsToContents()
        self.view.resizeRowsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
