import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
import serial

class GUI(QWidget):

    def __init__(self, device):
        QWidget.__init__(self)

        # Arduino stuff
        self.device = device
        self.connection = serial.Serial(self.device, 9600)
        self.refreshRateFps = 10

        self.text = QLabel("No gesture")
        #self.button = QPushButton("Click me!")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        #self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        #self.button.clicked.connect(self.onButton)

        self.poolSerialDevice()

    #def onButton(self):
    #    self.text.setText("PREMUTO")

    def poolSerialDevice(self):

        if self.connection.in_waiting == 0: # No messages from arduino
            QTimer.singleShot(int(1000/self.refreshRateFps), self.poolSerialDevice)
        elif self.connection.in_waiting > 0: # Some messages from arduino
            message = self.connection.readline().decode('ascii')

            self.text.setText(message)

            QTimer.singleShot(int(1000/self.refreshRateFps), self.poolSerialDevice)

if __name__ == "__main__":
    app = QApplication([])
    gui=GUI(sys.argv[1])
    gui.resize(400, 300)
    gui.setWindowTitle("Gesture")
    gui.show()
    sys.exit(app.exec_())
