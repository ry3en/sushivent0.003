import sys
from PyQt6.QtWidgets import QApplication
from SushiSystem import SushiSystem

app = QApplication(sys.argv)

sushi = SushiSystem()
sys.exit(app.exec())