import sys
import sqlite3
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from sqlite3.dbapi2 import Cursor
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5 import QtCore


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.information_k = 0
        self.Information_btn.clicked.connect(self.information)
        self.information_text.hide()
        self.information_text.setText(
            'Эта программа поможет вам следить за своими финансами, а также правильно ими распоряжаться.')
        self.rashod_btn.clicked.connect(self.rashod_func)
        self.popolnenie_btn.clicked.connect(self.popolnit_func)
        self.update_btn.clicked.connect(self.update_func)
        # Обновляем главное окно
        self.update_main_window()

    '''
    обновляет главное окно
    '''

    def update_func(self):
        self.update_main_window()

    '''
    информация о приложении
    '''

    def information(self):
        self.information_k += 1
        if self.information_k % 2 != 0:
            self.information_text.show()
        else:
            self.information_text.hide()

    '''
    вызывает окно расходов
    '''

    def rashod_func(self):
        self.form = AddRashod()
        self.form.exec_()

    '''
    вызывает окно доходов
    '''

    def popolnit_func(self):
        self.form = AddPopolnenia(self)
        self.form.exec_()

    '''
    сумма расходов
    '''

    def rashod_sum(self):
        vse_rashodi_list = []
        vse_rashodi = self.cursor.execute(
            """SELECT summa FROM rashodi""").fetchall()
        for i in vse_rashodi:
            vse_rashodi_list.append(int(str(i)[1:-2]))

        return sum(vse_rashodi_list)

    '''
    сумма доходов
    '''

    def dohod_sum(self):
        vse_dohodi_list = []
        vse_dohodi = self.cursor.execute(
            """SELECT summa FROM dohodi""").fetchall()
        for i in vse_dohodi:
            vse_dohodi_list.append(int(str(i)[1:-2]))

        return sum(vse_dohodi_list)

    '''
    обновление главного окна
    '''

    def update_main_window(self):
        self.balance.setText(
            f'     Остаток средств: {self.dohod_sum() - self.rashod_sum()} руб.')
        self.dohod.setText(
            f'     Зачисления: {self.dohod_sum()} руб.')

        self.rashod.setText(
            f'     Расходы: {self.rashod_sum()} руб.')


class AddRashod(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_rashodi.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.addr.clicked.connect(self.add_elem)
        self.graph_btn.clicked.connect(self.graph_window)
        self.rashod_window.itemDoubleClicked.connect(self.delete_rashod_func)
        self.update_rashod()
        self.update_category_rashod()

    '''
    вызывает окно добавления элемента
    '''

    def add_elem(self):
        self.form = AddElem(self)
        self.form.exec_()
        if self.form.ok_pressed:
            self.update_rashod()
            self.update_category_rashod()

    '''
    вызывает окно графика
    '''

    def graph_window(self):
        self.form = GraphWindow(self)
        self.form.exec_()

    '''
    обновляет/отображает список расходов
    '''

    def update_rashod(self):
        self.rashod_spisok = []
        self.rashod_window.clear()
        self.spisok_rashodov = self.cursor.execute(
            """SELECT * FROM rashodi""").fetchall()
        for i in self.spisok_rashodov:
            self.rashod_window.addItem(str(', '.join([str(j) for j in i][1:])))

    '''
    обновляет/отображает список расходов по категориям
    '''

    def update_category_rashod(self):
        self.category_rashod_dict = {}
        self.category_rashod_dict_str = ''
        for i in self.spisok_rashodov:
            if i[-1] not in self.category_rashod_dict:
                self.category_rashod_dict[i[-1]] = [i[1:-1]]
            else:
                categoryes = self.category_rashod_dict.get(i[-1])
                categoryes.append(i[1:-1])
        for key, value in self.category_rashod_dict.items():
            values = ''
            for elem_cat in value:
                values += f'''{elem_cat[0]}, {str(elem_cat[1])}, {str(elem_cat[2])}\n'''
            self.category_rashod_dict_str += f'''---{key}--- \n{values}\n'''
        self.categories_window.setText(self.category_rashod_dict_str)

    '''
    вызывает окно подтверждения
    '''

    def delete_rashod_func(self, item):
        items = [self.rashod_window.item(x)
                 for x in range(self.rashod_window.count())]
        self.form = DeleteFuncR(self, items.index(item))
        self.form.exec_()
        if self.form.ok_pressed_r:
            self.update_rashod()
            self.update_category_rashod()


class AddElem(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('add_elem.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.main_window = MyWidget
        self.ok_btn.clicked.connect(self.add_rashod)
        self.cancel_btn.clicked.connect(self.close)
        self.ok_pressed = False
        today = QtCore.QDate.currentDate()
        self.date_edit.setDate(today)

    '''
    добавляет расход в БД
    '''

    def add_rashod(self):
        self.name_ = self.name_edit.text()
        self.summa_ = self.summa_edit.value()
        self.cat_ = self.cat_edit.currentText()
        self.date_ = self.date_edit.text()
        rashod_inf = []
        if self.name_ != '':
            rashod_inf.append(str(self.name_))
        if self.summa_ != 0:
            rashod_inf.append(int(str(self.summa_)))
        rashod_inf.append(self.date_)
        rashod_inf.append(self.cat_)
        if len(rashod_inf) == 4:
            self.cursor.execute(f"""INSERT INTO rashodi(name, summa, date, category)
            VALUES(?, ?, ?, ?)""", rashod_inf)
            self.connection.commit()
        self.ok_pressed = True
        self.close()


class AddPopolnenia(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('add_popolnenia.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.main_window = MyWidget
        self.addp.clicked.connect(self.add_elem_z)
        self.dohod_window.itemDoubleClicked.connect(self.delete_dohod_func)
        self.update_dohod()

    '''
    вызывает окно добавления элемента
    '''

    def add_elem_z(self):
        self.form = AddElemZ(self)
        self.form.exec_()
        if self.form.ok_pressed_z:
            self.update_dohod()
            # MyWidget.update_main_window(self)

    '''
    обновляет/отображает список доходов
    '''

    def update_dohod(self):
        self.dohod_spisok = []
        self.dohod_window.clear()
        self.spisok_dohodov = self.cursor.execute(
            """SELECT * FROM dohodi""").fetchall()
        for i in self.spisok_dohodov:
            self.dohod_window.addItem(str(', '.join([str(j) for j in i][1:])))

        '''
    вызывает окно подтверждения
    '''

    def delete_dohod_func(self, item):
        items = [self.dohod_window.item(x)
                 for x in range(self.dohod_window.count())]
        self.form = DeleteFuncD(self, items.index(item))
        self.form.exec_()
        if self.form.ok_pressed_d:
            self.update_dohod()


class AddElemZ(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('add_elem_z.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.main_window = MyWidget
        self.ok_btn_z.clicked.connect(self.add_dohod)
        self.cancel_btn_z.clicked.connect(self.close)
        self.ok_pressed_z = False
        today = QtCore.QDate.currentDate()
        self.date_edit_z.setDate(today)

    '''
    добавляет доход в БД
    '''

    def add_dohod(self):
        self.name_ = self.name_edit_z.text()
        self.summa_ = self.summa_edit_z.value()
        self.date_ = self.date_edit_z.text()
        dohod_inf = []
        if self.name_ != '':
            dohod_inf.append(str(self.name_))
        if self.summa_ != 0:
            dohod_inf.append(int(str(self.summa_)))
        dohod_inf.append(self.date_)
        if len(dohod_inf) == 3:
            self.cursor.execute(f"""INSERT INTO dohodi(name, summa, date)
            VALUES(?, ?, ?)""", dohod_inf)
            self.connection.commit()
        self.ok_pressed_z = True
        self.close()


class GraphWindow(QDialog):
    def __init__(self, MyWidget):
        super().__init__()
        uic.loadUi('graph_ui.ui', self)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.back_btn.clicked.connect(self.close)
        self.cat_name_spisok = []
        self.cat_sum_spisok = []
        self.graf_categ()

    '''
    берет информацию из БД
    '''

    def graf_categ(self):
        self.rashod_spisok = ''
        self.spisok_rashodov = self.cursor.execute(
            """SELECT * FROM rashodi""").fetchall()
        self.category_rashod_dict = {}
        for i in self.spisok_rashodov:
            if i[-1] not in self.category_rashod_dict:
                self.category_rashod_dict[i[-1]] = [i[1:-1]]
            else:
                categoryes = self.category_rashod_dict.get(i[-1])
                categoryes.append(i[1:-1])
        for key, value in self.category_rashod_dict.items():
            self.cat_name_spisok.append(key)
            cat_sum = 0
            for elem_cat in value:
                cat_sum += int(elem_cat[1])
            self.cat_sum_spisok.append(cat_sum)
        self.build_a_graph()

    '''
    строит график
    '''

    def build_a_graph(self):
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(720 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 9})
        plt.title('График расходов по категориям')
        plt.pie(
            self.cat_sum_spisok, autopct='%.1f', radius=1.2,
            explode=[0] + [0 for _ in range(len(self.cat_name_spisok) - 1)])
        plt.legend(
            bbox_to_anchor=(-0.6, 0.615, 0, 0),
            loc='lower left', labels=self.cat_name_spisok)
        fig.savefig('graph_pie.png')
        pixmap = QPixmap('graph_pie.png')
        self.graph_label.setPixmap(pixmap)


class DeleteFuncR(QDialog):
    def __init__(self, main_window, item):
        super().__init__()
        self.item = item
        uic.loadUi('delete_item.ui', self)
        self.close_btn.clicked.connect(self.close)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.ok_btn.clicked.connect(self.deletes_rashod)
        self.ok_pressed_r = False

    '''
    удаляет расход
    '''

    def deletes_rashod(self):
        result = self.cursor.execute("""SELECT id FROM rashodi""").fetchall()
        result = [int(str(i)[1:-2]) for i in result]
        id_item = result[self.item]
        self.cursor.execute(
            """DELETE FROM rashodi WHERE id == ?""", (id_item, ))
        self.connection.commit()
        self.close()
        self.ok_pressed_r = True


class DeleteFuncD(QDialog):
    def __init__(self, main_window, item):
        super().__init__()
        self.item = item
        uic.loadUi('delete_item_d.ui', self)
        self.close_btn.clicked.connect(self.close)
        # подключение БД
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()
        self.ok_btn.clicked.connect(self.deletes_dohod)
        self.ok_pressed_d = False

    '''
    удаляет расход
    '''

    def deletes_dohod(self):
        result = self.cursor.execute("""SELECT id FROM dohodi""").fetchall()
        result = [int(str(i)[1:-2]) for i in result]
        id_item = result[self.item]
        self.cursor.execute(
            """DELETE FROM dohodi WHERE id == ?""", (id_item, ))
        self.connection.commit()
        self.close()
        self.ok_pressed_d = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
