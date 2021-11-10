import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("testdb.ui", self)
        self.con = sqlite3.connect("QT_Project_db.db")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.add_result)
        # self.tableWidget.itemChanged.connect(self.item_changed)
        # self.pushButton_2.clicked.connect(self.save_results)
        # self.modified = {}
        # self.titles = None
        # self.dateEdit.dateChanged.connect(self.onDateChanged)

    # def onDateChanged(self, qDate):
    #     print('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))


    def add_result(self):
        self.name_ = self.lineEdit.text()
        self.summa_ = self.spinBox.value()
        self.cat_ = self.comboBox.currentText()
        self.date_ = self.dateEdit.text()
        listt = []
        listt.append(str(self.name_))
        listt.append(int(str(self.summa_)))
        listt.append(self.date_)
        listt.append(self.cat_)
        self.cur.execute(f"""INSERT INTO rashodi(name, summa, date, category)
        VALUES(?, ?, ?, ?)""", listt)

        self.con.commit()


    def item_changed(self, item):
        pass

    def save_results(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())