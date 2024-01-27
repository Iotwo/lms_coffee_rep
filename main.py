import sys
from io import StringIO

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5 import uic

import sqlite3


class Espresso(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.db_connector = sqlite3.connect(".\coffee.sqlite")
        self.cursor = self.db_connector.cursor()
        self.row_data = []
        self.editor = None
        self.col_names = ["ID", "название сорта", "степень обжарки", "молотый/в зернах",
                          "описание вкуса", "цена", "объем упаковки"]

        self.load_data()
        return None
    
    def initUI(self) -> None:
        with open(file="main.ui", mode='r', encoding="utf-8") as template:
            uic.loadUi(StringIO(template.read()), self)
        self.table.cellDoubleClicked.connect(self.gather_cell_data_and_edit)
        self.addRec_menuItem.triggered.connect(self.add_new_rec)
        return None

    def load_data(self) -> None:
        
        rows = self.cursor.execute("select * from coffee").fetchall()
        self.table.clearContents()
        self.table.setHorizontalHeaderLabels(self.col_names)
        self.table.setRowCount(len(rows))
        rows = [tuple(map(str, [elem for elem in row])) for row in rows]
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                self.table.setItem(i, j, QTableWidgetItem(rows[i][j]))
                
        return None

    def gather_cell_data_and_edit(self, row_index) -> None:
        row_data = [self.table.item(row_index, j).text() for j in range(self.table.columnCount())]
        self.editor = AddOrEditCoffee(self, row_data)
        self.editor.show()
        return None

    def add_new_rec(self) -> None:
        print("hey!")
        self.editor = AddOrEditCoffee(self, [])
        self.editor.show()
        print("ho!")
        return None


class AddOrEditCoffee(QWidget):
    def __init__(self, parent, coffee_data) -> None:
        super().__init__()
        self.parent = parent
        self.initUI()
        self.db_connector = sqlite3.connect(".\coffee.sqlite")
        self.cursor = self.db_connector.cursor()
        self.edit_id = -1
        if coffee_data is not None and len(coffee_data) > 0:
            self.edit_id = coffee_data[0]
            self.name_txtEd.setText(coffee_data[1])
            self.burn_txtEd.setText(coffee_data[2])
            self.blend_txtEd.setText(coffee_data[3])
            self.taste_txtEd.setText(coffee_data[4])
            self.price_txtEd.setText(coffee_data[5])
            self.vol_txtEd.setText(coffee_data[6])
        else:
            pass
        return None
    
    def initUI(self) -> None:
        with open(file="addEditCoffeeForm.ui", mode='r', encoding="utf-8") as template:
            uic.loadUi(StringIO(template.read()), self)
        self.addEdit_btn.clicked.connect(self.add_or_edit_record)
        return None

    def add_or_edit_record(self) -> None:
        data = [self.name_txtEd.text(), self.burn_txtEd.text(), self.blend_txtEd.text(),
                self.taste_txtEd.text(), self.price_txtEd.text(), self.vol_txtEd.text()]
        if self.edit_id != -1:  # update existing record
            sql_cmd = "UPDATE coffee SET " +\
                      "name=" + '\'' + data[0] + '\'' + ',' +\
                      "burn_degree=" + '\'' + data[1] + '\'' + ',' +\
                      "blend=" + '\'' + data[2] + '\'' + ',' +\
                      "taste_descr=" + '\'' + data[3] + '\'' + ',' +\
                      "price=" + data[4] + ',' +\
                      "vol=" + '\'' + data[5] + '\'' +\
                      " WHERE id=" + str(self.edit_id) + ';'
            
            self.cursor.execute(sql_cmd)
        else:  # add new record
            sql_cmd = "INSERT INTO coffee (name, burn_degree, blend, taste_descr, price, vol) VALUES(?, ?, ?, ?, ?, ?)"
            self.cursor.execute(sql_cmd, data)
        self.db_connector.commit()
        self.parent.load_data()
        self.close()
        return None


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec())
