# import sqlite3
# import sys

# from PyQt5 import uic
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

# import antigravity


# class MyWidget(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi("testdb.ui", self)
#         self.con = sqlite3.connect("QT_Project_db.db")
#         self.cur = self.con.cursor()
#         self.pushButton.clicked.connect(self.add_result)
#         # self.tableWidget.itemChanged.connect(self.item_changed)
#         # self.pushButton_2.clicked.connect(self.save_results)
#         # self.modified = {}
#         # self.titles = None
#         # self.dateEdit.dateChanged.connect(self.onDateChanged)

#     # def onDateChanged(self, qDate):
#     #     print('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))


#     def add_result(self):
#         self.name_ = self.lineEdit.text()
#         self.summa_ = self.spinBox.value()
#         self.cat_ = self.comboBox.currentText()
#         self.date_ = self.dateEdit.text()
#         listt = []
#         listt.append(str(self.name_))
#         listt.append(int(str(self.summa_)))
#         listt.append(self.date_)
#         listt.append(self.cat_)
#         self.cur.execute(f"""INSERT INTO rashodi(name, summa, date, category)
#         VALUES(?, ?, ?, ?)""", listt)

#         self.con.commit()


#     def item_changed(self, item):
#         pass

#     def save_results(self):
#         pass


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyWidget()
#     ex.show()
#     sys.exit(app.exec())

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QPixmap


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.btn.clicked.connect(self.bebraa)

    def bebraa(self):
        data_names = ['qwerty', 'Санкт-Петербург', 'Сочи', 'Архангельск',
              'Владимир', 'Краснодар', 'Курск', 'Воронеж',
              'Ставрополь', 'Мурманск']
        data_values = [1076, 979, 222, 189, 137, 134, 124, 124, 91, 79]

        dpi = 80
        fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
        mpl.rcParams.update({'font.size': 9})

        plt.title('Бебра')

        xs = range(len(data_names))

        plt.pie(
            data_values, autopct='%.1f', radius = 1.1,
            explode = [0.15] + [0 for _ in range(len(data_names) - 1)] )
        plt.legend(
            bbox_to_anchor = (-0.16, 0.45, 0.25, 0.25),
            loc = 'lower left', labels = data_names )
        fig.savefig('pie.png')
        pixmap = QPixmap('pie.png')
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())