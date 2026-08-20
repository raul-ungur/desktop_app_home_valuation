from PySide6.QtWidgets import QApplication,QCheckBox, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout,  QVBoxLayout

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

import sys

import requests



app = QApplication(sys.argv)
window = QWidget()

class Worker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def run(self):
        try:
            result = request()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
        
class LoadingPopup(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Please wait")
        self.setFixedSize(250,200)

        layout = QVBoxLayout()

        self.spinner = QLabel("◌")
        self.spinner.setAlignment(Qt.AlignCenter)
        self.spinner.setFont(QFont("Arial",35))

        self.loading_label = QLabel("Loading...It can last up to 2 minutes.")
        self.loading_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.spinner)
        layout.addWidget(self.loading_label)

        self.setLayout(layout)

class ResultPopup(QWidget):
    def __init__(self, message):
        super().__init__()

        self.setWindowTitle("House Estimate")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()

        title = QLabel("Result")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))

        text = QLabel(message)
        text.setAlignment(Qt.AlignCenter)
        text.setWordWrap(True)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(text)
        layout.addWidget(close_button)

        self.setLayout(layout)

def update_house_info():
    button_submit.setEnabled(False)

    loading_popup = LoadingPopup()
    loading_popup.show()

    worker = Worker()

    def on_finished(result):
        loading_popup.close()
        result_popup = ResultPopup(result["message"])
        result_popup.show()

        window.result_popup = result_popup
        worker.deleteLater()

    sq_text = input_square.text()
    rooms_text = input_rooms.text()
    bathrooms_text = input_bathrooms.text()

    try:
        float(sq_text)
        int(rooms_text)
        int(bathrooms_text)
    except ValueError:
        error_popup = ResultPopup(
            "Please enter valid numeric values."
        )
        error_popup.show()
        window.error_popup = error_popup
        return
    def on_error(error):
        loading_popup.close()

        layout.addWidget(
            QLabel("Error: "+ error, window)
        )
        worker.deleteLater()

    worker.finished.connect(on_finished)
    worker.error.connect(on_error)

    worker.start()

    window.worker = worker
    window.loading_popup = loading_popup


SERVER_URL = "http://192.168.1.7:8000"


def request():
    data = {
         "square":input_square.text() ,
         "rooms": input_rooms.text(),
         "bathrooms": input_bathrooms.text(),
         "garage": checkbox.isChecked()
    }
    response = requests.post(
        f"{SERVER_URL}/api/estimate", json=data
    )
    print(response.status_code)
    print(response.text)

    response.raise_for_status()
    return response.json()


def reset():
    input_square.clear() ,
    input_rooms.clear(),
    input_bathrooms.clear(),
    checkbox.setChecked(False)
    button_submit.setEnabled(True)

window.setWindowTitle("My PySide6 App")
window.setGeometry(550, 300, 400, 300)


layout = QVBoxLayout()
layout.setAlignment(Qt.AlignCenter)
layout.setContentsMargins(20, 40, 20, 40)



label_title = QLabel("House Information", window)
label_title.setFont(QFont("Arial", 24, QFont.Bold))

label_square = QLabel("Square meters:", window)

input_square = QLineEdit()
input_square.setPlaceholderText("Enter square meters")


label_rooms = QLabel("Rooms:", window)

input_rooms = QLineEdit()
input_rooms.setPlaceholderText("Enter Rooms")


label_bathrooms = QLabel("Bathrooms:", window)

input_bathrooms = QLineEdit()
input_bathrooms.setPlaceholderText("Enter Bathrooms")

label_garage = QLabel(" Garage:", window)

checkbox = QCheckBox()

button_submit = QPushButton("Submit", window, clicked=lambda: update_house_info())
button_reset = QPushButton("Reset ⟲", window, clicked=lambda: reset())

layout.addWidget(label_title)
layout.addWidget(label_square)
layout.addWidget(input_square)
layout.addWidget(label_rooms)
layout.addWidget(input_rooms)
layout.addWidget(label_bathrooms)
layout.addWidget(input_bathrooms)
layout.addWidget(label_garage)
layout.addWidget(checkbox)
layout.addWidget(button_submit)
layout.addWidget(button_reset)



window.setLayout(layout)
window.show()
sys.exit(app.exec())