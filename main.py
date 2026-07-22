from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton,  QHBoxLayout

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import sys

app = QApplication(sys.argv)
window = QWidget()

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

input_garage = QLineEdit()
input_garage.setPlaceholderText("Enter (yes/no) if there is a garage")



layout.addWidget(label_title)
layout.addWidget(label_square)
layout.addWidget(input_square)
layout.addWidget(label_rooms)
layout.addWidget(input_rooms)
layout.addWidget(label_bathrooms)
layout.addWidget(input_bathrooms)
layout.addWidget(label_garage)
layout.addWidget(input_garage)


window.setLayout(layout)
window.show()
sys.exit(app.exec())