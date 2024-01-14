from sys import argv, exit
from io import StringIO

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic

import sqlite3


class Espresso(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.db_connector = sqlite3.connect(".\coffee.sqlite")
        self.cursor = self.db_connector.cursor()

        self.load_data()
        return None
    
    def initUI(self) -> None:
        with open(file="main.ui", mode='r', encoding="utf-8") as template:
            uic.loadUi(StringIO(template.read()), self)
        return None

    def load_data(self) -> None:
        col_names = ["ID", "название сорта", "степень обжарки", "молотый/в зернах",
                     "описание вкуса", "цена", "объем упаковки"]
        rows = self.cursor.execute("select * from coffee").fetchall()
        self.table.clearContents()
        self.table.setHorizontalHeaderLabels(col_names)
        self.table.setRowCount(len(rows))
        rows = [tuple(map(str, [elem for elem in row])) for row in rows]
        print(rows)
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                self.table.setItem(i, j, QTableWidgetItem(rows[i][j]))
        
                
        return None
    

if __name__ == "__main__":
    app = QApplication(argv)
    ex = Espresso()
    ex.show()
    exit(app.exec())
