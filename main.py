from PySide6.QtWidgets import QApplication,QCheckBox, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout,  QVBoxLayout

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import sys
import sqlite3
import pandas as pd
from threading import Timer

import requests

conn = sqlite3.connect('houses.db')

df = pd.read_sql_query("SELECT * FROM houses", conn)


app = QApplication(sys.argv)
window = QWidget()

def estimation_price(square,rooms , bathrooms, garage ):
    
    value1 = float(square) * 2000
    value2 = float(rooms) * 2000
    value3 = float(bathrooms) * 1000
    value4 = 0 if garage == False else  1000
   
    final_price = value1 + value2 +  value3 + value4
    
    return f"The price is: { final_price : ,} $"




def update_house_info():
    request()
    sq_text = input_square.text()
    rooms_text = input_rooms.text()
    bathrooms_text = input_bathrooms.text()
    garage_text  = checkbox.isChecked()
    print(df)
    try:
        layout.addWidget(QLabel(str(estimation_price(sq_text, rooms_text, bathrooms_text, garage_text) ) , window))
    except ValueError :
        layout.addWidget(QLabel("Please enter the correct value", window ))
    print(type(garage_text))
    button_submit.setEnabled(False)

SERVER_URL = "http://192.168.1.4:8000"

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
    response.raise_for_status()
    t = Timer(60.0, print(request()))
    t.start
    return response.json()



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


window.setLayout(layout)
window.show()
sys.exit(app.exec())